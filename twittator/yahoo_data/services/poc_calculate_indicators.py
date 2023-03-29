from poc_get_data import get_price_data
import pandas as pd
from ta import trend

ticker = 'MGLU3.SA'
start_date = '2022-01-01'
end_date = '2023-01-05'

results = get_price_data(
    ticker = ticker,
    start_date = start_date,
    end_date = end_date
    )

# def get_technical_analysis(data: pd.DataFrame):

test_mglu = results

moving_average = trend.sma_indicator(
    test_mglu['Close'], 
    window = 1,
    )
weighted_average = trend.wma_indicator(
    test_mglu['Close'],
    window = 1
)
cci = trend.CCIIndicator(
    high = test_mglu['High'],
    low = test_mglu['Low'],
    close = test_mglu['Close'],
    window = 14,
    constant = 0.015
)