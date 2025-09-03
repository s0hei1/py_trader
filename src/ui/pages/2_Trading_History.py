import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode

from bi_app.di.provider import Provider
from bi_app.viewmodel.planning_dash_vm import PlanningDashVM

st.set_page_config(layout="wide")


def setUpProductionCodeAndNameAggrid(vm : PlanningDashVM):

    pCodeAndNamesDF = vm.getProductionCodeAndNames()
    gridOptions = GridOptionsBuilder.from_dataframe(pCodeAndNamesDF)
    gridOptions.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions.configure_columns('productionCode', filter = True)
    gridOptions = gridOptions.build()

    response = AgGrid(
        pCodeAndNamesDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
        height=250
    )
    if response['selected_rows'] is not None:
        vm.selectedProductionCodes = response['selected_rows']['productionCode'].to_list()
def setUpMoqetsAggrid(vm : PlanningDashVM):

    pCodeAndNamesDF = vm.getMoqets()
    gridOptions = GridOptionsBuilder.from_dataframe(pCodeAndNamesDF)
    gridOptions.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions.configure_columns('palazCode', filter = True)
    gridOptions = gridOptions.build()

    response = AgGrid(
        pCodeAndNamesDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
        height=250
    )
    if response['selected_rows'] is not None:
        vm.selectedMoqets = response['selected_rows']['palazCode'].to_list()
def setUpRollsAggrid(vm : PlanningDashVM):

    pCodeAndNamesDF = vm.getRolls()
    gridOptions = GridOptionsBuilder.from_dataframe(pCodeAndNamesDF)
    gridOptions.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions.configure_columns('rollSize', filter = True)
    gridOptions = gridOptions.build()

    response = AgGrid(
        pCodeAndNamesDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
        height=250
    )
    if response['selected_rows'] is not None:
        vm.selectedRolls = response['selected_rows']['rollSize'].to_list()
def setUpOrdersAggrid(vm : PlanningDashVM):

    pCodeAndNamesDF = vm.getOrders()
    gridOptions = GridOptionsBuilder.from_dataframe(pCodeAndNamesDF)
    gridOptions.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions.configure_columns('orderDocumentNumber', filter = True)
    gridOptions = gridOptions.build()

    response = AgGrid(
        pCodeAndNamesDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
        height=250
    )
    if response['selected_rows'] is not None:
        vm.selectedOrders = response['selected_rows']['orderDocumentNumber'].to_list()
def setUpCustomersAggrid(vm : PlanningDashVM):

    pCodeAndNamesDF = vm.getCustomers()
    gridOptions = GridOptionsBuilder.from_dataframe(pCodeAndNamesDF)
    gridOptions.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions.configure_columns('vendorCode', filter = True)
    gridOptions = gridOptions.build()

    response = AgGrid(
        pCodeAndNamesDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
        height=250
    )
    if response['selected_rows'] is not None:
        vm.selectedCustomers = response['selected_rows']['vendorCode'].to_list()
def setUpDateSeriesAggrid(vm : PlanningDashVM):

    dateSeriesDF = vm.getDateSeries()
    gridOptions = GridOptionsBuilder.from_dataframe(dateSeriesDF)
    gridOptions.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridOptions.configure_columns('jalaliDate', filter = True)
    gridOptions = gridOptions.build()

    response = AgGrid(
        dateSeriesDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
        height=250
    )
    if response['selected_rows'] is not None:
        vm.selectedDate = response['selected_rows']['jalaliDate'].to_list()

