# Generated by Django 4.1.7 on 2023-11-04 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewer', '0017_alter_reviews_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]