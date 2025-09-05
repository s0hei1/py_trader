import streamlit as st
from streamlit import session_state as state
from src.ui.viewmodel.trade_vm import TradeVM

if not "trade_vm" in st.session_state:
    state.trade_vm = TradeVM()

st.set_page_config(layout="wide")

cols = st.columns([1.5,2,2,0.5,3.5])

with cols[0]:
    st.selectbox("Select Time Frame", [None] + state.trade_vm.get_time_frames(), key = "pattern_tf")
    st.selectbox(
        "Select Currency",
        [None] + state.trade_vm.get_symbols(),
        key="currency_pattern",
        on_change=lambda: state.trade_vm.set_currency(
            state.currency_select
        )
    )

    if st.button("add Pattern"):
        pass

with cols[1]:
    st.date_input("Pattern Start Date")
    st.time_input("Pattern Start Time")

with cols[2]:
    st.date_input("Pattern End Date")
    st.time_input("Pattern End Time")

with cols[3]:
    pass

with cols[4]:
    st.text_input(
        "Risk Percentage %",
        disabled=True,
        value=state.trade_vm.risk_percentage,
        key="risk_percentage_input",
        on_change=lambda: state.trade_vm.set_risk_percentage(
            state.risk_percentage_input
        ))

    st.text_input(
        "Volume Size $",
        value=state.trade_vm.balance,
        disabled=True,
        key="balance_input",
        on_change=lambda: state.trade_vm.set_balance(
            state.volume_size_input
        ))

st.markdown("---")

cols = st.columns(3)

with cols[0]:
    st.selectbox(
        "Select Currency",
        [None] + state.trade_vm.get_symbols(),
        key="currency_select",
        on_change=lambda: state.trade_vm.set_currency(
            state.currency_select
        )
    )

with cols[1]:
    time_frame = st.selectbox("Select Time Frame", [None] + state.trade_vm.get_time_frames())

with cols[2]:
    st.selectbox(
        "Select Currency",
        [None] + state.trade_vm.get_order_types(),
        key="order_select",
        on_change=lambda: state.trade_vm.set_order_type(
            state.order_select
        )
    )

cols = st.columns(3)

with cols[0]:
    st.text_input(
        "Entry Price",
        value=state.trade_vm.entry_price,
        key="entry_price_input",
        on_change=lambda: state.trade_vm.set_entry_price(
            state.entry_price_input
        ))

with cols[1]:
    st.text_input(
        "Stop loss pips",
        value=state.trade_vm.sl,
        key="sl_input",
        on_change=lambda: state.trade_vm.set_sl(
            state.sl_input
        ))

with cols[2]:
    st.text_input(
        "Take profit pips",
        value=state.trade_vm.tp,
        key="tp_input",
        on_change=lambda: state.trade_vm.set_tp(
            state.tp_input
        ))

if st.button("Place Order"):
    set_order_result = state.trade_vm.set_order()
    if set_order_result.has_error:
        st.error(set_order_result.message)
    if not set_order_result.has_error:
        st.success(set_order_result.message)

