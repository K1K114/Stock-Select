from tabulate import tabulate
import requests
import yahoo_fin.stock_info as si
from datetime import date
import re
import warnings
from alive_progress import alive_bar
import pandas as pd


a = si.get_quote_table("aapl")
print(a)
