import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from news_data.services.get_rss_data import GetNewsData

get_news = GetNewsData()

test_news_with_query = get_news.get_news_data(
    'intitle:PETR4',
    before = "2023-01-12",
    after = "2023-01-10",
)
for entry in test_news_with_query.entries:
    print(entry.title, entry.link)
print(len(test_news_with_query.entries))

# test_news_with_topic = get_news.get_news_data(
#     is_query = False,
#     topic = 'BUSINESS',
# )

# for entry in test_news_with_topic.entries:
#     print(entry.title)
# print(len(test_news_with_topic.entries))
