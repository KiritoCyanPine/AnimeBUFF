# Generated by Django 3.0.6 on 2020-06-01 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animetitles', '0004_animetitle_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animetitle',
            name='genres',
            field=models.CharField(max_length=200),
        ),
    ]
