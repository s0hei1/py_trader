import pandas as pd
from functools import reduce
import numpy as np

def _combineFilters(filter1, filter2):
    return filter1 & filter2


def filterGeneration( df: pd.DataFrame, collumnAndFilterList: dict):
    filtersToApply = []

    for column in collumnAndFilterList:
        filtersList = collumnAndFilterList[column]

        if filtersList:
            filtersToApply.append(df[column].isin(filtersList))

    if filtersToApply:
        filtersToApply = reduce(_combineFilters, filtersToApply)
        return filtersToApply

    return np.ones(len(df), dtype=bool)

