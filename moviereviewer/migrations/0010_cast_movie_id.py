# Generated by Django 4.1.7 on 2023-10-21 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewer', '0009_movie_vote_average_movie_vote_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cast',
            name='movie_id',
            field=models.IntegerField(null=True),
        ),
    ]
