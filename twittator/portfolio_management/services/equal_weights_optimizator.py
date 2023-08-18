import pandas as pd
from portfolio_management.services.base_optimizator import Optimizator
import numpy as np

class EqualWeightsOptimizator(Optimizator):
    """
    This class implements an optimizator for a very simple investment
    strategy: every n = periods lines, The optimizator selects the
    stocks which have a positive predicted return in n days and equally
    distributes these weights among these stocks. The strategy keeps
    these weights untouched for n days, and then reevaluates with the
    new expected returns for n days. n = periods defaults to 5.

    Inputs:
    - price_dfs: list with the dataframes that contains the prie data for each
    of the stocks
    - dfs: list with the dataframes that contains the prediction data for each
    of the stocks.
    *The dataframes inside these lists will be merged for the analysis.*
    - tickers: list of the tickers.
    - prediction_column: str that determines which column of the 
    param "dfs" is going to be used. Defaults to 'Predictions'.
    - price_column: str that determines which column of the
    param "price_dfs" is going to be used. Defaults to "Close".
    - periods: int that determines for how many days the weights will
    be held. Defaults to 5.
    - initial_investment: The initial value of the capitalization that
    will be used. Defaults to 1.

    Returns:
    The merged prediction dfs adding the columns of the obtained daily return
    generated from the weights and the capitalization from the initial investment.
    """
    def optimize(self, 
                 price_dfs: list[pd.DataFrame],
                 dfs: list[pd.DataFrame],
                 tickers: list[str],
                 prediction_column: str = 'Predictions',
                 price_column: str = 'Close',
                 periods: int = 5,
                 initial_investment: int = 1,
        ):
        """
        Method from the above class that optimizes the portfolio.
        Preprocesses the dataframes and calls the get_row_returns,
        which implements the strategy and gets the returns.
        """
        self.periods = periods
        self.initial_investment = initial_investment

        merged_prediction_dfs = self.merge_dataframes(dfs, [prediction_column], tickers)

        merged_price_dfs = self.merge_dataframes(price_dfs, [price_column], tickers)

        size_difference = len(merged_price_dfs.index)-len(merged_prediction_dfs.index)

        merged_prediction_dfs['obtained_return'] = merged_prediction_dfs.apply(
            self.get_row_returns, 
            axis=1, 
            price_dfs=merged_price_dfs,
            size_difference=size_difference,
            price_column=price_column,
        )

        merged_prediction_dfs['capitalization'] = merged_prediction_dfs.apply(
            self.get_return_from_initial_investment,
            axis=1,
            initial_investment=initial_investment,
            column='obtained_return'
        )

        return merged_prediction_dfs

    def get_row_returns(
            self,
            row: pd.Series,
            price_dfs: pd.DataFrame,
            size_difference: int,
            price_column: str
    ):
        """
        Implements the equal weights based on expected
        returns strategy.
        """
        reset = self.handle_count()

        prediction_index = row.name
        current_price_index = prediction_index + size_difference

        if not reset:
            self.handle_weights([], reset)
        else:
            row_dict = row.to_dict()
            expected_returns_list = list(row_dict.values())

            positive_count = sum(stock_return > 0 for stock_return in expected_returns_list)
            if positive_count > 0:
                ratio = 1 / positive_count
            else:
                ratio = 1 / len(expected_returns_list)
            self.weights = [ratio if stock_return > 0 else 0 for stock_return in expected_returns_list]

        returns = self.get_next_day_retuns(price_dfs, current_price_index, price_column)
        row_portfolio_return = self.weights @ returns

        return row_portfolio_return[0]

    
    def handle_count(self):
        """
        Handles the count to reset
        the weights every n = periods
        days.
        """
        if not hasattr(self, 'count'):
            self.count = 0
        if self.count == 0:
            self.count += 1
            return True
        else:
            if self.count < self.periods -1:
                self.count += 1
            else:
                self.count = 0
            return False
        
    def handle_initial_investment(self, initial_investment: float):
        """
        Simply generates a class attribute corresponding to the
        initial investment.
        """
        if not hasattr(self, 'initial_investment'):
            self.initial_investment = initial_investment
            return self.initial_investment
        return self.initial_investment
    
    def handle_weights(self, result_weights: list[float], reset: bool):
        """
        Gets the weights based on the resets.
        """
        if not hasattr(self, 'weights'):
            self.weights = result_weights
        elif reset:
            self.weights = result_weights
        return self.weights
    
        
    def get_next_day_retuns(self, price_dfs: pd.DataFrame, current_price_index: int, price_column: str):
        """
        Gets the next day return for each of the stocks. These returns will be used on the get_row_returns
        multiplicating these results by the weights. The result of this multiplication corresponds to the 
        portfolio return on that date.
        """
        next_index = current_price_index + 1
        new_df = pd.DataFrame(price_dfs.loc[                
            (price_dfs.index == current_price_index)
            |
            (price_dfs.index == next_index) 
        ])

        returns = new_df.pct_change()

        if len(returns.index) > 1:
            returns.reset_index(drop = True, inplace = True)
            return np.array(returns.iloc[1])[..., np.newaxis]
        return np.zeros((1, len(new_df.columns))).T
    
    def get_return_from_initial_investment(self, row: pd.Series, initial_investment: float, column: str, is_percentage: bool = False):
        """
        Gets the capitalization of the investment, based on the obtained returns of the portfolio.
        """
        initial_investment = self.handle_initial_investment(initial_investment)
        if not is_percentage:
            self.initial_investment = initial_investment * (1 + row[column])
            return self.initial_investment
        self.initial_investment = initial_investment * (1 + row[column]/100)
        return self.initial_investment
