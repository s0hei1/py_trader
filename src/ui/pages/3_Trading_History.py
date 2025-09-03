import streamlit as st
import  pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder

from bi_app.di.provider import Provider
from bi_app.viewmodel.sales_dash_vm import SalesDashVM

st.set_page_config(layout="wide")


def setUpAggridPivot(df : pd.DataFrame, values : str):


    pDF = df.pivot_table(
        index=['productionCode', 'productionName', 'itemName'],
        columns='rollSize',
        values=values,
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    pDF.rename(columns=
    {
        1: '1',2: '2',3: '3',4: '4',5: '5',
        6: '6',7: '7',8: '8',9: '9',10: '10',
        11: '11',12: '12',15: '15',30: '30',
    }, inplace=True)

    # pDF.columns.add_column('2')

    gridOptions = GridOptionsBuilder.from_dataframe(pDF)
    gridOptions.configure_side_bar()
    gridOptions.configure_columns('productionName', rowGroup=True, hide=True, checkboxSelection=True)
    gridOptions.configure_columns('productionCode', hide=True)
    gridOptions.configure_column("itemName", filter=True)

    for i in range(31):
        if str(i) in pDF.columns.to_list():
            gridOptions.configure_columns(str(i), width=20)

    gridOptions = gridOptions.build()

    response = AgGrid(
        pDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
    )

    return response


vm : SalesDashVM = Provider().provideSalesDashVM()

toRoll = st.checkbox("Show to Roll",False)
getInStockColumnName = lambda f : 'rollQty' if f else 'm2Qty'

setUpAggridPivot(vm.df, getInStockColumnName(toRoll))