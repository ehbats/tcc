import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from django.db import models
from news_data.models.query import Query


class News(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.TextField(default='')
    rss_link = models.TextField(default='')
    description = models.TextField(default='')
    source = models.TextField(default='')
    source_url = models.TextField(default='')
    pubdate = models.DateField()
    query_id = models.ForeignKey(Query, on_delete = models.CASCADE)
    has_polarization = models.BooleanField(default = False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'source', 'pubdate'], name="unique_news")
        ]