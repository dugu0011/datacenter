# Generated by Django 3.2.5 on 2021-07-13 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_notif_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='adddevice',
            name='cctv_url',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]