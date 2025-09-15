import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from streamlit import session_state as state
from src.ui.shared_views.show_result import show_result
from src.ui.viewmodel.trade_vm import PatternTradingVM

if not "trade_vm" in st.session_state:
    state.trade_vm = PatternTradingVM()

st.set_page_config(layout="wide")

cols = st.columns([1.5, 2, 2, 0.5, 3.5])

with cols[0]:
    st.selectbox(
        "Select Time Frame",
        [None] + state.trade_vm.get_time_frames(),
        key="pattern_tf_selection",
        on_change=lambda: state.trade_vm.set_pattern_time_frame(
            state.pattern_tf_selection
        )

    )

    st.selectbox(
        "Select Currency",
        [None] + state.trade_vm.get_symbols(),
        key="pattern_symbol_selection",
        on_change=lambda: state.trade_vm.set_pattern_symbol(
            state.pattern_symbol_selection
        )
    )

with cols[1]:
    st.date_input(
        "Pattern Start Date",
        key="pattern_start_date_input",
        on_change=lambda: state.trade_vm.set_pattern_start_date(
            state.pattern_start_date_input
        )
    )
    st.time_input(
        "Pattern Start Time",
        key="pattern_start_time_input",
        on_change=lambda: state.trade_vm.set_pattern_start_time(
            state.pattern_start_time_input
        )
    )

with cols[2]:
    st.date_input(
        "Pattern End Date",
        key="pattern_end_date_input",
        on_change=lambda: state.trade_vm.set_pattern_end_date(
            state.pattern_end_date_input
        )
    )
    st.time_input(
        "Pattern End Time",
        key="pattern_end_time_input",
        on_change=lambda: state.trade_vm.set_pattern_end_time(
            state.pattern_end_time_input
        )
    )

with cols[3]:
    pass

with cols[4]:
    """Config"""
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

if st.button("Add Pattern"):
    result = state.trade_vm.add_pattern()
    show_result(result)

st.markdown("---")

cols = st.columns([3,1])

with cols[0]:
    grid_options = GridOptionsBuilder.from_dataframe(state.trade_vm.patterns_df,)
    grid_options.configure_selection(use_checkbox=True)
    grid_options = grid_options.build()

    response = AgGrid(
        state.trade_vm.patterns_df,
        gridOptions=grid_options,
        height=120,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,

    )

    if response.selected_rows is not None:
        state.trade_vm.set_selected_pattern(response.selected_rows.iloc[0]['id'])
    else:
        state.trade_vm.set_selected_pattern(None)


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
        "Select Order Type",
        [None] + state.trade_vm.get_order_types(),
        key="order_type_select",
        on_change=lambda: state.trade_vm.set_order_type(
            state.order_type_select
        )
    )

# with cols[3]:
#     st.selectbox(
#         "Select Order Type",
#         [None] + state.trade_vm.get_order_types(),
#         key="order_type_select",
#         on_change=lambda: state.trade_vm.set_order_type(
#             state.order_type_select
#         )
#     )




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
