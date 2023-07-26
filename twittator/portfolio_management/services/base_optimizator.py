import pandas as pd
import sys, os
from abc import ABC, abstractmethod

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_price_data import GetPriceData
from numbers import Number
import numpy as np

class Optimizator(ABC):
    """
    This abstract class is created to create the basic needs to run an
    optimization algorithm. The goal here is to, given expected returns
    and historical prices, optimize the portfolio selection, creating 
    weights for each of the assets, given the calculated portfolio risk
    and expected returns. 
    
    New optimizators should inherit this class and create it's own optimize
    method. There is no standard way to optimize portfolios in this project.
    The user is free to implement optimization methods as they wish, and the
    tools created in this class are here to help. 

    The user's desired path when using this class should be:
    1. Use the class only when already having a DataFrame with prices and expected returns for
    each stock.
    2. Generate a DataFrame with the merged price data of all of the stocks.
    3. Generate the covariance matrix with the DataFrame obtained on step 2.
    4. Using the covariance matrix and the expected returns, optimize the
    portfolio by maximizing the return function. It is recommended to use the constraints:
        - The sum of the weights must equal to 1.
        - The user must pass a constraint specifying a desired risk level OR a desired return. 
    5. Get the generated weights and calculate the actual return. Compare it with the expected
    return to evaluate the model.
    6. Fin.
    """
    @staticmethod
    def get_portfolio_return(
        weights_returns: dict, 
        weight_key: str = 'weight',
        return_key: str = 'return',
        decimal_places: int = 2
        ):
        """
        This class receives a dictionary containing a stock name
        for each key. Each value is a dictionary with the return from the stock and
        it's weight on the portfolio. These informations will be used to calculate
        return of the portfolio, by multiplying the weight by the return for each
        stock and summing the results. 

        Example dictionary:
        dictionary = {
            'PETR4': {
                'weight': 0.6,
                'return': 1
            },
            'MGLU3': {
                'weight': 0.1, 
                'return': -1
            },
            'ITUB4': {
                'weight': 0.3,
                'return': 3
            }
        } 
        Inputs:
        weight_returns: Dictionary exemplified above containing the stocks, weights and returns.
        weight_key (optional): the key that specifies the weight. Defaults to 'weight'.
        return_key (optional): the key that specifies the return. Defautls to 'return'.

        Returns:
        return_sum: The negative sum of the weighted returns, equivalent to the portfolio return.
        This is currently negative due to limitations with the scipy library
        """
        weight_sum = 0
        return_sum = 0
        for weight_return_dict in weights_returns.values():
            return_sum = round(return_sum + weight_return_dict[weight_key] * weight_return_dict[return_key], decimal_places)
            weight_sum += weight_return_dict[weight_key]
        
        if weight_sum != 1:
            raise Exception('The weights do not sum to 1!')

        return -return_sum

    @staticmethod
    def get_portfolio_covariance_matrix(
        prices_df: pd.DataFrame, 
        prices_colums: list[str]
        ):
        """
        This class generates a covariance matrix for stocks.
        Was created to be used along with the merge_dataframes
        method.

        Inputs:
        prices_df: A pandas DataFrame containing the price data for
        all of the desired stocks.
        prices_columns: The column names that should be used to 
        calculate the covariance matrix. E.g.: Close PETR4

        Returns:
        covariance_matrix: The covariance matrix generated
        """
        df_to_generate_cov = prices_df[prices_colums]

        covariance_matrix = df_to_generate_cov.cov()
        
        return covariance_matrix
    
    @staticmethod
    def get_portfolio_variance(
        ordered_weights: list[Number],
        covariance_matrix: pd.DataFrame | np.ndarray
    ):
        """
        Calculates the variance of the portfolio, given
        a covariance matrix and the weights of each asset
        in the matrix.

        Inputs:
        ordered_weights: The weights of each of the stocks
        in the covariance matrix. This list MUST be ordered
        according to the covariance matrix.
        covariance_matrix: the covariance matrix of the stocks.
        
        Returns:
        portfolio_variance: the variance of the portfolio.
        """
        if isinstance(covariance_matrix, pd.DataFrame):
            covariance_matrix = np.matrix(covariance_matrix)
        
        weights = Optimizator.parse_weights_list(ordered_weights)

        portfolio_variance = weights.T * covariance_matrix * weights

        return portfolio_variance.tolist()[0][0]
    
    @staticmethod
    def merge_dataframes(
        dfs_to_merge: list[pd.DataFrame], 
        columns_to_keep: list[str],
        tickers: list[str]
        ):
        """
        Merges prices DataFrames to make analysis easier. Merges
        price DataFrames from many stocks into one.

        Inputs:
        dfs_to_merge: List of pandas DataFrames that the user wishes
        to merge.
        columns_to_keep: List of columns that the user wants to keep 
        in de DataFrame (e.g.: Close).
        tickers: List of ticker names append to the end of each column.
        This is necessary to avoid repeated column names (e.g.: More than
        one column called Close in the DataFrame).
        
        Returns:
        merged_df: the DataFrame with all of the merged price data.
        """
        dataframes = []

        for index, df in enumerate(dfs_to_merge):
            desired_series = df[columns_to_keep]
            desired_series = desired_series.add_suffix(f' {tickers[index]}')
            dataframes.append(desired_series)

        merged_df = pd.concat(dataframes, axis = 1)

        return merged_df
    
    @staticmethod
    def parse_weights_list(weights: list[Number]):
        """
        This method is used to parse the weights list for the
        portfolio variance method. It turns a list of numbers
        into a list of lists containing one number each.
        
        Inputs:
        weights: A list of weights.

        Returns:
        weight_array: An array generated with the list of lists.
        """
        weight_array = []
        for weight in weights:
            weight_array.append([weight])

        return np.array(weight_array)

    @abstractmethod
    def optimize(self):
        """
        This method should be used by lower classes to determine
        how each one of them will calculate the optimized returns. It must
        be implemented.
        """
        raise NotImplementedError('Optimizator classes must implement an optimize method!')
