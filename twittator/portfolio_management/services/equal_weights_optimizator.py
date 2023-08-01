import pandas as pd
from portfolio_management.services.base_optimizator import Optimizator
import numpy as np

class EqualWeightsOptimizator(Optimizator):
    def optimize(self, 
                 price_dfs: list[pd.DataFrame],
                 dfs: list[pd.DataFrame],
                 tickers: dict,
                 prediction_column: str = 'Predictions',
                 price_column: str = 'Close',
                 periods: int = 5,
                 initial_investment: int = 1,
        ):
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
        if not hasattr(self, 'initial_investment'):
            self.initial_investment = initial_investment
            return self.initial_investment
        return self.initial_investment
    
    def handle_weights(self, result_weights: list[float], reset: bool):
        if not hasattr(self, 'weights'):
            self.weights = result_weights
        elif reset:
            self.weights = result_weights
        return self.weights
    
        
    def get_next_day_retuns(self, price_dfs: pd.DataFrame, current_price_index: int, price_column: str):
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
        initial_investment = self.handle_initial_investment(initial_investment)
        if not is_percentage:
            self.initial_investment = initial_investment * (1 + row[column])
            return self.initial_investment
        self.initial_investment = initial_investment * (1 + row[column]/100)
        return self.initial_investment
