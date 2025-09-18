import streamlit as st
from streamlit import session_state as state
from src.ui.shared_views.show_result import StaticAgGrid
from src.ui.viewmodel.pattern_vm import PatternVM


st.set_page_config(layout="wide")

if 'patterns_vm' not in state:
    state.patterns_vm = PatternVM()


StaticAgGrid(df = state.patterns_vm.patterns_df)