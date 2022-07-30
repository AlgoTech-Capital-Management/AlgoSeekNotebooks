 # Algorithmic Trading with Python and AlgoSeek on AWS

## Introduction
This is a collection of notebooks, recipes, and scripts demonstrating how to use AlgoSeek as a data provider 
for Quantitative Finance, Algorithmic Trading, and Machine Learning. There are samples covering everything from 
data ingestion (real-time and batch), stock/universe selection, backtesting, and feature engineering. Additionally, 
there are examples showing how to manipulate financial data with AWS EMR, PySpark, and AWS Sagemaker for end-to-end ML 
pipelines and intraday strategy research.

## 1) Overview 
The notebooks in the root of this repo are the starting point. These are the broad introductions to sections detailed in
the notebooks portion. The rest of the subdirectories are as follows

| Directory | Description                                    |
|-----------|------------------------------------------------|
| [algoseek](./algoseek/)  | Library for algoseek-specific functions        |
| [data](./data/) | data folder (gitignored but created in first notebook |
| [Datasets](./datasets/)  | Samples and descriptions of AlgoSeeks Datasets |
| [eda](./eda/) | Exploratory Data Analysis and Data Visualizations | 
| [integrations](./integrations/) | Using AlgoSeek with external data sources |
| [ML](./ml/)        | Machine Learning Scripts | 
| [Notebooks](./notebooks/) | Miscellaneous Notebooks | 
| [Strategies](./strategies/) | Trading Strategies |
| [WIP](./wip/) | Work In Progress Notebooks | 


## 2) AlgoSeek Datasets

Equity Market Data:

| Dataset                                | Description                                         |
|----------------------------------------|-----------------------------------------------------|
| BasicOHLCDaily                         | |
| BasicAdjustedOHLCDaily                 | [Link](./eda/dataset_eda/basic_adjusted_ohlc_daily.ipynb) |
| PrimaryOHLCDaily                       | [Link](./eda/dataset_eda/primary_ohlc_daily.ipynb) |
| PrimaryAdjustedOHLCDaily               | |
| StandardOHLCDaily                      | |
| StandardAdjustedOHLCDaily              | [Link](./eda/dataset_eda/standard_adjusted_ohlc_daily.ipynb) |
| TradeAndQuote                          | |
| TradeAndQuoteMinuteBar                 | [Link](./2_Intraday_Data_Intro.ipynb) |
| TradeAndQuoteMinuteBarExcludingTRF     | |
| TradeOnly                              | |
| TradeOnlyAdjusted                      | |
| TradeOnlyAdjustedMinuteBar             | |
| TradeOnlyAdjustedMinuteBarBBG          | |
| TradeOnlyAdjustedMinuteBarExcludingTRF | |
| TradeOnlyMinuteBar | |
| TradeOnlyMinuteBarBBG | |
| TradeOnlyMinuteBarExcludingTRF | |

Equity Reference Data:

| Dataset | Description                                                                   |
|---------|-------------------------------------------------------------------------------|
| BasicAdjustments |  [Link](./eda/dataset_eda/basic_adjustments.ipynb)                                                                             |
| DetailedAdjustments | [Link](./eda/dataset_eda/detailed_adjustments.ipynb)                                                                 |
| LookupBase | |
| SecMasterBase | [Link](./eda/dataset_eda/sec_master_base.ipynb) |

## 3) Data Access
There are currently two different ways to access the data: using the AlgoSeek SDK or using Boto3. There a notebooks 
for both methods here, which are denoted in the file names.

## 4) [ML Models](./ml/README.md)

| Model                 | Frequency | Description                                     |
|-----------------------|-----------|-------------------------------------------------|
| Keras Univariate LSTM | Intraday  | [Link](ml/intraday_keras_lstm_univariate.ipynb) |
| Linear Regression     | Intraday  | [Link](ml/intraday_linear_regression.ipynb) |
| LightGBM Regression | Intraday | [Link](ml/intraday_lightgbm.ipynb) |
| XGBoost | Intraday | |
