# Schemas for AlgoSeek Datasets

import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds

from pyarrow import int64, timestamp, float64, decimal128, string, date32, date64
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.functions import *
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
from pyspark.sql.types import *

primary_adj_schema = pa.schema([
    ("TradeDate", date32()),
    ("SecId", int64()),
    ("Ticker", string()),
    ("Name", string()),
    ("PrimaryExchange", string()),
    ("ISIN", string()),
    ("OpenTime", timestamp('ns', tz='US/Eastern')),
    ("OpenPrice", float64()),
    ("OpenSize", int64()),
    ("HighTime", timestamp('ns', tz='US/Eastern')),
    ("HighPrice", float64()),
    ("LowTime", timestamp('ns', tz='US/Eastern')),
    ("LowPrice", float64()),
    ("CloseTime", timestamp('ns', tz='US/Eastern')),
    ("ClosePrice", float64()),
    ("CloseSize", int64()),
    ("ListedMarketHoursVolume", int64()),
    ("ListedMarketHoursTrades", int64()),
    ("ListedTotalVolume", int64()),
    ("ListedTotalTrades", int64()),
    ("FinraMarketHoursVolume", int64()),
    ("FinraMarketHoursTrades", int64()),
    ("FinraTotalVolume", int64()),
    ("FinraTotalTrades", int64()),
    ("MarketVWAP", float64()),
    ("DailyVWAP", float64()),
    ("PriceAdjFactor", float64()),
    ("VolumeAdjFactor", float64())
])

taq_min_schema = pa.schema([
    ("TradeDate", timestamp('us', tz='US/Eastern')),
    ("BarDateTime", timestamp('us', tz='US/Eastern')),
    ("Ticker", string()),
    ("SecId", int64()),
    ("OpenBarTimeOffset", decimal128(1, 0)),
    ("OpenBidPrice", float64()),
    ("OpenBidSize", int64()),
    ("OpenAskPrice", float64()),
    ("OpenAskSize", int64()),
    ("FirstTradeTimeOffset", decimal128(11, 9)),
    ("FirstTradePrice", float64()),
    ("FirstTradeSize", int64()),
    ("HighBidTimeOffset", decimal128(11, 9)),
    ("HighBidPrice", float64()),
    ("HighBidSize", int64()),
    ("HighAskTimeOffset", decimal128(11, 9)),
    ("HighAskPrice", float64()),
    ("ighAskSize", int64()),
    ("HighTradeTimeOffset", decimal128(11, 9)),
    ("HighTradePrice", float64()),
    ("HighTradeSize", int64()),
    ("LowBidTimeOffset", decimal128(11, 9)),
    ("LowBidPrice", float64()),
    ("LowBidSize", int64()),
    ("LowAskTimeOffset", decimal128(11, 9)),
    ("LowAskPrice", float64()),
    ("LowAskSize", int64()),
    ("LowTradeTimeOffset", decimal128(11, 9)),
    ("LowTradePrice", float64()),
    ("LowTradeSize", int64()),
    ("CloseBarTimeOffset", decimal128(11, 9)),
    ("CloseBidPrice", float64()),
    ("CloseBidSize", int64()),
    ("CloseAskPrice", float64()),
    ("CloseAskSize", int64()),
    ("LastTradeTimeOffset", decimal128(11, 9)),
    ("LastTradePrice", float64()),
    ("LastTradeSize", int64()),
    ("MinSpread", float64()),
    ("MaxSpread", float64()),
    ("CancelSize", int64()),
    ("VolumeWeightPrice", float64()),
    ("NBBOQuoteCount", int64()),
    ("TradeAtBid", int64()),
    ("TradeAtBidMid", int64()),
    ("TradeAtMid", int64()),
    ("TradeAtMidAsk", int64()),
    ("TradeAtAsk", int64()),
    ("TradeAtCrossOrLocked", int64()),
    ("Volume", int64()),
    ("TotalTrades", int64()),
    ("FinraVolume", int64()),
    ("FinraVolumeWeightPrice", float64()),
    ("UptickVolume", int64()),
    ("DowntickVolume", int64()),
    ("RepeatUptickVolume", int64()),
    ("RepeatDowntickVolume", int64()),
    ("UnknownTickVolume", int64()),
    ("TradeToMidVolWeight", float64()),
    ("TradeToMidVolWeightRelative", float64()),
    ("TimeWeightBid", float64()),
    ("TimeWeightAsk", float64())
])

