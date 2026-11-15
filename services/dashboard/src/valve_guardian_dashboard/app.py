from typing import Final

import streamlit as st
from valve_guardian.model import Predictor

from valve_guardian_dashboard.charts import Charts
from valve_guardian_dashboard.upload import Upload
from valve_guardian_dashboard.verdicts import StoredVerdicts

TITLE: Final = "Predictive Valve Guardian"


@st.cache_resource
def predictor() -> Predictor:
    return Predictor.deployed()


def predict_button(upload: Upload) -> None:
    if st.button("Run predictions", type="primary"):
        with st.spinner("Running predictions..."):
            StoredVerdicts.set(predictor().optimal_valve(upload.pressure, upload.flow))


def page() -> None:
    st.title(TITLE)
    upload = Upload.from_sidebar()
    if upload is None:
        st.info("Upload both the PS2 and FS1 signal files to begin.")
        return
    if not upload.is_aligned:
        st.error("PS2 and FS1 must hold the same number of cycles.")
        return
    st.sidebar.success(f"Loaded {upload.cycles} cycles.")
    st.subheader("Cycle inspection")
    cycle = int(st.number_input("Cycle", min_value=0, max_value=upload.cycles - 1))
    predict_button(upload)
    verdicts = StoredVerdicts.get()
    Charts.cycle(upload, cycle, None if verdicts is None else verdicts[cycle])
    if verdicts is not None:
        Charts.table(verdicts)


st.set_page_config(page_title=TITLE, layout="wide")
page()
