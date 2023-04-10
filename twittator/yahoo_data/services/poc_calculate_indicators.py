from poc_yahoo_data import GetPriceData
import pandas as pd
from ta import trend
from ta import momentum
from ta import volume
from datetime import datetime

from momentum import GetMomentumIndicators

ticker = 'MGLU3.SA'
start_date = '2022-01-01'
end_date = '2023-01-05'

class GenerateTechnicalIndicators():
    def __init__(self, ticker: str, start_date: str, end_date: str = datetime.now()):
        price_data = GetPriceData()
        self.df = price_data.get_price_data(
            ticker,
            start_date,
            end_date
        )

    def get_trend_indicators(self,
                             df: pd.DataFrame,
                             sma_window: int = 1, 
                             wma_window: int = 1,
                             cci_window: int = 1,
                             cci_constant: float = 0.015
                             ):
        df['sma'] = trend.sma_indicator(
            df['Close'], 
            window = sma_window,
        )

        df['wma'] = trend.wma_indicator(
            df['Close'],
            window = wma_window
        )

        df['cci'] = trend.cci(
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            window = cci_window,
            constant = cci_constant
        )

        return df
    
    def get_mean_reversion(self,
                           df: pd.DataFrame,
                           window: int = 14, 
                           smooth_window: int = 3):
        fast_stoch = momentum.StochasticOscillator(
            high= df['High'], 
            low= df['Low'], 
            close= df['Close'], 
            window = window, 
            smooth_window = smooth_window
            )

        df['fast_stoch'] = fast_stoch.stoch()
        df['fast_signal'] = fast_stoch.stoch_signal()

        df['slow_stoch'] = df['fast_signal']
        df['slow_signal'] = df['slow_stoch'].rolling(window = smooth_window).mean()
        
        return df
    
    def get_relative_strength(self,
                              df: pd.DataFrame,
                              window: int = 14,
                              william_lpb: int = 14
                              ):
        
        df['rsi'] = momentum.rsi(df['Close'], window = window)

        df['williams_r'] = momentum.williams_r(df['High'], df['Close'], william_lpb)

        return df
    
    def get_volume(self,
                   df: pd.DataFrame,
                   mf_window: int = 14
                   ):
        df['on_balance'] = volume.on_balance_volume(df['Close'], df['Volume'])

        df['MFI'] = volume.money_flow_index(
            df['High'], 
            df['Low'], 
            df['Close'], 
            df['Volume'],
            mf_window
            )
        
        return df
    
    def get_momentum(self,
                     df: pd.DataFrame,
                     macd_window_slow: int = 26,
                     macd_window_fast: int = 12,
                     roc_window: int = 10
                     ):
        df['macd'] = trend.macd(df['Close'], macd_window_slow, macd_window_fast)

        df['roc'] = momentum.roc(df['Close'], roc_window)

        momentum_indicators = GetMomentumIndicators()
        df = momentum_indicators.run_with_standard_intervals(df = df)

        return df

    def run_with_default_params(self):
        df = self.df
        df = self.get_trend_indicators(df = df)
        df = self.get_mean_reversion(df = df)
        df = self.get_relative_strength(df = df)
        df = self.get_volume(df = df)
        df = self.get_momentum(df = df)

        return df

# test_mglu = GetPriceData.get_price_data(
#     ticker = ticker,
#     start_date = start_date,
#     end_date = end_date
#     )


# ## TREND INDICATORS
# moving_average = trend.sma_indicator(
#     test_mglu['Close'], 
#     window = 1,
#     )
# weighted_average = trend.wma_indicator(
#     test_mglu['Close'],
#     window = 1
# )
# cci = trend.cci(
#     high = test_mglu['High'],
#     low = test_mglu['Low'],
#     close = test_mglu['Close'],
#     window = 14,
#     constant = 0.015
# )

# ## MEAN REVERSION

# fast_stoch = momentum.StochasticOscillator(
#     high=test_mglu['High'], 
#     low=test_mglu['Low'], 
#     close=test_mglu['Close'], 
#     window=14, 
#     smooth_window=3
#     )

# fast_stock = fast_stoch.stoch()
# fast_signal = fast_stoch.stoch_signal()

# slow_stock = fast_stock
# slow_signal = slow_stock.rolling(window = 3).mean()

# ## RELATIVE STRENGTH

# rsi = momentum.rsi(test_mglu['Close'], window = 14)

# william = momentum.williams_r(test_mglu['High'], test_mglu['Close'])

# ## VOLUME

# on_balance = volume.on_balance_volume(test_mglu['Close'], test_mglu['Volume'])

# money_flow = volume.money_flow_index(
#     test_mglu['High'], 
#     test_mglu['Low'], 
#     test_mglu['Close'], 
#     test_mglu['Volume'],
#     )

# ## MOMENTUM

# macd = trend.macd(test_mglu['Close'], )

# rate_of_change = momentum.roc(test_mglu['Close'], 10)

# momentums = GetMomentumIndicators.run_with_standard_intervals(test_mglu)

# print(momentums)