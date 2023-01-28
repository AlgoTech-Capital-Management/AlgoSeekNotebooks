"""
Dataset handling Functions
"""
import pandas as pd
import algoseek_connector
import algoseek_connector.functions as fn
from dotenv import load_dotenv
from tqdm import tqdm
import os
import requests
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# Data Download
def download_sec_master(session):
    resource = algoseek_connector.DataResource(session)
    sec_master_base = resource.datagroups.USEquityReferenceData.datasets.SecMasterBase
    sec_df = sec_master_base.select(sec_master_base.SecId,
                       sec_master_base.ListStatus,
                       sec_master_base.SecurityDescription,
                       sec_master_base.Sic,
                       sec_master_base.Sector,
                       sec_master_base.Industry,
                       sec_master_base.SEDOL,
                       sec_master_base.Ticker,
                       sec_master_base.TickerStartToEndDate,
                       sec_master_base.Name,
                       sec_master_base.NameStartToEndDate,
                       sec_master_base.ISIN,
                       sec_master_base.ISINStartToEndDate,
                       sec_master_base.USIdentifier,
                       sec_master_base.USIdentifierStartToEndDate,
                       sec_master_base.PrimaryExchange,
                       sec_master_base.PrimaryExchangeStartToEndDate,
                       sec_master_base.FIGI).fetch()
    sec_df.to_parquet('data/us_equity/reference/sec_master.parquet')
    print('SEC Master file Successfully Downloaded!')
def download_lookup_base(session):
    resource = algoseek_connector.DataResource(session)
    lookup_base = resource.datagroups.USEquityReferenceData.datasets.LookupBase
    look_df = lookup_base.select(lookup_base.SecId,
                                 lookup_base.Ticker,
                                 lookup_base.StartDate,
                                 lookup_base.EndDate
                                 ).fetch()
    look_df.to_parquet('data/us_equity/reference/lookup_base.parquet')
    print('Lookup Base Successfully Downloaded!')
def download_basic_adjustment_factors(session):
    resource = algoseek_connector.DataResource(session)
    basic_adj = resource.datagroups.USEquityReferenceData.datasets.BasicAdjustmentFactors
    basic_df = basic_adj.select(basic_adj.SecId,
                                basic_adj.Ticker,
                                basic_adj.EffectiveDate,
                                basic_adj.AdjustmentFactor,
                                basic_adj.AdjustmentReason,
                                basic_adj.EventId
                                ).fetch()
    basic_df.to_parquet('data/us_equity/reference/basic_adj.parquet')

def download_detailed_adjustment_factors(session):
    resource = algoseek_connector.DataResource(session)
    detailed_adj = resource.datagroups.USEquityReferenceData.datasets.DetailedAdjustmentFactors
    det_df = detailed_adj.select(detailed_adj.SecId,
                                 detailed_adj.Ticker,
                                 detailed_adj.Name,
                                 detailed_adj.ISIN,
                                 detailed_adj.EffectiveDate,
                                 detailed_adj.ReportDate,
                                 detailed_adj.Revision,
                                 detailed_adj.AdjustmentFactor,
                                 detailed_adj.AdjustmentReason,
                                 detailed_adj.EventType,
                                 detailed_adj.EventId,
                                 detailed_adj.DivPayrate,
                                 detailed_adj.DivCurrency,
                                 detailed_adj.DivPaymentType,
                                 detailed_adj.Detail
                                 ).fetch()
    det_df.to_parquet('data/us_equity/reference/detailed_adj.parquet')

def download_basic_adj_ohlc_daily(stocks, session):
    """

    :param stocks: tickers to fetch
    :type stocks: array or list
    :param session:
    :type session: AlgoSeeK Connector Session
    :return:
    :rtype:
    """
    resource = algoseek_connector.DataResource(session)
    basic_adj_ohlc_daily = resource.datagroups.USEquityMarketData.datasets.BasicAdjustedOHLCDaily
    for stock in tqdm(stocks):
        stock_df = basic_adj_ohlc_daily.select(
                   basic_adj_ohlc_daily.TradeDate,
                   basic_adj_ohlc_daily.SecId,
                   basic_adj_ohlc_daily.Ticker,
                   basic_adj_ohlc_daily.OpenPrice,
                   basic_adj_ohlc_daily.HighPrice,
                   basic_adj_ohlc_daily.LowPrice,
                   basic_adj_ohlc_daily.ClosePrice,
                   basic_adj_ohlc_daily.MarketHoursVolume,
                   basic_adj_ohlc_daily.MarketVWAP,
                   basic_adj_ohlc_daily.PriceAdjFactor,
                   basic_adj_ohlc_daily.VolumeAdjFactor
            ).filter(
                    (basic_adj_ohlc_daily.Ticker == stock)
            ).fetch()
        print('{stock} done downloading.'.format(stock=stock))
        stock_df.to_parquet('data/us_equity/basic_adj_ohlc/{stock}.parquet'.format(stock=stock))
        print('{stock} saved'.format(stock=stock))

    print('Finished downloading stock data.')


# Data Loaders
def load_reference_data():
    """

    :return: basic_adjustments, detailed_adjustments, Lookup_base, sec_master
    :rtype: dataframes
    """
    try:
        basic_adj = pd.read_parquet('../../data/us_equity/reference/basic_adj.parquet')
        detailed_adj = pd.read_parquet('../../data/us_equity/reference/detailed_adj.parquet')
        lookup = pd.read_parquet('../../data/us_equity/reference/lookup_base.parquet')
        sec_master = pd.read_parquet('../../data/us_equity/reference/sec_master.parquet')

    except:
        # throw error if a file is missing
        print('Make sure you have downloaded all US Equity Reference Files')

    return basic_adj, detailed_adj, lookup, sec_master



#############
# Dataset handling classes
#############

class SecMasterBase():
    """

    """
    def __init__(self, session=None):
        self.session = session

    def _load_dataset(self, datapath):
        # load local file
        pass

    def download_dataset(self, save_path):
        # download dataset
        pass

    def get_companies_by_sector(self, sector):
        # fetch all companies in sector
        pass

    def get_companies_by_sic(self, sic):
        # fetch all companies by Sector Identifier Code (SIC)
        pass


class TAQMinuteBar():
    """

    args:
        session - AlgoSeek Connector Session

    """

    def __init__(self, session=None, datadir):
        self.datadir = datadir
        self.session = session
        self._dataset = None
    def _load_dataset(self,datadir):
        """

        :param datadir:
        :return:
        """
        _dataset = ds.dataset(datadir+'/us_equity/taq_min',format="parquet")
        self._dataset = _dataset
        return _dataset
    def download_single_ticker(self, ticker, fields=None):
        """

        :param ticker:
        :param fields:
        :return:
        """
        pass

    def download_multiple_tickers(self, ticker_list, fields=None):
        """

        :param ticker_list:
        :param fields:
        :return:
        """
        pass
    def list_instruments(self):
        """
        """
        pass
    def get_fields(self):
        """

        :return:
        """
        pass

class DailyMarketData():
    """
    Class for all daily frequency pricing datasets from AlgoSeek. These are:
        PrimaryExchangeDailyOHLC
        StandardDailyOHLC
        StandardAdjustedDailyOHLC
        BloombergAdjustedDailyOHLC

    """

    def __init__(self, session=None, dataset=None):
        self.session = session
        self.dataset = dataset



class ParquetDataHandler():
    """

    """

    def __init__(self, datadir: Path) -> None:
        self._datadir = datadir


