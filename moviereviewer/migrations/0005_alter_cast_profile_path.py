# Generated by Django 4.1.7 on 2023-08-20 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewer', '0004_cast'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='profile_path',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
