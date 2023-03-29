import yfinance as yf
import pandas as pd
from datetime import datetime
def get_price_data(
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

    return df

ticker = 'MGLU3.SA'
start_date = '2022-01-01'
end_date = '2023-01-05'
results = get_price_data(
    ticker = ticker,
    start_date = start_date,
    end_date = end_date
    )

# print(results)