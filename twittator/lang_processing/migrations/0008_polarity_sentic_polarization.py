# Generated by Django 4.1.7 on 2023-08-29 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lang_processing', '0007_polarity_kagglenews_id_alter_polarity_news_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='polarity',
            name='sentic_polarization',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
    ]