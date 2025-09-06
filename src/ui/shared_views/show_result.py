import streamlit as st
from src.ui.viewmodel.vm_result import VMResult


def show_result(result : VMResult):
    if result.has_error:
        st.error(result.message)
    else:
        st.success(result.message)