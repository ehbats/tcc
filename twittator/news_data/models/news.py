import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from django.db import models
from news_data.models.query import Query


class News(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.TextField()
    rss_link = models.TextField()
    description = models.TextField()
    source = models.TextField()
    source_url = models.TextField()
    pubdate = models.DateField()
    query_id = models.ForeignKey(Query, on_delete = models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'source', 'pubdate'], name="unique_news")
        ]