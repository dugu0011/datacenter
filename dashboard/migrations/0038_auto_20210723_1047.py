# Generated by Django 3.2.5 on 2021-07-23 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_browser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browser',
            name='chrome',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='browser',
            name='firefox',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='browser',
            name='mozilla',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='browser',
            name='others',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='browser',
            name='safari',
            field=models.FloatField(default=0.0),
        ),
    ]
