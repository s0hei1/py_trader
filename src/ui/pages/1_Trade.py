import streamlit as st
from streamlit import session_state as state
from src.ui.viewmodel.trade_vm import TradeVM

if not "trade_vm" in st.session_state:
    state.trade_vm : TradeVM = TradeVM()

st.set_page_config(layout="wide")

cols = st.columns(2)

with cols[0]:
    st.text_input(
        "Risk Percentage %",
        value=state.trade_vm.risk_percentage,
        key="risk_percentage_input",
        on_change=lambda: state.trade_vm.set_risk_percentage(
            state.risk_percentage_input
        ))

with cols[1]:
    st.text_input(
        "Volume Size $",
        value=state.trade_vm.balance,
        key="balance_input",
        on_change=lambda: state.trade_vm.set_balance(
            state.volume_size_input
        ))

cols = st.columns(2)

with cols[0]:
    currency = st.selectbox("Select Currency", ["EURUSDb"])

with cols[1]:
    time_frame = st.selectbox("Select Time Frame", [None,"m15","H1","H4","Daily"])

cols = st.columns(3)

with cols[0]:
    st.text_input("Entry Price")

with cols[1]:
    st.text_input("Stop loss Pips")

with cols[2]:
    st.text_input("Take Profit Pips")


if st.button("Place Order"):
    pass