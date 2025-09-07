import streamlit as st

cols = st.columns(3)

with cols[0]:
    st.metric("Real Balance", f"100 $")