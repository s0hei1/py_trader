from pprint import pformat

import pandas as pd
from bi_app.viewmodel.vm_helper_functios import filterGeneration
from bi_app.warehouse.repository.moqet_inventory_fact import MoqetInventoryFactRepository
from bi_app.warehouse.repository.sales_fact_repository import SalesFactRepository


class PlanningDashVM():

    dfSalesOriginal = None
    dfInvOriginal = None

    dfFilteredSales = None
    dfSales = None


    rollNames = {
        1: '1', 2: '2', 3: '3', 4: '4', 5: '5',
        6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: '11', 12: '12', 15: '15', 30: '30',
    }

    selectedProductionCodes = []
    selectedMoqets = []
    selectedRolls= []
    selectedOrders = []
    selectedCustomers = []
    selectedDate = []

    _productionCodeAndName = None
    _moqets = None
    _rolls = None
    _orders = None
    _customers = None
    _dateSeries = None

    def __init__(self,
                 salesFactRepository: SalesFactRepository,
                 moqetInvFactRepository: MoqetInventoryFactRepository
                 ):

        qSales = salesFactRepository.getReport()
        qInv = moqetInvFactRepository.getMoqetInventoryReport()

        self.dfInvOriginal = pd.read_sql(qInv.statement, qInv.session.bind)
        self.dfSalesOriginal = pd.read_sql(qSales.statement, qSales.session.bind)
        self.dfFilteredSales = self.dfSalesOriginal.copy()


        self.dfSalesOriginal['rollSize'] = self.dfSalesOriginal['rollSize'].astype(str)


        self._moqets = self.dfSalesOriginal[['itemName', 'palazCode', 'productionCode']].drop_duplicates().sort_values('palazCode').copy()

        self._productionCodeAndName = (self.dfSalesOriginal[['productionCode', 'productionName']]
                                       .drop_duplicates().reset_index(drop=True)).sort_values(by='productionCode')
        self._rolls = self.dfInvOriginal[['rollSize']].astype(str).drop_duplicates().reset_index(drop=True).sort_values(by='rollSize', key =lambda x: x.astype(int))
        self._orders = self.dfSalesOriginal[['orderDocumentNumber', 'vendorCode', 'jalaliDate']].drop_duplicates().reset_index(drop=True).sort_values(
            by='orderDocumentNumber')
        self._customers = self.dfSalesOriginal[['vendorCode', 'vendorName','orderDocumentNumber','jalaliDate']].drop_duplicates()
        self._dateSeries = self.dfSalesOriginal[['jalaliDate']].drop_duplicates().reset_index(drop=True).sort_values(
            by='jalaliDate')




    def getProductionCodeAndNames(self):
        return self._productionCodeAndName

    def getMoqets(self):

        colFilter = {'productionCode' : self.selectedProductionCodes }
        filters = filterGeneration(df = self._moqets,collumnAndFilterList = colFilter)
        self._moqets = self._moqets[filters]

        return  self._moqets[['itemName', 'palazCode']]

    def getRolls(self):
        return self._rolls

    def getOrders(self):
        colFilter = {
            'vendorCode' : self.selectedCustomers,
            'jalaliDate' : self.selectedDate
        }
        filters = filterGeneration(df = self._orders,collumnAndFilterList = colFilter)
        self._orders = self._orders[filters]
        return self._orders[['orderDocumentNumber']]

    def getCustomers(self):
        colFilter = {
            'orderDocumentNumber' : self.selectedOrders ,
            'jalaliDate' : self.selectedDate
        }
        filters = filterGeneration(df = self._customers,collumnAndFilterList = colFilter)

        return self._customers[filters].drop(columns=['orderDocumentNumber','jalaliDate']).drop_duplicates().sort_values(by='vendorCode')

    def getDateSeries(self):
        return self._dateSeries


    @property
    def _dfSalesFilters(self):

        columnAndFilterList = {
            'productionCode' : self.selectedProductionCodes,
            'palazCode' : self.selectedMoqets,
            'rollSize' : self.selectedRolls,
            'orderDocumentNumber' : self.selectedOrders,
            'vendorCode' : self.selectedCustomers,
            'jalaliDate' : self.selectedDate,
        }


        return filterGeneration(self.dfSalesOriginal, columnAndFilterList)

    @property
    def _dfInvFilters(self):

        columnAndFilterList = {
            'productionCode' : self.selectedProductionCodes,
            'palazCode' : self.selectedMoqets,
            'rollSize' : self.selectedRolls,
        }
        return filterGeneration(self.dfInvOriginal, columnAndFilterList)

    def getSalesReport(self):
        return self.dfSalesOriginal[self._dfSalesFilters]


    def getInvReport(self):
        if self._dfInvFilters is not None:
            return self.dfInvOriginal[self._dfInvFilters]


        return self.dfInvOriginal
