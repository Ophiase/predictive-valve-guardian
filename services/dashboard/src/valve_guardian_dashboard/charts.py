import numpy as np
import pandas as pd
import streamlit as st

from valve_guardian_dashboard.upload import Upload
from valve_guardian_dashboard.verdicts import Verdicts


class Charts:
    @staticmethod
    def cycle(upload: Upload, cycle: int, verdict: bool | None) -> None:
        st.markdown(f"### Cycle {cycle}")
        if verdict is not None:
            status = ":green[Optimal]" if verdict else ":red[Faulty]"
            st.markdown(f"**Prediction:** {status}")
        pressure, flow = st.columns(2)
        with pressure:
            st.write("PS2 signal (pressure)")
            st.line_chart(upload.pressure[cycle])
        with flow:
            st.write("FS1 signal (flow)")
            st.line_chart(upload.flow[cycle])

    @staticmethod
    def table(verdicts: Verdicts) -> None:
        results = pd.DataFrame({
            "cycle": np.arange(len(verdicts)),
            "valve_optimal": verdicts,
        })
        with st.expander("All predictions"):
            st.dataframe(results, width="stretch")
            st.download_button(
                "Download predictions (CSV)",
                results.to_csv(index=False).encode(),
                "predictions.csv",
                "text/csv",
            )
