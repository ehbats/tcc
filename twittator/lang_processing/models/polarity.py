import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from django.db import models
from news_data.models.news import News

class Polarity(models.Model):
    id = models.AutoField(primary_key = True)
    relevant_words = models.JSONField(default = list)
    mean_polarization = models.FloatField(default = 0,)
    polarization_list = models.JSONField(default = list)
    news_id = models.ForeignKey(News, on_delete = models.CASCADE)
    news_pubdate = models.DateField(null=True, blank=True)
    news_query = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['news_id'], name="one_to_one_news_to_polarity")
        ]