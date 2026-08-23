import streamlit as st
from streamlit import session_state as state
from apps.stremlit_ui.datasource.api_clients.market_data_client.api_client import MarketDataAPIClient,market_data_client_factory
from apps.stremlit_ui.pages.shared_views.candles_browser import candles_browser_view
from apps.stremlit_ui.viewmodel.backtrader_vm import BackTraderVM
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Backtrader Analysis")

if 'backtrader_vm' not in state:
    state.backtrader_vm = BackTraderVM()

st.header("Backtrader Settings", divider=True)

cols = st.columns(3)
with cols[0]:
    st.selectbox(
        "Select Strategy",
        [None] + state.backtrader_vm.get_strategies(),
        key="selected_strategy",
        on_change=lambda: state.backtrader_vm.set_selected_strategy(
            state.selected_strategy
        )
    )


st.header("Data Browser",divider=True)


brokers ,symbols ,tfs = state.backtrader_vm.get_market_data_info()

broker_map = {b.name: b.id for b in brokers}
symbol_map = {s.name: s.id for s in symbols}
tf_list = [t.name for t in tfs]

cols = st.columns(3)


selected_broker = cols[0].selectbox("Broker", list(broker_map.keys()))
selected_symbol = cols[1].selectbox("Symbol", list(symbol_map.keys()))
selected_tf = cols[2].selectbox("Time Frame", tf_list)

if st.button("Load Candles"):
    try:
        state.backtrader_vm.get_market_data(
            time_frame_name=selected_tf,
            broker_id=broker_map[selected_broker],
            symbol_id=symbol_map[selected_symbol]
        )
    except Exception as e:
        st.error(f"Failed loading candles: {e}")



st.header("Backtrader",divider=True)

if st.button('Cerebro Run'):
    if state.backtrader_vm.is_data_feed:
        state.backtrader_vm.run_strategy()
    else:
        st.error("Data Feed is None")


trade_analyzer_analysis = state.backtrader_vm.get_trade_analyzer_analysis()

time_return_analysis = state.backtrader_vm.get_time_return_analyzer_analysis()
equity_analysis = state.backtrader_vm.get_equity_analysis()
trade_df = state.backtrader_vm.get_trade_details_dataframe()
draw_down_analysis = state.backtrader_vm.get_draw_down_analysis()

