# Generated by Django 3.2.5 on 2021-07-30 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0050_auto_20210728_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddevice',
            name='tapelib_space_occupied',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devicetemplate',
            name='tapelib_space_occupied',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
