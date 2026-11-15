import sys
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any, Final

import yaml

type Service = Mapping[str, Any]

FORBIDDEN_KEYS: Final = ("privileged", "network_mode", "pid", "ipc")
LOOPBACK: Final = "127.0.0.1:"


class ComposeSmells:
    """The few things a compose file of this repository must never do."""

    @classmethod
    def of(cls, path: Path) -> Iterator[str]:
        document = yaml.safe_load(path.read_text())
        for name, service in document.get("services", {}).items():
            yield from (f"{name}: {smell}" for smell in cls.service(service))

    @staticmethod
    def service(service: Service) -> Iterator[str]:
        image = str(service.get("image", ""))
        if ":" not in image.rsplit("/", 1)[-1] or image.endswith(":latest"):
            yield f"image {image!r} needs an explicit tag, never latest"
        yield from (f"{key} is not allowed" for key in FORBIDDEN_KEYS if key in service)
        for port in service.get("ports") or []:
            if not str(port).startswith(LOOPBACK):
                yield f"port {port!r} must bind {LOOPBACK.rstrip(':')}"


if __name__ == "__main__":
    smells = [f"{path}: {smell}" for path in map(Path, sys.argv[1:]) for smell in ComposeSmells.of(path)]
    print("\n".join(smells) or "compose: no smell")
    sys.exit(1 if smells else 0)
