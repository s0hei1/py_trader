import streamlit as st
from lightweight_charts.widgets import StreamlitChart
from streamlit import session_state as state
from src.ui.shared_views.show_result import StaticAgGrid
from src.ui.viewmodel.pattern_vm import PatternVM

st.set_page_config(layout="wide")

if 'patterns_vm' not in state:
    state.patterns_vm = PatternVM()

ag_grid_response = StaticAgGrid(df=state.patterns_vm.patterns_df,use_checkbox=True)

if ag_grid_response.selected_rows is not None:
    state.patterns_vm.set_selected_pattern(ag_grid_response.selected_rows['id'])

if state.patterns_vm.selected_pattern is not None:
    chart = StreamlitChart(width=600, height=600)
    df = state.patterns_vm.selected_pattern.copy()

    # If you want timezone-aware ISO 8601 format (2025-09-12T15:00:00+00:00), use:
    # df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    df["time"] = df["datetime"].dt.to_pydatetime().astype(str)
    df.drop(columns=['datetime'],inplace=True)

    chart.set(df[['time', 'open', 'high', 'low', 'close']])
    chart.load()
