import feedparser

class GetNewsData():
    BASE_URL =  "https://news.google.com/rss/"
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
        print(final_url)
        feed = feedparser.parse(final_url)

        return feed

# rss_url = "https://news.google.com/rss/search?q=EXEMPLO&hl=pt-BR&gl=BR&ceid=PT:br"
# feed = feedparser.parse(rss_url)

# for entry in feed.entries:
#     print(entry.title)
#     print(entry.summary)
#     print()
