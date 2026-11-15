import sys
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any, Final

import yaml

REGISTRY: Final = "{{ .Values.global.registry }}"
TAG: Final = "{{ .Values.global.imageTag }}"
SHARED: Final = "stack.yaml"


class ValuesSmells:
    """What a file of app-template values must respect: one concern, tags from the release."""

    @classmethod
    def of(cls, path: Path) -> Iterator[str]:
        document: Mapping[str, Any] = yaml.safe_load(path.read_text()) or {}
        if path.name != SHARED and len(document) != 1:
            yield f"one concern per file, found {', '.join(document)}"
        if "ingress" in document:
            yield "no Ingress: expose through a Gateway API route"
        for name, controller in document.get("controllers", {}).items():
            for container, spec in controller.get("containers", {}).items():
                image = spec.get("image", {})
                if image and (image.get("tag") != TAG or not str(image.get("repository", "")).startswith(REGISTRY)):
                    yield f"{name}/{container}: the image must be {REGISTRY}<name> at {TAG}"


if __name__ == "__main__":
    smells = [f"{path}: {smell}" for path in map(Path, sys.argv[1:]) for smell in ValuesSmells.of(path)]
    print("\n".join(smells) or "values: no smell")
    sys.exit(1 if smells else 0)
