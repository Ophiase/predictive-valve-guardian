import sys
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

import yaml

type Document = Mapping[str, Any]


@dataclass(frozen=True)
class Workload:
    """What compose and Kubernetes must agree on for one service."""

    image: str
    port: int
    environment: frozenset[str]
    read_only: bool
    scratch: frozenset[str]

    @classmethod
    def of_compose(cls, service: Document) -> Self:
        image = str(service["image"]).split(":")[0].rsplit("/", 1)[-1]
        port = int(str(service["ports"][0]).rsplit(":", 1)[-1])
        return cls(
            image=image,
            port=port,
            environment=frozenset(service.get("environment") or {}),
            read_only=service.get("read_only") is True,
            scratch=frozenset(service.get("tmpfs") or []),
        )

    @classmethod
    def of_deployment(cls, deployment: Document) -> Self:
        pod = deployment["spec"]["template"]["spec"]
        container = pod["containers"][0]
        volumes = {volume["name"] for volume in pod.get("volumes", []) if "emptyDir" in volume}
        mounts = container.get("volumeMounts", [])
        return cls(
            image=container["image"].split(":")[0].rsplit("/", 1)[-1],
            port=container["ports"][0]["containerPort"],
            environment=frozenset(variable["name"] for variable in container.get("env", [])),
            read_only=container["securityContext"].get("readOnlyRootFilesystem") is True,
            scratch=frozenset(mount["mountPath"] for mount in mounts if mount["name"] in volumes),
        )


class Parity:
    """Every compose service is a Deployment of the same name that runs it the same way."""

    @staticmethod
    def of(compose: Path, manifests: Path) -> Iterator[str]:
        services = yaml.safe_load(compose.read_text())["services"]
        documents = [each for each in yaml.safe_load_all(manifests.read_text()) if each]
        deployments = {
            each["metadata"]["name"]: each for each in documents if each["kind"] == "Deployment"
        }
        for name in sorted(services.keys() ^ deployments.keys()):
            yield f"{name}: in only one of compose and Kubernetes"
        for name in sorted(services.keys() & deployments.keys()):
            local = Workload.of_compose(services[name])
            cluster = Workload.of_deployment(deployments[name])
            for field, value in vars(local).items():
                if getattr(cluster, field) != value:
                    yield f"{name}: {field} is {value} in compose, {getattr(cluster, field)} in Kubernetes"


if __name__ == "__main__":
    smells = list(Parity.of(Path(sys.argv[1]), Path(sys.argv[2])))
    print("\n".join(smells) or "parity: compose and Kubernetes agree")
    sys.exit(1 if smells else 0)
