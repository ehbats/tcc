import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from news_data.services.populate_news import PopulateNewsData

get_news = PopulateNewsData()

get_news.populate_daily_news_between_two_periods(
    '2021-01-01',
    '2021-02-01',
    'intitle:BPAC11'
)