# Generated by Django 3.2.5 on 2021-08-18 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0065_raiseticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raiseticket',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
