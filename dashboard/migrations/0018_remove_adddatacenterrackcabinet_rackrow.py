# Generated by Django 3.2.5 on 2021-07-13 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_adddatacenterrackcabinet_datacenter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adddatacenterrackcabinet',
            name='RackRow',
        ),
    ]
