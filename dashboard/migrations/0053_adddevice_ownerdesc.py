# Generated by Django 3.2.5 on 2021-07-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0052_devicetemplate_ownerdesc'),
    ]

    operations = [
        migrations.AddField(
            model_name='adddevice',
            name='ownerDesc',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
