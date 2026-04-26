import streamlit as st
from streamlit import session_state as state

from src.ui.viewmodel.auto_trading_vm import AutoTradingVM

if 'auto_trading_vm' not in state:
    state.backtrader_vm = AutoTradingVM()



if st.button("Run"):
    state.backtrader_vm.run_simple_ma_strategy()
