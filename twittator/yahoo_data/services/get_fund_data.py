import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import investpy
import os
import requests
import pprint

key = os.environ.get('ALPHA')

class GetFundData:
    def __init__(self, key):
        cash_flow = self.get_cash_flow(key = key, symbol = 'WMT')
        balance_sheet = self.get_balance_sheet(key = key, symbol = 'WMT')
        income_statement = self.get_income_statement(key = key, symbol = 'WMT')
        
    def get_cash_flow(
            self, 
            key: str,
            symbol: str,
            period: str = 'quarterlyReports'
            ):
        data = self.make_request(f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={key}", period)
        return data

    def get_income_statement(
            self,
            key: str,
            symbol: str,
            period: str = 'quarterlyReports'
    ):
        data = self.make_request(f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={key}", period)
        return data
    
    def get_balance_sheet(
            self,
            key: str,
            symbol: str,
            period: str = 'quarterlyReports'
    ):
        data = self.make_request(f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={key}", period)
        return data
    
    def make_request(
            self, 
            url: str,
            period: str = 'quarterlyReports'
            ):
        data = requests.get(url).json()
        period_data = data[period]
        return period_data
    
    def run_quarterly(self, key):

        

instance = GetFundData(key)