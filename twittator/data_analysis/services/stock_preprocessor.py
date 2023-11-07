import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_ta_indicators import GenerateTechnicalIndicators
from yahoo_data.services.get_pca import GeneratePCAByGrouping
from yahoo_data.services.get_price_data import GetPriceData
from portfolio_management.services.get_stock_pnl import StockPnLCalculator
from data_analysis.useful_defaults import GROUPS
from datetime import datetime

class StockPreprocessor:
    @staticmethod
    def preprocess(
            ticker: str,
            start_date: str,
            price_column: str,
            return_periods: int,
            end_date: str = datetime.now(),
            generate_technical: bool = True
        ):
            if generate_technical:
                technical_indicators_df = GenerateTechnicalIndicators(
                    ticker,
                    start_date,
                    end_date
                ).run_with_default_params()
                technical_indicators_df = technical_indicators_df.dropna()

                groups = GROUPS

                df_after_pca = GeneratePCAByGrouping().generate_pca(
                    df = technical_indicators_df, 
                    groupings = groups,
                    columns_to_leave = ['Open', 'High', 'Low', 'Close'],
                )
            else:
                df_after_pca = GetPriceData().get_price_data(
                    ticker,
                    start_date,
                    end_date
                )
            df_n_days = StockPnLCalculator().calculate_pnl(
                df_after_pca,
                price_column,
                return_periods
            )
            df_n_days = df_n_days.dropna()
            
            return df_n_days