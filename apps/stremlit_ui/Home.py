import os
from typing import AnyStr
import sys

def get_current_path_parent(path: AnyStr, depth=1):
    if depth == 0:
        return path
    else:
        path = os.path.dirname(path)
        return get_current_path_parent(path=path, depth=depth - 1)

sys.path.append(get_current_path_parent(path=os.path.abspath(__file__), depth=3))

import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("Welcome to Palaz Bi Demo Application! 👋",)

st.sidebar.success("Select a dashboard above.")

st.markdown(
    """
    This is an example for showing some reports from PALAZ Company
    
    You can select the dashboards on right side and see interactive reports !
    """
)