def setUpSalesPivotDF(df : pd.DataFrame):

    pDF = df.pivot_table(
        index=['productionCode', 'productionName', 'itemName'],
        columns='rollSize',
        values='rollQty',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    colNames = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '15', '30']

    for col in colNames:
        if col not in pDF.columns.to_list():
            pDF[col] = 0

    pDF = pDF[['productionCode', 'productionName', 'itemName'] + colNames]


    gridOptions = GridOptionsBuilder.from_dataframe(pDF)
    gridOptions.configure_side_bar()
    gridOptions.configure_columns('productionName', rowGroup=True, hide=True, checkboxSelection=True)
    gridOptions.configure_columns('productionCode', hide=True)
    gridOptions.configure_column("itemName", filter=True)

    for i in colNames:
        gridOptions.configure_columns(i, width=10)


    gridOptions = gridOptions.build()

    response = AgGrid(
        pDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
    )

    return pDF, response

def setUpInvAggrid(df : pd.DataFrame):

    pDF = df.pivot_table(
        index=['productionCode', 'productionName', 'itemName'],
        columns='rollSize',
        values='inStockRoll',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    pDF.rename(columns=vm.rollNames, inplace=True)

    colNames = [i for i in vm.rollNames.values()]

    for col in colNames:
        if col not in pDF.columns.to_list():
            pDF[col] = 0

    pDF = pDF[['productionCode', 'productionName', 'itemName'] + colNames]


    gridOptions = GridOptionsBuilder.from_dataframe(pDF)
    gridOptions.configure_side_bar()
    gridOptions.configure_columns('productionName', rowGroup=True, hide=True, checkboxSelection=True)
    gridOptions.configure_columns('productionCode', hide=True)
    gridOptions.configure_column("itemName", filter=True)

    for i in colNames:
        gridOptions.configure_columns(i, width=10)


    gridOptions = gridOptions.build()

    response = AgGrid(
        pDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
    )

    return pDF , response

def setUpAvailableAggrid(dfSales : pd.DataFrame, dfInv : pd.DataFrame, vm : PlanningDashVM):
    pDF = pd.merge(left= dfSales , right= dfInv , on = ['productionCode', 'productionName', 'itemName'] , how = 'outer',suffixes=('_sle', '_inv'))
    pDF.fillna(0, inplace= True)

    for idx, row in pDF.iterrows():
        for j in [i for i in vm.rollNames.values()]:
            pDF.loc[idx, j] = row[f'{j}_inv'] -  row[f'{j}_sle']

    pDF.drop(columns= [f'{i}_inv' for i in vm.rollNames.values()], inplace=True)
    pDF.drop(columns= [f'{i}_sle' for i in vm.rollNames.values()], inplace= True)

    pDF = pDF.replace(0,' ')

    gridOptions = GridOptionsBuilder.from_dataframe(pDF)
    gridOptions.configure_side_bar()
    gridOptions.configure_columns('productionName', rowGroup=True, hide=True, checkboxSelection=True,                                  )
    gridOptions.configure_columns('productionCode', hide=True)
    gridOptions.configure_column("itemName", filter=True)

    for i in [i for i in vm.rollNames.values()]:
        gridOptions.configure_columns(i, width=10)

    gridOptions = gridOptions.build()

    response = AgGrid(
        pDF,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="streamlit",
        enable_enterprise_modules=True,
    )

    return response


cols = st.columns([1.7,0.05, 2 , 0.05 , 1])

vm : PlanningDashVM = Provider().providePlanningDashVM()





with cols[0]:
    setUpProductionCodeAndNameAggrid(vm)
    setUpDateSeriesAggrid(vm)

with cols[2]:
    setUpMoqetsAggrid(vm)
    setUpCustomersAggrid(vm)

with cols[4]:
    setUpRollsAggrid(vm)
    setUpOrdersAggrid(vm)


colsReports = st.columns([1,0.1,1])

with colsReports[0]:
    st.write('Commited')
    pivotDfSales = setUpSalesPivotDF(vm.getSalesReport())[0]



with colsReports[2]:
    st.write('In Stock')
    pivotDFInv = setUpInvAggrid(vm.getInvReport())[0]

st.write('Available')
setUpAvailableAggrid(dfSales= pivotDfSales,dfInv= pivotDFInv, vm = vm)

