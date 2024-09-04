from tabulate import tabulate
import requests
import yahoo_fin.stock_info as si
from datetime import date, timedelta
import re
import warnings
from alive_progress import alive_bar

a = (date.today())
n = a - timedelta(weeks=2)

year, month, day = str(a).split("-")
nyear, nmonth, nday = str(n).split("-")

end_date = f"{month}/{day}/{year}"
start_date = f"{nmonth}/{nday}/{nyear}"

print(si.get_data("aapl", start_date=start_date, end_date=end_date))
