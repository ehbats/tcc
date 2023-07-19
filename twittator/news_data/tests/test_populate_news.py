import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from news_data.services.populate_news import PopulateNewsData

get_news = PopulateNewsData()

# test_news_with_query = get_news.populate(
#     'AMER3',
#     before = "2023-01-12",
#     after = "2023-01-10",
# )
get_news.populate_daily_news_between_two_periods(
    '2023-01-01',
    '2023-01-15',
    'intitle:BPAC11'
)