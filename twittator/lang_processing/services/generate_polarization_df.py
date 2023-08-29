import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from lang_processing.models.polarity import Polarity
import pandas as pd
from yahoo_data.services.get_price_data import GetPriceData
from datetime import timedelta
import itertools
import json

class GeneratePolarizationDataFrame:
    """
    This class generates polarization for a ticker. It populates
    a DataFrame with the polarization of n days before each date.
    The DataFrame must have a column with date values in the 
    yyyy-mm-dd, so the function can compare the date column
    with the dates on the News table.
    Params:
    df: pandas DataFrame that must contain a date column.
    ticker: the ticker of the stock that will have the daily polarization calculated.
    Can be any query that was used in the News app, however, this param will be called
    ticker because for now the only news that will be on the news app will be related to
    tickers.
    periods: amount of days that will be used to calculate the
    polarization. Defaults to 1.
    """
    def generate_polarization_for_ticker(
            self,
            df: pd.DataFrame,
            ticker: str,
            periods: int = 1,
    ):
        df['polarity'] = df.index.to_series().apply(self.get_news_n_days_prior, ticker = ticker, periods = periods)
        
        return df

    def get_news_n_days_prior(self, date, query: dict = {}, periods: int = 5):
        final_date = pd.to_datetime(date)
        start_date = final_date - timedelta(days=periods)

        date_polarity_list = []
        date_sentic_polarity_list = []

        polarity_filter = Polarity.objects.filter(
            news_pubdate__lte = final_date,
            news_pubdate__gte = start_date,
            **query
        )
        
        if polarity_filter.exists():
            for polarity in polarity_filter:
                parsed_polarity = json.loads(polarity.polarization_list)
                date_polarity_list.append(parsed_polarity)
                parsed_sentic_polarity = json.loads(polarity.sentic_polarization_list)
                date_sentic_polarity_list.append(parsed_sentic_polarity)
        final_list = list(itertools.chain(*date_polarity_list))
        sentic_list = list(itertools.chain(*date_sentic_polarity_list))
        
        return final_list, sentic_list

# instance = GeneratePolarizationDataFrame()
# price_df = GetPriceData().get_price_data(
#     'BPAC11.SA',
#     '2023-01-01',
#     '2023-01-15'
# )
# instance.generate_polarization_for_ticker(
#     price_df,
#     'BPAC11',
#     1
# )