fixed_taq_min = pa.schema([
    ("TradeDate", timestamp('us')),
    ("BarDateTime", timestamp('us')),
    ("Ticker", string()),
    ("OpenBarTimeOffset", float64()),
    ("OpenBidPrice", float64()),
    ("OpenBidSize", int64()),
    ("OpenAskPrice", float64()),
    ("OpenAskSize", int64()),
    ("FirstTradeTimeOffset", float64()),
    ("FirstTradePrice", float64()),
    ("FirstTradeSize", int64()),
    ("HighBidTimeOffset", float64()),
    ("HighBidPrice", float64()),
    ("HighBidSize", int64()),
    ("HighAskTimeOffset", float64()),
    ("HighAskPrice", float64()),
    ("HighAskSize", int64()),
    ("HighTradeTimeOffset", float64()),
    ("HighTradePrice", float64()),
    ("HighTradeSize", int64()),
    ("LowBidTimeOffset", float64()),
    ("LowBidPrice", float64()),
    ("LowBidSize", int64()),
    ("LowAskTimeOffset", float64()),
    ("LowAskPrice", float64()),
    ("LowAskSize", int64()),
    ("LowTradeTimeOffset", float64()),
    ("LowTradePrice", float64()),
    ("LowTradeSize", int64()),
    ("CloseBarTimeOffset", float64()),
    ("CloseBidPrice", float64()),
    ("CloseBidSize", int64()),
    ("CloseAskPrice", float64()),
    ("CloseAskSize", int64()),
    ("LastTradeTimeOffset", float64()),
    ("LastTradePrice", float64()),
    ("LastTradeSize", int64()),
    ("MinSpread", float64()),
    ("MaxSpread", float64()),
    ("CancelSize", int64()),
    ("VolumeWeightPrice", float64()),
    ("NBBOQuoteCount", int64()),
    ("TradeAtBid", int64()),
    ("TradeAtBidMid", int64()),
    ("TradeAtMid", int64()),
    ("TradeAtMidAsk", int64()),
    ("TradeAtAsk", int64()),
    ("TradeAtCrossOrLocked", int64()),
    ("Volume", int64()),
    ("TotalTrades", int64()),
    ("FinraVolume", int64()),
    ("FinraVolumeWeightPrice", float64()),
    ("UptickVolume", int64()),
    ("DowntickVolume", int64()),
    ("RepeatUptickVolume", int64()),
    ("RepeatDowntickVolume", int64()),
    ("UnknownTickVolume", int64()),
    ("TradeToMidVolWeight", float64()),
    ("TradeToMidVolWeightRelative", float64()),
    ("TimeWeightBid", float64()),
    ("TimeWeightAsk", float64())])

taq_1min_schema = StructType([
 StructField("Date", DateType(),False), \
 StructField("Ticker", StringType(),False), \
 StructField("TimeBarStart", TimestampType(),False), \
 StructField("OpenBarTime", TimestampType(),False), \
 StructField("OpenBidPrice", DoubleType(),False), \
 StructField("OpenBidSize", DoubleType(),False), \
 StructField("OpenAskPrice", DoubleType(),False), \
 StructField("OpenAskSize", DoubleType(),False), \
 StructField("FirstTradeTime", TimestampType(),True), \
 StructField("FirstTradePrice", DoubleType(),True), \
 StructField("FirstTradeSize", DoubleType(),True), \
 StructField("HighBidTime", TimestampType(),False), \
 StructField("HighBidPrice", DoubleType(),False), \
 StructField("HighBidSize", DoubleType(),False), \
 StructField("HighAskTime", TimestampType(),False), \
 StructField("HighAskPrice", DoubleType(),False), \
 StructField("HighAskSize", DoubleType(),False), \
 StructField("HighTradeTime", TimestampType(),True), \
 StructField("HighTradePrice", DoubleType(),True), \
 StructField("HighTradeSize", DoubleType(),True), \
 StructField("LowBidTime", TimestampType(),False), \
 StructField("LowBidPrice", DoubleType(),False), \
 StructField("LowBidSize", DoubleType(),False), \
 StructField("LowAskTime", TimestampType(),False), \
 StructField("LowAskPrice", DoubleType(),False), \
 StructField("LowAskSize", DoubleType(),False), \
 StructField("LowTradeTime", TimestampType(),True), \
 StructField("LowTradePrice", DoubleType(),True), \
 StructField("LowTradeSize", DoubleType(),True), \
 StructField("CloseBarTime", TimestampType(),False), \
 StructField("CloseBidPrice", DoubleType(),False), \
 StructField("CloseBidSize", DoubleType(),False), \
 StructField("CloseAskPrice", DoubleType(),False), \
 StructField("CloseAskSize", DoubleType(),False), \
 StructField("LastTradeTime", TimestampType(),True), \
 StructField("LastTradePrice", DoubleType(),True), \
 StructField("LastTradeSize", DoubleType(),True), \
 StructField("MinSpread", DoubleType(),False), \
 StructField("MaxSpread", DoubleType(),False), \
 StructField("CancelSize", DoubleType(),True), \
 StructField("VolumeWeightPrice", DoubleType(),True), \
 StructField("NBBOQuoteCount", DoubleType(),True), \
 StructField("TradeAtBid", DoubleType(),True), \
 StructField("TradeAtBidMid", DoubleType(),True), \
 StructField("TradeAtMid", DoubleType(),True), \
 StructField("TradeAtMidAsk", DoubleType(),True), \
 StructField("TradeAtAsk", DoubleType(),True), \
 StructField("TradeAtCrossOrLocked", DoubleType(),True), \
 StructField("Volume", DoubleType(),True), \
 StructField("TotalTrades", DoubleType(),True), \
 StructField("FinraVolume", DoubleType(),True), \
 StructField("FinraVolumeWeightPrice", DoubleType(),True), \
 StructField("UptickVolume", IntegerType(),True), \
 StructField("DowntickVolume", IntegerType(),True), \
 StructField("RepeatUptickVolume", IntegerType(),True), \
 StructField("RepeatDowntickVolume", IntegerType(),True), \
 StructField("UnknownTickVolume", IntegerType(),True), \
 StructField("TradeToMidVolWeight", IntegerType(),True), \
 StructField("TradeToMidVolWeightRelative", IntegerType(),True), \
 StructField("TimeWeightBid", IntegerType(),True), \
 StructField("TimeWeightAsk", IntegerType(),True)
])