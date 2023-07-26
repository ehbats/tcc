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

    def cp_compatible_return_calculator(self, weights: cp.Variable, returns_list):
        returns = weights @ returns_list
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
        ticker_weights_list = []
        ticker_returns_list = []
        tickers_list = list(ticker_weights.keys())
        for index, expected_return in enumerate(expected_returns_list):
            corresponding_ticker = tickers_list[index]
            ticker_weights[corresponding_ticker]['return'] = expected_return
            ticker_weights_list.append(ticker_weights[corresponding_ticker]['weight'])
            ticker_returns_list.append(expected_return)
        
        weights = cp.Variable(len(ticker_weights_list))
        variance = self.get_portfolio_variance(weights, covariance_matrix)
        objective = cp.Maximize(self.cp_compatible_return_calculator(weights, ticker_returns_list))
        problem = cp.Problem(
            objective,
            [cp.sum(weights) == 1, weights >= 0, variance == 10])
        problem.solve()
        print(weights.value)
        print(type(weights.value))
        print(sum(weights.value))