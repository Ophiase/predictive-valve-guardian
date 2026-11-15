from typing import Final

import streamlit as st

KEY: Final = "verdicts"

type Verdicts = tuple[bool, ...]


class StoredVerdicts:
    """The predictions of the current upload, kept across reruns of the page."""

    @staticmethod
    def get() -> Verdicts | None:
        return st.session_state.get(KEY)

    @staticmethod
    def set(verdicts: Verdicts) -> None:
        st.session_state[KEY] = verdicts

    @staticmethod
    def clear() -> None:
        st.session_state.pop(KEY, None)
