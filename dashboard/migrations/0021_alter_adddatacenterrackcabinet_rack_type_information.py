# Generated by Django 3.2.5 on 2021-07-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20210714_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddatacenterrackcabinet',
            name='Rack_Type_Information',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]