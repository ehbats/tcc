from django.db import models

class Query(models.Model):
    id = models.AutoField(primary_key = True)
    query = models.TextField(default="")
    topic = models.TextField(default="")
    before = models.DateField()
    after = models.DateField()
    language = models.TextField(default="")
    country = models.TextField(default="")
    ceid = models.TextField(default="")
    url = models.TextField(default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['query','before','after','language'], name="unique_query_time_language")
        ]