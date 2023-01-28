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

Here are dataset-specific notebooks exploring data for daily and intraday frequencies. 

### 2.1) Equity Market Data:
These datasets contain the actual stock movement data.

| Dataset                                                                           | Description                                   |
|-----------------------------------------------------------------------------------|-----------------------------------------------|
| BasicOHLCDaily                                                                    | |
| [BasicAdjustedOHLCDaily](./eda/dataset_eda/basic_adjusted_ohlc_daily.ipynb)       | |
| [PrimaryOHLCDaily](./eda/dataset_eda/primary_ohlc_daily.ipynb)                    | |
| [PrimaryAdjustedOHLCDaily](./eda/dataset_eda/primary_adj_ohlc_daily.ipynb)        | |
| StandardOHLCDaily                                                                 | |
| [StandardAdjustedOHLCDaily](./eda/dataset_eda/standard_adjusted_ohlc_daily.ipynb) | |
| TradeAndQuote                                                                     | |
| [TradeAndQuoteMinuteBar](./Intraday_Data_Intro.ipynb)                             | |
| TradeAndQuoteMinuteBarExcludingTRF                                                | |
| TradeOnly                                                                         | |
| TradeOnlyAdjusted                                                                 | |
| TradeOnlyAdjustedMinuteBar                                                        | |
| TradeOnlyAdjustedMinuteBarBBG                                                     | |
| TradeOnlyAdjustedMinuteBarExcludingTRF                                            | |
| TradeOnlyMinuteBar                                                                | |
| TradeOnlyMinuteBarBBG                                                             | |
| TradeOnlyMinuteBarExcludingTRF                                                    | |

### 2.2) Equity Reference Data:
These datasets provide more information about the securities and the Equity datasets.

| [Dataset](./eda/dataset_eda/README.md)                              | Description                                                             |
|---------------------------------------------------------------------|-------------------------------------------------------------------------|
| [BasicAdjustments](./eda/dataset_eda/basic_adjustments.ipynb)       | |
| [DetailedAdjustments](./eda/dataset_eda/detailed_adjustments.ipynb) |                                                        |
| [LookupBase](./eda/dataset_eda/lookupBase.ipynb)                    | |
| [SecMasterBase](./eda/dataset_eda/sec_master_base.ipynb)            | |

## 3) Data Access
There are currently two different ways to access the data: using the AlgoSeek SDK or using Boto3. There are notebooks 
for both methods here, but you should start with the introductions for both.

## 4) Time Series Analysis


## 5) Getting Started with Machine Learning

### 5.1) [ML Preprocessing](./ml/preprocessing/README.md)

### 5.2) [Popular Libraries](./ml/library_intro/README.md)
Introductions to using AlgoSeek datasets with several popular libraries


### 5.3) [ML Models](./ml/README.md)
Some sample machine learning models to get you started 

| Model                                                            | Frequency | Description         |
|------------------------------------------------------------------|-----------|---------------------|
| [Keras Univariate LSTM](./ml/intraday_keras_lstm_univariate.ipynb) | Intraday  | Intraday Regression |
| [Linear Regression](./ml/intraday_linear_regression.ipynb)         | Intraday  |                     |
| [LightGBM Regression](./ml/intraday_lightgbm.ipynb)                | Intraday |                     |
| [Random Forest Regressor](./ml/intraday_random_forests.ipynb)      | Intraday |                     |
| XGBoost                                                          | Intraday |                     |

### 5.4) [MLOps Framework](./ml/mlflow/README.md)

| Model                 | Frequency | Description                                      |
|-----------------------|-----------|--------------------------------------------------|
| LightGBM Regressor | Intraday | [Link](ml/mlflow/lightgbm/ | 


## 5) Strategies

| Strategy | Frequency | Description |
|----------|-----------|-------------|


