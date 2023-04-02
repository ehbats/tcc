import yfinance as yf
import pandas as pd
from datetime import datetime

class GetPriceData():
    def get_price_data(
            self,
            ticker: str, 
            start_date: str, 
            end_date: str = datetime.now()
            ):
        
        df = pd.DataFrame()

        ticker_historical_prices = yf.Ticker(
            ticker
            ).history(
            start = start_date, 
            end = end_date,
            )
        df['High'] = ticker_historical_prices['High']
        df['Low'] = ticker_historical_prices['Low']
        df['Open'] = ticker_historical_prices['Open']
        df['Close'] = ticker_historical_prices['Close']
        df['Volume'] = ticker_historical_prices['Volume']

        return df
