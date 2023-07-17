import yfinance as yf
import pandas as pd
from datetime import datetime

class GetPriceData:
    """
    Inputs:
    - ticker: The ticker of the equity asset
    - start_date: Price data will be fetched starting from this date onwards
    - end_date: Price data will be fetched until this date. Defaults to today
    Returns:
    A pandas containing the following price daily data from the specified ticker
    on the specified date range:
    - High: the highest price at which the specified ticker was traded on a specific date
    - Low: the lowest price at which the specified ticker was traded on a specific date
    - Open: the opening price on that trading session for the specified ticker
    - Close: the close price on that trading session for the specified ticker
    - Volume: the trading volume of the specified ticker on a specific date
    """
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
