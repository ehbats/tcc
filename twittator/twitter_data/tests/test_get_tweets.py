import sys, os
sys.path.append(os.path.abspath("."))
from twitter_data.services.get_twitter_data import GetTwitterData

twitter_data = GetTwitterData()

data = twitter_data.get_twitter_data(
    '2023-01-07',
    '2023-01-09'
)

for tweet in data:
    print(tweet.content)