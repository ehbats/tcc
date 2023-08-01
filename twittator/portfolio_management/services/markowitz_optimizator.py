import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from portfolio_management.services.base_optimizator import Optimizator
import pandas as pd
import numpy as np
import cvxpy as cp

class MarkowitzOptimizator(Optimizator):
    def optimize(self, 
                 price_dfs: list[pd.DataFrame],
                 dfs: list[pd.DataFrame],
                 tickers: dict,
                 prediction_column: str = 'Predictions',
                 price_column: str = 'Close',
                 desired_risk: float = 10,
                 periods: int = 5,
                 initial_investment: int = 1,
                 ):
        self.count = 0
        self.tickers = tickers
        self.periods = periods

        merged_prediction_dfs = self.merge_dataframes(dfs, [prediction_column], tickers)

        merged_price_dfs = self.merge_dataframes(price_dfs, [price_column], tickers)

        size_difference = len(merged_price_dfs.index)-len(merged_prediction_dfs.index)

        merged_prediction_dfs['obtained_return'] = merged_prediction_dfs.apply(
            self.get_row_returns, 
            axis=1, 
            price_dfs=merged_price_dfs,
            size_difference=size_difference,
            desired_risk=desired_risk,
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
            desired_risk: float,
            price_column: str
        ):
        reset = self.handle_count()

        prediction_index = row.name
        current_price_index = prediction_index + size_difference

        if not reset:
            self.handle_weights([], reset)
        else:
            prices_until_current_line = price_dfs.loc[
                (price_dfs.index < current_price_index)
                &
                (price_dfs.index > current_price_index - 252)
                ]
            columns = list(prices_until_current_line.columns)
            covariance_matrix = self.get_portfolio_covariance_matrix(
                prices_until_current_line,
                columns
            )
            row_dict = row.to_dict()
            expected_returns_list = list(row_dict.values())

            formatted_risk = self.format_desired_risk(desired_risk)

            weights = cp.Variable(len(expected_returns_list))
            covariance_matrix_as_constant = np.array(covariance_matrix)
            variance = cp.quad_form(weights, covariance_matrix_as_constant)

            expected_returns_array = np.array([expected_returns_list])
            portfolio_return = expected_returns_array @ weights
            portfolio_return = portfolio_return[0]
            gamma = cp.Parameter(nonneg = True)
            gamma.value = 6
            obj = portfolio_return - gamma * variance

            objective = cp.Maximize(obj)

            problem = cp.Problem(
                objective,
                [
                cp.sum(weights) == 1, 
                weights >= 0,
                variance <= formatted_risk
                ])
            problem.solve()

            self.handle_weights(weights.value, reset)

        returns = self.get_next_day_retuns(price_dfs, current_price_index, price_column)

        row_portfolio_return = self.weights @ returns

        return row_portfolio_return[0]

    def format_desired_risk(self, desired_risk: float):
        desired_risk_as_var = (desired_risk ** 2) / 252
        return desired_risk_as_var
    
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
            
    def handle_weights(self, result_weights: list[float], reset: bool):
        if not hasattr(self, 'weights'):
            self.weights = result_weights
        elif reset:
            self.weights = result_weights
        return self.weights
    
    def handle_initial_investment(self, initial_investment: float):
        if not hasattr(self, 'initial_investment'):
            self.initial_investment = initial_investment
            return self.initial_investment
        return self.initial_investment
        