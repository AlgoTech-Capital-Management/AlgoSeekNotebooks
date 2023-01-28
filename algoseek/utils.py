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
