# Generated by Django 3.2.5 on 2021-07-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0048_gittest'),
    ]

    operations = [
        migrations.AddField(
            model_name='gittest',
            name='series2',
            field=models.FloatField(default=0.0),
        ),
    ]
