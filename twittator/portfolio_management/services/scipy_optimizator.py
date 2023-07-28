import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from portfolio_management.services.base_optimizator import Optimizator
import pandas as pd
import numpy as np
import cvxpy as cp

class SciPyOptimizator(Optimizator):
    def optimize(self, 
                 price_dfs: list[pd.DataFrame],
                 dfs: list[pd.DataFrame],
                 tickers: dict,
                 prediction_column: str = 'Predictions',
                 price_column: str = 'Close',
                 desired_risk: float = 10,
                 ):
        self.tickers = tickers

        merged_prediction_dfs = self.merge_dataframes(dfs, [prediction_column], tickers)

        merged_price_dfs = self.merge_dataframes(price_dfs, [price_column], tickers)

        size_difference = len(merged_price_dfs.index)-len(merged_prediction_dfs.index)

        columns = list(merged_price_dfs.columns)
        covariance_matrix = self.get_portfolio_covariance_matrix(merged_price_dfs, columns)

        merged_prediction_dfs.apply(
            self.get_row_expected_returns, 
            axis=1, 
            covariance_matrix=covariance_matrix,
            price_dfs=merged_price_dfs,
            size_difference=size_difference,
            desired_risk = desired_risk
            )
        
    def get_row_expected_returns(
            self, 
            row: pd.Series, 
            covariance_matrix: np.ndarray,
            price_dfs: pd.DataFrame,
            size_difference: int,
            desired_risk: float,
        ):
        prediction_index = row.name
        current_price_index = prediction_index + size_difference
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

        desired_risk = self.format_desired_risk(desired_risk)

        weights = cp.Variable(len(expected_returns_list))
        covariance_matrix_as_constant = np.array(covariance_matrix)
        variance = cp.quad_form(weights, covariance_matrix_as_constant)

        expected_returns_array = np.array([expected_returns_list])
        portfolio_return = expected_returns_array @ weights
        portfolio_return = portfolio_return[0]
        gamma = cp.Parameter(nonneg = True)
        gamma.value = 3
        obj = portfolio_return - gamma * variance

        objective = cp.Maximize(obj)

        problem = cp.Problem(
            objective,
            [
             cp.sum(weights) == 1, 
             weights >= 0,
             variance <= desired_risk
             ])
        problem.solve()

        print('RETURNS ARRAY', portfolio_return.value)
        # print('EXPECTED RETURNS ARRAY', expected_returns_array)
        # print('objective', objective.value)
        print('VARIANCE ARRAY', variance.value)
        print('WEIGHTS ARRAY', weights.value)

    def format_desired_risk(self, desired_risk: float):
        desired_risk_as_var = (desired_risk ** 2) / 252
        return desired_risk_as_var