import streamlit as st
from streamlit import session_state as state
from src.ui.viewmodel.config_vm import ConfigVM

if not "config_vm" in st.session_state:
    state.config_vm = ConfigVM()

st.set_page_config(layout="wide")

cols = st.columns(2)

with cols[0]:
    st.text_input(
        "Risk Percentage %",
        value=state.config_vm.risk_percentage,
        key="risk_percentage_input",
        on_change=lambda: state.config_vm.set_risk_percentage(
            state.risk_percentage_input
        ))

with cols[1]:
    st.text_input(
        "Volume Size $",
        value=state.config_vm.total_balance,
        key="balance_input",
        on_change=lambda: state.config_vm.set_total_balance(
            state.balance_input
        ))


if st.button("Update Flags"):
    result = state.config_vm.update_flags()

    if result.has_error:
        st.error(result.message)
    else:
        st.success(result.message)
