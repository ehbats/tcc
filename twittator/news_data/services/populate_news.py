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
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from time import time

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
        """
        This class receives the params used to search for news on the google news rss feed and uses the necessary methods created on this app
        to get the content of these news and generate polarization from the text. Then it populates these news on the DB, according to the 
        modelling
        """
        entries = self.get_news_data(query, topic, before, is_query, after, language, country, ceid).entries

        if before:
            try:
                before = datetime.strptime(before, '%Y-%M-%d').date()
            except:
                raise ValidationError(f'The before date {before} is invalid')

        if after:
            try:
                after = datetime.strptime(after, '%Y-%M-%d').date()
            except:
                raise ValidationError(f'The after date {after} is invalid!')

        query, created = Query.objects.get_or_create(
            query = query, 
            topic = topic, 
            before = before, 
            after = after, 
            language= language, 
            country = country, 
            ceid = ceid,
        )

        query.url = self.final_url
        query.save()
        for entry in entries:
            title = entry.title
            published_parsed = entry.published_parsed
            pub_date = f'{published_parsed.tm_year}-{published_parsed.tm_mon}-{published_parsed.tm_mday}'
            try:
                pub_date = datetime.strptime(pub_date, '%Y-%M-%d').date()
            except:
                raise ValidationError(f'Could not parse te PubDate {pub_date}')
            rss_link = entry.link
            source = entry.source.title
            title = title.split(source)[0][:-3]

            news_obj = News.objects.filter(
                rss_link = rss_link
            )
            if not news_obj.exists():
                content = self.get_content(rss_link)
                original_text = ' '.join(content[0])
                original_url = content[1]
                news, created = News.objects.get_or_create(
                    title = title,
                    source = source,
                    pubdate = pub_date,
                    query_id = query
                )

                if created:
                    news.description = original_text
                    news.source_url = original_url
                    news.query_id = query
                    news.rss_link = rss_link
                    news.save()

    def populate_daily_news_between_two_periods(
            self, 
            start_date: str,
            end_date: str,
            query: str
            ):
        """
        The method populate is limited, because it only allows the user to populate date period
        per query. This method will make the same query on the news.google RSS feed
        for every single date in between the start and end dates passed.
        """
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_time = time()
        while start_date < end_date:
            print(f'Attempting date {start_date}!!!')
            next_date = start_date + timedelta(days=2)
            try:
                self.populate(
                    query=query,
                    before=datetime.strftime(next_date, '%Y-%m-%d'),
                    after=datetime.strftime(start_date, '%Y-%m-%d')
                )
            except Exception as error:
                print(f'Failed date {start_date}!!!')
                print(f'Detail: {error}')
            start_date = start_date + timedelta(days=1)
        end_time = time()
        print(f'Finished running between dates {start_date} and {end_date}!!!')

        print(f"Total process time: {round(end_time - start_time, 2)} seconds.")