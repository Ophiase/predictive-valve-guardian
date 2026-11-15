from dataclasses import dataclass
from typing import Final, Self

import numpy as np
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from valve_guardian.arrays import Signals

from valve_guardian_dashboard.verdicts import StoredVerdicts

ACCEPTED: Final = ("txt", "csv", "tsv")


@dataclass(frozen=True)
class Upload:
    pressure: Signals
    flow: Signals

    @classmethod
    def from_sidebar(cls) -> Self | None:
        st.sidebar.header("Data upload")
        pressure = cls.uploader("PS2 signal (pressure)", "ps2")
        flow = cls.uploader("FS1 signal (flow)", "fs1")
        if pressure is None or flow is None:
            return None
        return cls(pressure=cls.signals(pressure), flow=cls.signals(flow))

    @staticmethod
    def uploader(label: str, key: str) -> UploadedFile | None:
        return st.sidebar.file_uploader(
            label, type=ACCEPTED, key=key, on_change=StoredVerdicts.clear
        )

    @staticmethod
    @st.cache_data
    def signals(file: UploadedFile) -> Signals:
        return np.loadtxt(file)

    @property
    def cycles(self) -> int:
        return self.pressure.shape[0]

    @property
    def is_aligned(self) -> bool:
        return self.pressure.shape[0] == self.flow.shape[0]
