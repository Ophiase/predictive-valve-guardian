import logging
import zipfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Final

import httpx

SOURCE: Final = httpx.URL(
    # hardcoded-url: the public UCI archive is the one source of the dataset
    "https://archive.ics.uci.edu/static/public/447/condition+monitoring+of+hydraulic+systems.zip"
)
DOWNLOAD_TIMEOUT_SECONDS: Final = 120

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HydraulicArchive:
    folder: Path = Path("data") / "hydraulic"

    @property
    def pressure(self) -> Path:
        return self.folder / "PS2.txt"

    @property
    def flow(self) -> Path:
        return self.folder / "FS1.txt"

    @property
    def profile(self) -> Path:
        return self.folder / "profile.txt"

    @property
    def is_present(self) -> bool:
        return all(path.exists() for path in (self.pressure, self.flow, self.profile))

    def download(self) -> None:
        logger.info("Downloading %s into %s", SOURCE, self.folder)
        response = httpx.get(SOURCE, timeout=DOWNLOAD_TIMEOUT_SECONDS)
        response.raise_for_status()
        self.folder.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(BytesIO(response.content)) as archive:
            archive.extractall(self.folder)

    def ensure(self) -> None:
        if not self.is_present:
            self.download()
