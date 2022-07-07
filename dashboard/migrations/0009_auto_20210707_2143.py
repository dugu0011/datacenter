# Generated by Django 3.2.5 on 2021-07-07 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_adddevice'),
    ]

    operations = [
        migrations.AddField(
            model_name='adddevice',
            name='Device_Information',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='adddevice',
            name='IP_Address_col4',
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
    ]
