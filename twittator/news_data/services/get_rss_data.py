import feedparser

class GetNewsData():
    BASE_URL =  "https://news.google.com/rss/"
    """
    This class gets the data from the news google rss.
    It receives as inputs the query params which will be used to make queries on the webste.
    query: keywords that will be searched on the news. There are more advanced queries one can make. See google news documentation for more info
    topic: the topic of the news (e.g.: business, health, sports)
    before: the news fetched will be only from before this date
    is_query: if the user does not pass a query, it is necessary to set this param as false, as the url does not support both query and topic searches. Defaults to True
    after: the news fetched will be only from after this date
    language: the language of the news that will be fetched. Defaults to pt-BR
    country: The country where the fetched news were posted. Defaults to BR
    ceid: the id of the country and language. Defaults to PT:br

    Returns the data of the parsed rss feed.
    """
    def get_news_data(
            self,
            query: str = "",
            topic: str = "",
            before: str = "",
            is_query: bool = True,
            after: str = "",
            language: str = 'pt-BR',
            country: str = 'BR',
            ceid: str = 'PT:br',
        ):
        base_url = self.BASE_URL
        
        if is_query:
            base_url = f'{base_url}search?q={query}+after:{after}+before:{before}&'

        if topic != "":
            base_url = f'{base_url}headlines/section/topic/BUSINESS?'
        
        final_url = f'{base_url}hl={language}&gl={country}&ceid={ceid}'

        feed = feedparser.parse(final_url)

        return feed
