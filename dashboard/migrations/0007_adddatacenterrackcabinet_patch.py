# Generated by Django 3.2.5 on 2021-07-07 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_adddatacenter_adddatacenterrackcabinet_adddatacenterrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='adddatacenterrackcabinet',
            name='Patch',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
