import streamlit as st
from streamlit import session_state as state
from src.ui.viewmodel.live_activities_vm import LiveActivitiesVM

st.set_page_config(layout="wide")

if 'live_activities_vm' not in state:
    state.live_activities_vm = LiveActivitiesVM()

cols = st.columns(5)
account_info = state.live_activities_vm.account_info
with cols[0]:
    st.metric("Balance", f"{account_info.balance} $")

with cols[1]:
    st.metric("Equity", f"{account_info.equity} $")

with cols[2]:
    st.metric("Profit", f"{account_info.profit} $")

with cols[4]:
    st.metric("Limit Orders", f"{account_info.limit_orders}")



