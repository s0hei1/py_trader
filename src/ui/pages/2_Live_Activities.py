import streamlit as st

cols = st.columns(3)

with cols[0]:
    st.metric("Real Balance", f"100 $")

with cols[1]:
    st.metric("Open Orders", f"1")

with cols[2]:
    st.metric("Open Position", f"0")



