# Generated by Django 4.1.7 on 2023-10-29 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewer', '0013_remove_watchlist_added_at_remove_watchlist_movie_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='movies',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='movies',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to='moviereviewer.movie'),
        ),
    ]
