# Generated by Django 3.2.5 on 2021-07-21 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_devicedetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uptime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startingTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
