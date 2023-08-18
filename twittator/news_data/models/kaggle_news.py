from django.db import models

class KaggleNews(models.Model):
    class CountryChoices(models.TextChoices):
        USA = 'USA'
        BRZ = 'BRZ'

    id = models.AutoField(primary_key = True)
    title = models.TextField(default='')
    description = models.TextField(default='')
    has_description = models.BooleanField(default=True)
    source = models.TextField(default='')
    category = models.TextField(default='BUSINESS')
    source = models.TextField(default='')
    pubdate = models.DateField()
    country = models.TextField(choices=CountryChoices.choices, default=CountryChoices.BRZ)
    kaggle_url = models.TextField(default='')
    has_polarization = models.BooleanField(default = False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'country'], name="unique_kaggle_news")
        ]