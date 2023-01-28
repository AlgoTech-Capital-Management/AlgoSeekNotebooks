##########################################################
# Data Download Script
##########################################################

import os
import ta
import sys
import json
import math
import pickle
import random
import requests
import collections
import numpy as np
from os import walk
import pandas as pd
import yfinance as yf
import datetime as dt
from tqdm import tqdm
from scipy.stats import linregress
from datetime import datetime, timedelta
from feature_generator import TAEngine
import warnings
import algoseek_connector
import pyarrow as pa
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

warnings.filterwarnings("ignore")

