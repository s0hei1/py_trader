import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, AgGridReturn
import pandas as pd
from src.ui.viewmodel.vm_result import VMResult


def ShowResult(result : VMResult):
    if result.has_error:
        st.error(result.message)
    else:
        st.success(result.message)

def StaticAgGrid(df : pd.DataFrame, use_checkbox : bool = False) -> AgGridReturn:
    grid_options = GridOptionsBuilder.from_dataframe(df)
    grid_options.configure_selection(use_checkbox=use_checkbox)

    response : AgGridReturn = AgGrid(
        data=df,
        height=240,
        gridOptions=grid_options.build()
    )

    return response