import pandas as pd

from bi_app.tools.date_range import DateRange
from bi_app.warehouse.repository.sales_fact_repository import SalesFactRepository


class SalesDashVM():

    df = None

    selectedProductionCodes = []
    selectedMoqets = []
    selectedRolls = []
    selectedOrders = []
    selectedCustomers = []
    selectedDateRange : DateRange = None


    _productionCodeAndName = None
    _moqets = None
    _rolls = None
    _orders = None
    _customers = None
    _dateSeries = None


    def __init__(self,
                 salesFactRepository : SalesFactRepository):

        self.salesFactRepository = salesFactRepository

        reportQuery = self.salesFactRepository.getReport()
        self.df = pd.read_sql(reportQuery.statement, reportQuery.session.bind)
        self.df['rollSize'] = self.df['rollSize'].apply(lambda x : None if pd.isna(x) else int(x))


        self._moqets = self.df[['itemName', 'palazCode']].drop_duplicates().sort_values('palazCode')

        self._productionCodeAndName = (self.df[['productionCode', 'productionName']]
                                       .drop_duplicates().reset_index(drop=True)).sort_values(by='productionCode')
        self._rolls = self.df[['rollSize']].drop_duplicates().reset_index(drop=True).sort_values(by='rollSize')

        self._orders = self.df[['orderDocumentNumber']].drop_duplicates().reset_index(drop=True).sort_values(by='orderDocumentNumber')

        self._customers =self.df[['vendorCode', 'vendorName']].drop_duplicates().reset_index(drop=True).sort_values(by='vendorCode')

        self._dateSeries = self.df[['jalaliDate']].drop_duplicates().reset_index(drop=True).sort_values(by='jalaliDate')



    def getSalesReport(self):
        filterItemName = self.df['palazCode'].isin(self.selectedMoqets) if self.selectedMoqets else ~self.df[True == True].isna()

        return self.df[filterItemName]