# Generated by Django 4.1.7 on 2023-10-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewer', '0010_cast_movie_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]