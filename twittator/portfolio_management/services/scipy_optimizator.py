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
        self.constraints = [
            {'type': 'eq', 'fun': self.weights_constraint, 'args': (ticker_weights)},
            {'type': 'uneq', 'fun': self.risk_constraint, 'args': (desired_risk, covariance_matrix, ticker_weights)}
        ]

        merged_price_dfs.apply(
            self.get_row_expected_returns, 
            axis=1, 
            original_ticker_weights=ticker_weights,
            covariance_matrix=covariance_matrix)

    def weights_constraint(self, iterator, ticker_weights: dict):
        weights = list(ticker_weights.values())

        return sum(weights) -1
    
    def risk_constraint(self, iterator, max_risk: Number, covariance_matrix: np.ndarray, ticker_weights: dict):
        ticker_weights = ticker_weights
        weights = list(ticker_weights.values())
        variance = self.get_portfolio_variance(weights, covariance_matrix)

        return variance - max_risk

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
        
        row_return = self.get_portfolio_return(ticker_weights, decimal_places=self.decimal_places)
        minimize(self.get_portfolio_return, original_ticker_weights, )
        return -row_return
    