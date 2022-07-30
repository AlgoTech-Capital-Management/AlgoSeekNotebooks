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

def load_credentials(host_var='host_julian',user_var='user_julian',pass_var='password_julian'):
    """

    :param host_var: host variable name in env file
    :type host_var:
    :param user_var: user variable name in env file
    :type user_var:
    :param pass_var: password variable name in env file
    :type pass_var:
    :return: host, user, password
    :rtype:
    """

    load_dotenv('../../.env')
    host = os.getenv(host_var)
    user = os.getenv(user_var)
    password = os.getenv(pass_var)
    return host, user, password

def get_session():
    host, user, password = load_credentials()
    session = algoseek_connector.Session(host,user,password)
    return session

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