if trade_analyzer_analysis is not None:

    st.divider()
    st.header("📈 Equity Tracker")
    fig_line_equity_tracer = px.line(equity_analysis, x= "Index", y = "Equity")
    st.plotly_chart(fig_line_equity_tracer, use_container_width=True)

    data = trade_analyzer_analysis
    st.divider()
    st.header("📈 Trade Analyzer Analysis")

    # 1. Key Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    win_rate = (data.won_total / data.total_closed * 100) if data.total_closed > 0 else 0

    m1.metric("Total Trades", data.total_total)
    m2.metric("Win Rate", f"{win_rate:.2f}%")
    m3.metric("Net PnL", f"${data.pnl_net_total:,.2f}",
              delta=f"{data.pnl_net_average:,.2f} avg")
    m4.metric("Max Win/Loss Streak", f"{data.streak_won_longest} / {data.streak_lost_longest}")

    tab1, tab2, tab3 = st.tabs(["Performance Overview", "PnL Breakdown", "Trade Durations"])

    with tab1:
        col_left, col_right = st.columns(2)

        with col_left:
            # Win/Loss/Open Pie Chart
            fig_pie = px.pie(
                names=['Won', 'Lost', 'Open'],
                values=[data.won_total, data.lost_total, data.total_open],
                color_discrete_sequence=['#2ecc71', '#e74c3c', '#3498db'],
                title="Trade Outcome Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_right:
            # Long vs Short Performance
            fig_ls = go.Figure(data=[
                go.Bar(name='Long', x=['Total', 'Won', 'Lost'], y=[data.long_total, data.long_won, data.long_lost]),
                go.Bar(name='Short', x=['Total', 'Won', 'Lost'], y=[data.short_total, data.short_won, data.short_lost])
            ])
            fig_ls.update_layout(title="Long vs Short Trade Counts", barmode='group')
            st.plotly_chart(fig_ls, use_container_width=True)

    with tab2:
        # PnL Comparison Bar Chart
        pnl_cols = st.columns(2)

        with pnl_cols[0]:
            fig_pnl = go.Figure()
            fig_pnl.add_trace(go.Bar(
                x=['Total Won PnL', 'Total Lost PnL', 'Net PnL'],
                y=[data.won_pnl_total, data.lost_pnl_total, data.pnl_net_total],
                marker_color=['#2ecc71', '#e74c3c', '#f1c40f']
            ))
            fig_pnl.update_layout(title="PnL Breakdown ($)")
            st.plotly_chart(fig_pnl, use_container_width=True)

        with pnl_cols[1]:
            # Average PnL per Side
            fig_avg_pnl = go.Figure(data=[
                go.Bar(name='Long PnL Avg', x=['All', 'Won', 'Lost'],
                       y=[data.long_pnl_average, data.long_pnl_won_average, data.long_pnl_lost_average]),
                go.Bar(name='Short PnL Avg', x=['All', 'Won', 'Lost'],
                       y=[data.short_pnl_average, data.short_pnl_won_average, data.short_pnl_lost_average])
            ])
            fig_avg_pnl.update_layout(title="Average PnL by Direction", barmode='group')
            st.plotly_chart(fig_avg_pnl, use_container_width=True)

    with tab3:
        # Length/Duration Analysis
        st.subheader("Trade Duration (Bars/Time)")
        len_cols = st.columns(2)

        with len_cols[0]:
            fig_len = go.Figure()
            fig_len.add_trace(go.Bar(
                x=['Average', 'Max', 'Min'],
                y=[data.len_average, data.len_max, data.len_min],
                name="Overall Length"
            ))
            fig_len.update_layout(title="Trade Length Stats (Total)")
            st.plotly_chart(fig_len, use_container_width=True)

        with len_cols[1]:
            fig_len_wl = go.Figure(data=[
                go.Bar(name='Won Trades', x=['Avg', 'Max', 'Min'],
                       y=[data.len_won_average, data.len_won_max, data.len_won_min]),
                go.Bar(name='Lost Trades', x=['Avg', 'Max', 'Min'],
                       y=[data.len_lost_average, data.len_lost_max, data.len_lost_min])
            ])
            fig_len_wl.update_layout(title="Trade Length: Won vs Lost", barmode='group')
            st.plotly_chart(fig_len_wl, use_container_width=True)

    st.divider()

    st.header("📈 Draw Down Analysis")
    drawdown_cols = st.columns(4)
    drawdown_cols[0].metric("Money Down",round(draw_down_analysis.moneydown,2))
    drawdown_cols[1].metric("Draw Down Length",draw_down_analysis.len_)
    drawdown_cols[2].metric("Max Money Down",round(draw_down_analysis.max_moneydown,2))
    drawdown_cols[3].metric("Max Draw Down Length",draw_down_analysis.max_len)



    st.header("📈 Time Return Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Months", len(time_return_analysis))
    col2.metric("Positive Months", len([i for i in time_return_analysis if i.is_positive]))
    col3.metric("Negative Months", len([i for i in time_return_analysis if i.is_negative]))

    st.divider()
    st.header("📈 Show Trades")
    if st.button("Show"):
        cerebro_plots = state.backtrader_vm.get_cerebro_plot_fig()
        if cerebro_plots is not None:
            for fig_group in cerebro_plots:
                for fig in fig_group:
                    st.pyplot(fig)
        else:
            st.info("There is No Plots for plotting !!!")

else:
    st.info("Run the strategy to see the analysis.")
