import os
from os.path import abspath

from dotenv import load_dotenv


load_dotenv(abspath('.env'))

BASE_COIN = os.getenv('BASE_COIN')
QUOTE_COIN = os.getenv('QUOTE_COIN')
INTERVAL = os.getenv('INTERVAL')

CUSTOM_EXCESS = 20
