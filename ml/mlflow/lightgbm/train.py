from pprint import pprint

import lightgbm as lgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

import mlflow
import mlflow.lightgbm

from utils import fetch_logged_data
from utils import *
import pandas as pd

data_store = 'data/intraday.h5'
results_store = 'data/results/lightgbm_intraday.h5'
model_path = Path('models/intraday/gradient_boosting/')

if not model_path.exists():
    model_path.mkdir(parents=True)

try:
    os.mkdir('data/results')
    os.mkdir('data/results/lightgbm_intraday')
except:
    pass
# Cross-Validation Setup
DAY = 390   # number of minute bars in a trading day of 6.5 hrs (9:30 - 15:59)
MONTH = 21  # trading days

def main():
    # prepare example dataset
    # X, y = load_iris(return_X_y=True, as_frame=True)
    features = pd.read_parquet('features.parquet')
    taq = pd.read_parquet('combined_taq.parquet')
    data = pd.merge(taq, features,left_index=True,right_index=True)
    data = data.drop(columns=['TradeDate', 'OpenBarTimeOffset', 'FirstTradeTimeOffset', 'HighBidTimeOffset', 'HighAskTimeOffset', 'HighTradeTimeOffset', 'LowBidTimeOffset', 'LowAskTimeOffset', 'LowTradeTimeOffset', 'CloseBarTimeOffset', 'CloseAskPrice', 'LastTradeTimeOffset'])
    data.rename(columns={'Stochastic_RSI_%K': 'stoch_rsi_k', 'Stochastic_RSI_%K_Default': 'stoch_rsi_k_default',
                         'Stochastic_RSI_%D_Default': 'stoch_rsi_d_default',
                         'Stochastic_RSI_%D': 'stoch_rsi_d',
                         'MACD(12,26)': 'macd_12_26',
                         'MACD(12,26)signal': 'macd_12_26_s',
                         'MACD(12,26)histogram': 'macd_12_26_h'}, inplace=True)
    # Categorical Variables
    data['stock_id'] = pd.factorize(data.index.get_level_values('Ticker'), sort=True)[0]
    categoricals = ['stock_id']
    # X = data.drop(columns='fwd1min')
    # y = data['fwd1min']
    # X_train, X_test, y_train, y_test = train_test_split(X, y)

    label = sorted(data.filter(like='fwd').columns)
    features = data.columns.difference(label).tolist()
    label = label[0]

    params = dict(objective='regression',
                  metric=['rmse'],
                  device='cpu',
                  max_bin=63,
                  gpu_use_dp=False,
                  num_leaves=16,
                  min_data_in_leaf=500,
                  feature_fraction=.8,
                  verbose=-1)
    num_boost_round = 400

    cv = get_cv(n_splits=23)  # we have enough data for 23 different test periods

    # enable auto logging
    # this includes lightgbm.sklearn estimators
    mlflow.lightgbm.autolog()

    start = time()
    for fold, (train_idx, test_idx) in enumerate(cv.split(X=data), 1):
        # create lgb train set
        train_set = data.iloc[train_idx, :]
        lgb_train = lgb.Dataset(data=train_set.drop(label, axis=1),
                                label=train_set[label],
                                categorical_feature=categoricals)

        # create lgb test set
        test_set = data.iloc[test_idx, :]
        lgb_test = lgb.Dataset(data=test_set.drop(label, axis=1),
                               label=test_set[label],
                               categorical_feature=categoricals,
                               reference=lgb_train)

        # train model
        evals_result = {}
        model = lgb.train(params=params,
                          train_set=lgb_train,
                          valid_sets=[lgb_train, lgb_test],
                          feval=ic_lgbm,
                          num_boost_round=num_boost_round,
                          evals_result=evals_result,
                          verbose_eval=50)
        model.save_model((model_path / f'{fold:02}.txt').as_posix())
        print('model saved')
        # get train/valid ic scores
        scores = get_scores(evals_result)

        #    scores.to_hdf(result_store, f'ic/{fold:02}')
        scores.to_hdf(results_store, f'ic/{fold:02}')
        print('scores saved')
        # get feature importance
        fi = get_fi(model)
        #    fi.to_hdf(result_store, f'fi/{fold:02}')
        fi.to_hdf(results_store, f'fi/{fold:02}')
        print('fi saved')
        # generate validation predictions
        X_test = test_set.loc[:, model.feature_name()]
        y_test = test_set.loc[:, [label]]
        y_test['pred'] = model.predict(X_test)
        #    y_test.to_hdf(result_store, f'predictions/{fold:02}')
        # y_test.to_hdf(results_store, f'predictions/{fold:02}')
        y_test.to_parquet(f'data/results/lightgbm_intraday/intraday_predictions_{fold:02}.parquet')
        print('y-test saved')
        # compute average IC per minute
        by_minute = y_test.groupby(test_set.index.get_level_values('BarDateTime'))
        daily_ic = by_minute.apply(lambda x: spearmanr(x[label], x.pred)[0]).mean()
        # print(f'\nFold: {fold:02} | {format_time(time() - start)} | IC per minute: {daily_ic:.2%}\n')

    # regressor = lgb.LGBMClassifier(n_estimators=20, reg_lambda=1.0)
    # regressor.fit(X_train, y_train, eval_set=[(X_test, y_test)])
    # y_pred = regressor.predict(X_test)
    # f1 = f1_score(y_test, y_pred, average="micro")
    run_id = mlflow.last_active_run().info.run_id
    # print("Logged data and model in run {}".format(run_id))

    # show logged data
    for key, data in fetch_logged_data(run_id).items():
        print("\n---------- logged {} ----------".format(key))
        pprint(data)


if __name__ == "__main__":
    main()