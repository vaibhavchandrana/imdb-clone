# Generated by Django 4.1.7 on 2023-03-12 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_movielist_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]