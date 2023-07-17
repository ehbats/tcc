import pandas as pd
import sys, os

class StockPnLCalculator:
    """
    This class calculates daily returns and losses for one stock.
    It receives a pandas DataFrame, and the column that will be used
    to calculate the PnL. For example, one may choose "Open" or "Close"
    to calculate the returns using the open price or the close price
    for that trading session. To make it easier to run a regression 
    or stock returns prediction model, the return between d0 and d1
    will be stored on the d0 row, because the d0 data will be used
    to predict the return on d1.

    params:
    price_data: Pandas DataFrame with the price data of the stock
    column: the column of the pandas DataFrame that will be used
    to calculate the daily returns. Example: 'Open', 'Close'
    periods: determines the number of days before the current date
    that will be used to calculate PnL. Defaults to 1 (daily returns).

    Returns:
    Pandas DataFrame with a new column, with the daily returns
    of the specified column
    """
    def calculate_pnl(
        self,
        price_data: pd.DataFrame,
        column: str,
        periods: int = 1,
    ):
        price_data = price_data.copy(deep = True)
        price_data[f'{column} PnL {periods} days'] = price_data[column].pct_change(periods=periods)
        return price_data