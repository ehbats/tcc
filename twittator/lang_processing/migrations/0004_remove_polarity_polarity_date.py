# Generated by Django 4.1.7 on 2023-05-14 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lang_processing', '0003_polarity_polarity_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polarity',
            name='polarity_date',
        ),
    ]
