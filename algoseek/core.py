# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from multiprocessing import cpu_count, Pool
from pathlib import Path
from time import perf_counter
from typing import List, Tuple
from warnings import simplefilter

import pandas as pd
from numpy import log10 as npLog10
from numpy import ndarray as npNdarray
from pandas.core.base import PandasObject

df = pd.DataFrame()

class BasePandasObject(PandasObject):
    """

    """

    def __init__(self, df, **kwargs):
        if df.empty: return
        if len(df.columns) > 0:
            common_names = {
                "Date": "date",
                "Time": "time",
                "Timestamp": "timestamp",
                "Datetime": "datetime",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
                "Dividends": "dividends",
                "Stock Splits": "split",
            }
            # Preemptively drop the rows that are all NaNs
            # Might need to be moved to AnalysisIndicators.__call__() to be
            #   toggleable via kwargs.
            # df.dropna(axis=0, inplace=True)
            # Preemptively rename columns to lowercase
            df.rename(columns=common_names, errors="ignore", inplace=True)

            # Preemptively lowercase the index
            index_name = df.index.name
            if index_name is not None:
                df.index.rename(index_name.lower(), inplace=True)

            self._df = df
        else:
            raise AttributeError(f"[X] No columns!")

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()

@pd.api.extensions.register_dataframe_accessor("algoseek")
class AlgoSeekDataset():
    """

    """
    def __init__(self,pandas_obj):
        self._validate(pandas_obj)
        self._df = pandas_obj

    @staticmethod
    def _validate(obj):
        if "SecId" not in obj.columns or "TradeDate" not in obj.columns:
            raise AttributeError("Must have 'SecId' and 'TradeDate'.")

    @property
    def secid(self):
        # test
        secid = self._df.SecId
        return(secid)

    def plot(self):
        pass