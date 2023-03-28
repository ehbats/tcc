import yfinance as yf
import pandas as pd
from datetime import datetime
def get_price_data(
        tickers: list, 
        start_date: str, 
        end_date: str = datetime.now()
        ):
    
    df = pd.DataFrame()

    for ticker in tickers:
        ticker_historical_prices = yf.Ticker(
            ticker
            ).history(
            start = start_date, 
            end = end_date,
            )['Close']
        
        df[ticker] = ticker_historical_prices

    return df

tickers = ['MGLU3.SA', 'PETR4.SA', 'ITUB4.SA']
start_date = '2022-01-01'
end_date = '2023-01-05'
results = get_price_data(
    tickers = tickers,
    start_date = start_date,
    end_date = end_date
    )

# print(results)