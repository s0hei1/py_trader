from typing import get_args

import streamlit as st
import pandas as pd
from streamlit import session_state as state

from src.ui.shared_views.show_result import ShowResult
from src.ui.viewmodel.imports_vm import ImportsVM

if 'imports_vm' not in state:
    state.imports_vm = ImportsVM()

st.header("Import Data")

cols = st.columns([1,3])

with cols[0]:
    st.selectbox(
        "Select The action",
        [None,] + list(get_args(state.imports_vm.Actions)),
        key="selected_action_input",
        on_change= lambda: state.imports_vm.set_selected_action(
            state.selected_action_input
        )
    )

with cols[1]:
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            state.imports_vm.set_uploaded_df(pd.read_csv(uploaded_file))
        if uploaded_file.name.endswith('.xlsx'):
            state.imports_vm.set_uploaded_df(pd.read_excel(uploaded_file))

        st.success("Data Uploaded successfully")

if st.button('Sync Data'):
    result = state.imports_vm.on_sync_data_click()

    ShowResult(result)