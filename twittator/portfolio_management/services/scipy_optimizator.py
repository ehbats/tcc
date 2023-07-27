import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from portfolio_management.services.base_optimizator import Optimizator
import pandas as pd
import numpy as np
from numbers import Number
from copy import deepcopy
from scipy.optimize import minimize
import cvxpy as cp

class SciPyOptimizator(Optimizator):
    def optimize(self, 
                 dfs: list[pd.DataFrame],
                 tickers: dict,
                 price_column: str = 'Close',
                 desired_risk: float = 10,
                 decimal_places: int = 5
                 ):
        self.desired_risk = desired_risk
        self.decimal_places = decimal_places
        ticker_weights = {}
        for index, ticker in enumerate(tickers):
            ticker_weights[ticker] = {}
            if index == 0:
                ticker_weights[ticker]['weight'] = 1
            else:
                ticker_weights[ticker]['weight'] = 0

        merged_price_dfs = self.merge_dataframes(dfs, [price_column], tickers)
        columns = merged_price_dfs.columns.values.tolist()
        covariance_matrix = self.get_portfolio_covariance_matrix(merged_price_dfs, columns)

        merged_price_dfs.apply(
            self.get_row_expected_returns, 
            axis=1, 
            original_ticker_weights=ticker_weights,
            covariance_matrix=covariance_matrix)

    def cp_compatible_return_calculator(self, weights: cp.Variable, returns_array: np.ndarray):
        returns = weights @ returns_array.T
        return returns

    def get_row_expected_returns(
            self, 
            row: pd.Series, 
            original_ticker_weights: dict,
            covariance_matrix: np.ndarray
        ):
        ticker_weights = deepcopy(original_ticker_weights)
        row_dict = row.to_dict()
        expected_returns_list = list(row_dict.values())
        tickers_list = list(ticker_weights.keys())
        for index, expected_return in enumerate(expected_returns_list):
            corresponding_ticker = tickers_list[index]
            ticker_weights[corresponding_ticker]['return'] = expected_return

        weights = cp.Variable(len(expected_returns_list))
        covariance_matrix_as_constant = np.array(covariance_matrix)
        variance = cp.quad_form(weights, covariance_matrix_as_constant.T.dot(covariance_matrix_as_constant))

        expected_returns_array = np.array([expected_returns_list])
        portfolio_return = expected_returns_array @ weights
        gamma = cp.Parameter(nonneg = True)
        gamma.value = self.desired_risk
        obj = portfolio_return - gamma * variance
        objective = cp.Maximize(obj)

        problem = cp.Problem(
            objective,
            [
             cp.sum(weights) == 1, 
             weights >= 0, 
             ])
        problem.solve()