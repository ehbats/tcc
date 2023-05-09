import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from news_data.services.get_rss_data import GetNewsData
from news_data.services.get_news_content import GetNewsContent
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittator.settings")
django.setup()
from news_data.models.news import News
from news_data.models.query import Query
from django.db import transaction

class PopulateNewsData(GetNewsData, GetNewsContent):
    def populate(
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
        entries = self.get_news_data(query, topic, before, is_query, after, language, country, ceid).entries
        query = Query.objects.get_or_create(
            query = query, 
            topic = topic, 
            before = before, 
            after = after, 
            language= language, 
            country = country, 
            ceid = ceid)[0]
        index = 0
        for entry in entries:
            title = entry.title
            published_parsed = entry.published_parsed
            pub_date = f'{published_parsed.tm_year}-{published_parsed.tm_mon}-{published_parsed.tm_mday}'
            rss_link = entry.link
            source = entry.source.title
            content = self.get_content(rss_link)
            original_text = ' '.join(content[0])
            original_url = content[1]
            
            news = News.objects.get_or_create(
                title = title,
                rss_link = rss_link,
                description = original_text,
                source = source,
                source_url = original_url,
                pubdate = pub_date,
                query_id = query
            )[0]
            news.save()

            index += 1
            if index > 3:
                break
        
get_news = PopulateNewsData()

test_news_with_query = get_news.populate(
    'AMER3',
    before = "2023-01-12",
    after = "2023-01-10",
)