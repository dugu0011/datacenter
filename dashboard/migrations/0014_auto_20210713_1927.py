# Generated by Django 3.2.5 on 2021-07-13 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_notif_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='dc',
            name='contact',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dc',
            name='datat_center_tag',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dc',
            name='email',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dc',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dc',
            name='phone',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dc',
            name='statte',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
