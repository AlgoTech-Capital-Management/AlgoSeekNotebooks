# Logging class for jupyter samples repo
import os
import logging
import pandas as pd

# create logger
logger = logging.getLogger('JupyterSamples')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.FileHandler('logs/daily_download.log')
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
