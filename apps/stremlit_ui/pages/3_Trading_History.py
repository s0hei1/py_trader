import streamlit as st
from st_aggrid import AgGrid
from streamlit import session_state as state
from src.ui.viewmodel.trading_history_vm import TradingHistoryVM

st.set_page_config(layout="wide")

if 'trading_history_vm' not in state:
    state.trading_history_vm = TradingHistoryVM()

response = AgGrid(
    state.trading_history_vm.deals_history,
    height=240,
    theme="streamlit",
)