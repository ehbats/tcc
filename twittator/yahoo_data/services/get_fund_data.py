import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import requests
import pprint
load_dotenv()
key = os.environ.get('ALPHA')


class GetFundData:
    def __init__(
            self,
            ticker: str,
            start_date: str,
            end_date: str = datetime.now()
    ):
        # url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=PETR4.SAO&apikey={key}'

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=PETR4.SAO&apikey={key}'
        
        # url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=PETR4&apikey={key}'

        data = requests.get(url)

        json_data = data.json()

        pprint.pprint(json_data)

instance = GetFundData('PETR4.SA', '2020-01-01')