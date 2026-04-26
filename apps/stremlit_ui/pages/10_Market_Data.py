import streamlit as st

from apps.stremlit_ui.datasource.api_clients.market_data_client.api_client import MarketDataAPIClient,market_data_client_factory
from apps.stremlit_ui.datasource.api_clients.market_data_client.client_models import BrokerModel, SymbolModel, TimeFrameModel
from apps.stremlit_ui.pages.shared_views.candles_browser import candles_browser_view

st.set_page_config(
    page_title="Market Data Admin",
    layout="wide",
)

api = MarketDataAPIClient(
    client=market_data_client_factory(),
)

cols = st.columns(3)
with cols[0]:
    st.header("Brokers")

    with st.expander("➕ Create Broker", expanded=False):
        with st.form("create_broker_form"):
            name = st.text_input("Broker Name")
            submitted = st.form_submit_button("Create")

            if submitted:
                if not name.strip():
                    st.error("Name cannot be empty.")
                else:
                    try:
                        created = api.create_broker(BrokerModel(name=name))
                        st.success(f"Broker created with ID {created.id}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    try:
        brokers = api.get_brokers()
        st.dataframe([b.to_dict() for b in brokers])
    except Exception as e:
        st.error(f"Failed loading brokers: {e}")


with cols[1]:
    st.header("Symbols")

    with st.expander("➕ Create Symbol", expanded=False):
        with st.form("create_symbol_form"):
            name = st.text_input("Symbol Name")
            submitted = st.form_submit_button("Create")

            if submitted:
                if not name.strip():
                    st.error("Symbol name cannot be empty.")
                else:
                    try:
                        created = api.create_symbol(SymbolModel(name=name))
                        st.success(f"Symbol created with ID {created.id}")
                    except Exception as e:
                        st.error(f"Error: {e}")


    try:
        symbols = api.get_symbols()
        st.dataframe([s.to_dict() for s in symbols])
    except Exception as e:
        st.error(f"Failed loading symbols: {e}")


with cols[2]:
    st.header("Time Frames")

    with st.expander("➕ Create Time Frame", expanded=False):
        with st.form("create_tf_form"):
            name = st.text_input("TF Name (e.g. 1m, 5m, 1H)")
            resolution = st.number_input("Resolution (minutes)", min_value=1, step=1)
            submitted = st.form_submit_button("Create")

            if submitted:
                if not name.strip():
                    st.error("TF name cannot be empty.")
                else:
                    try:
                        created = api.create_time_frame(TimeFrameModel(name=name, resolution=resolution))
                        st.success(f"Time Frame created with ID {created.id}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    try:
        tfs = api.get_time_frames()
        st.dataframe([{"id": t.id, "name": t.name, "resolution": t.resolution} for t in tfs])
    except Exception as e:
        st.error(f"Failed loading time frames: {e}")


st.divider()

candles_browser_view(api_client=api)