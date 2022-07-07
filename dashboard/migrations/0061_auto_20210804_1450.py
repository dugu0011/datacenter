# Generated by Django 3.2.5 on 2021-08-04 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0060_auto_20210804_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicecapibility',
            name='is_netconf',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='devicecapibility',
            name='is_restconf',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='devicecapibility',
            name='is_snmp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='devicecapibility',
            name='netconf',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicecapibility',
            name='restconf',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devicecapibility',
            name='snmp',
            field=models.TextField(blank=True, null=True),
        ),
    ]
