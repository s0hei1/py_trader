import pandas as pd
from apps.stremlit_ui.datasource.api_clients.market_data_client.api_client import MarketDataAPIClient
import streamlit as st
from typing import Callable,List
from apps.stremlit_ui.datasource.api_clients.market_data_client.client_models import ReadManyCandlesRequest, CandleModel


def candles_browser_view(
        api_client: MarketDataAPIClient,
        *,
        on_fetch_candles : Callable[[List[CandleModel] | pd.DataFrame], None] | None = None,
        show_candles : bool = True,
        header_divider : bool = False,
):
    st.header("Data Browser",divider=header_divider)

    try:
        brokers = api_client.get_brokers()
        symbols = api_client.get_symbols()
        tfs = api_client.get_time_frames()
    except Exception as e:
        st.error(f"Failed fetching filters: {e}")
        st.stop()

    broker_map = {b.name: b.id for b in brokers}
    symbol_map = {s.name: s.id for s in symbols}
    tf_map = {t.name: t.id for t in tfs}

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_broker = st.selectbox("Broker", list(broker_map.keys()))

    with col2:
        selected_symbol = st.selectbox("Symbol", list(symbol_map.keys()))

    with col3:
        selected_tf = st.selectbox("Time Frame", list(tf_map.keys()))

    if st.button("Load Candles"):
        try:
            req = ReadManyCandlesRequest(
                time_frame_id=tf_map[selected_tf],
                broker_id=broker_map[selected_broker],
                symbol_id=symbol_map[selected_symbol]
            )

            df = api_client.get_candles(req, to_dataframe=True)
            on_fetch_candles(df)
            df = df.rename(
                columns={
                    'open_': 'open'
                }
            )


            if df.empty:
                st.warning("No candles found.")
            else:
                if show_candles:
                    st.subheader("Candles Table")
                    st.dataframe(df)
                else:
                    st.success("Candles fetched successfully.")

        except Exception as e:
            st.error(f"Failed loading candles: {e}")
