import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_price_data import GetPriceData
import pandas as pd
from ta import trend
from ta import momentum
from ta import volume
from datetime import datetime
from statistics import mean 

from yahoo_data.services.momentum import GetMomentumIndicators

class GenerateTechnicalIndicators:
    """
    This class generates technical indicators for equities prices.
    Each method receives a pandas DataFrame with the price data for a specific Ticker
    and returns the DataFrame with the new indicators added as columns. Each method
    may also receive as params the indicators params such as time windows or other constants.
    
    All of these indicators params have a default value set, according to the reference article.
    You can run all of the indicators at once using the run with default params method, that gets
    all of the indicators using the default parameters set. 
    """
    def __init__(self, ticker: str, start_date: str, end_date: str = datetime.now()):
        """
        This class generates the data necessary to run all of the other methods. It is important that
        the data is loaded on a constructor method as it avoids unecessary API calls, making run time
        more efficient. This class uses the GetPriceData class, that gets all of the price data required
        to run this class's methods. Hence, the inputs are the same as GetPriceData
        
        Inputs:
        - ticker: the ticker of the equity we wish to get price data
        - start_date: the start date from when the price data will be fetched.
        - end_date: price data will be fetched until this date. Defaults to today.
        """
        price_data = GetPriceData()
        self.df = price_data.get_price_data(
            ticker,
            start_date,
            end_date
        )

    def get_trend_indicators(self,
                             df: pd.DataFrame,
                             sma_window: int = 30, 
                             wma_window: int = 30,
                             cci_window: int = 14,
                             cci_constant: float = 0.015
                             ):
        """
        Generates price trend indicators:
        sma (Simple Moving Average)
        wma (Weighted Moving Average)
        cci (Commodity Channel Index)
        
        Inputs:
        sma_window: The window, in days, to generate the sma
        wma_window: The window, in days, to generate the wma
        cci_window: The window, in days, to generate the cci
        cci_constant: Constant param to generate the cci
        """
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
            constant = cci_constant,
            fillna = True
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
        """
        Generates mean reversion indicators:
        Stochastic Oscillator (fast)
        Stochastic Oscillator (slow)

        Generates two columns for both the indicators: stoch and signal.

        Inputs:
        window: The window in days to generate the fast oscillator
        smooth_window: The window in days to generate the slow oscillator    
        """
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
        """
        Generates the relative strength indicators:
        rsi: Relative Strength Index
        williams_r: Williams %R

        Inputs:
        window: Window, in days, to generate the RSI
        william_lpb: Lookback period, in days
        """

        df['rsi'] = momentum.rsi(df['Close'], window = window)

        df['williams_r'] = momentum.williams_r(df['High'], df['Close'], william_lpb)

        return df
    
    def get_volume(self,
                   df: pd.DataFrame,
                   mf_window: int = 14
                   ):
        """
        
        """
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
