import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from lang_processing.models.polarity import Polarity
from news_data.models.news import News
from news_data.models.query import Query
import pandas as pd
from yahoo_data.services.get_price_data import GetPriceData

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
        self.get_news_n_days_prior(periods, df, ticker)

    def get_news_n_days_prior(self, periods: int, df: pd.DataFrame, ticker: str):
        
        polarity_filter = Polarity.objects.filter(
            news_pubdate = df.index[0],
            news_query__icontains = ticker
        )
        print(polarity_filter)

instance = GeneratePolarizationDataFrame()
price_df = GetPriceData().get_price_data(
    'BPAC11.SA',
    '2023-01-01',
    '2023-01-15'
)
instance.generate_polarization_for_ticker(
    price_df,
    'BPAC11',
    5
)
