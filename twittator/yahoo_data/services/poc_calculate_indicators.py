from poc_get_data import GetPriceData
import pandas as pd
from ta import trend
from ta import momentum
from ta import volume
ticker = 'MGLU3.SA'
start_date = '2022-01-01'
end_date = '2023-01-05'

results = GetPriceData.get_price_data(
    ticker = ticker,
    start_date = start_date,
    end_date = end_date
    )

# def get_technical_analysis(data: pd.DataFrame):

test_mglu = results

## TREND INDICATORS
moving_average = trend.sma_indicator(
    test_mglu['Close'], 
    window = 1,
    )
weighted_average = trend.wma_indicator(
    test_mglu['Close'],
    window = 1
)
cci = trend.cci(
    high = test_mglu['High'],
    low = test_mglu['Low'],
    close = test_mglu['Close'],
    window = 14,
    constant = 0.015
)

## MEAN REVERSION

fast_stoch = momentum.StochasticOscillator(
    high=test_mglu['High'], 
    low=test_mglu['Low'], 
    close=test_mglu['Close'], 
    window=14, 
    smooth_window=3
    )

fast_stock = fast_stoch.stoch()
fast_signal = fast_stoch.stoch_signal()

slow_stoch = momentum.StochasticOscillator(
    high=test_mglu['High'], 
    low=test_mglu['Low'], 
    close=test_mglu['Close'], 
    window=14, 
    smooth_window=3, 
    signal_window=3)

slow_stock = slow_stoch.stoch()
slow_signal = slow_stoch.stoch_signal()

## RELATIVE STRENGTH

rsi = momentum.rsi(test_mglu['Close'], window = 14)

william = momentum.williams_r(test_mglu['High'], test_mglu['Close'])

## VOLUME

on_balance = volume.on_balance_volume(test_mglu['Close'], test_mglu['Volume'])

money_flow = volume.money_flow_index(
    test_mglu['High'], 
    test_mglu['Low'], 
    test_mglu['Close'], 
    test_mglu['Volume'],
    )

## MOMENTUM

macd = trend.macd(test_mglu['Close'], )

rate_of_change = momentum.roc(test_mglu['Close'], 10)

