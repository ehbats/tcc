import snscrape.modules.twitter as sntwitter

lang = 'pt'
query = 'IBOVESPA'
since_date = '2023-01-12'
until_date = '2023-01-13'
max_tweets = 500

class GetTwitterData():
    def get_twitter_data(
            self,
            since_date: str,
            until_date: str,
            query: str = 'IBOVESPA',
            lang: str = 'pt',
        ):
        search_query = f'{query} lang:{lang} since:{since_date} until:{until_date}'

        tweets = []

        for tweet in sntwitter.TwitterSearchScraper(search_query).get_items():
            tweets.append(tweet)
            if len(tweets) >= max_tweets:
                break

        return tweets