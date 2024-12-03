import os
from os.path import abspath

from dotenv import load_dotenv


load_dotenv(abspath('.env'))

BASE_COIN = os.getenv('BASE_COIN').upper()
QUOTE_COIN = os.getenv('QUOTE_COIN').upper()
INTERVAL = str(os.getenv('INTERVAL'))

BASE_CUSTOM_EXCESS = 20
QUOTE_CUSTOM_EXCESS = 20