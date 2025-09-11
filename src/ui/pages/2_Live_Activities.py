import streamlit as st
from streamlit import session_state as state
from src.ui.viewmodel.live_activities_vm import LiveActivitiesVM
from st_aggrid import AgGrid
import pandas as pd

st.set_page_config(layout="wide")

if 'live_activities_vm' not in state:
    state.live_activities_vm = LiveActivitiesVM()

cols = st.columns(5)
account_info = state.live_activities_vm.account_info
orders = state.live_activities_vm.orders
positions = state.live_activities_vm.positions
with cols[0]:
    st.metric("Balance", f"{account_info.balance} $")

with cols[1]:
    st.metric("Equity", f"{account_info.equity} $")

with cols[2]:
    st.metric("Profit", f"{account_info.profit} $")

with cols[3]:
    st.metric("Active Positions", f"{len(positions)}")
with cols[4]:
    st.metric("Limit Orders", f"{len(orders)}")

orders_df = state.live_activities_vm.get_orders_df()
positions_df = state.live_activities_vm.get_positions_df()

st.markdown("---")

st.write("Orders")
AgGrid(data= orders_df, height=120)
st.write("Postions")
AgGrid(data= positions_df, height=120)
st.markdown("---")



if st.button("sync data"):
    state.live_activities_vm.fetch_data_from_mt5()
    st.rerun()
