# Generated by Django 4.1.7 on 2023-10-03 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewer', '0006_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_by', models.CharField(max_length=255)),
                ('added_at', models.DateTimeField(auto_now=True)),
                ('movie_id', models.ManyToManyField(related_name='movies', to='moviereviewer.movie')),
            ],
        ),
    ]
