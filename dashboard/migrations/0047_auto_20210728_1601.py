# Generated by Django 3.2.5 on 2021-07-28 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0046_auto_20210728_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adddevice',
            name='patchcross3',
        ),
        migrations.RemoveField(
            model_name='adddevice',
            name='patchlist3',
        ),
        migrations.RemoveField(
            model_name='adddevice',
            name='patchrouter3',
        ),
        migrations.RemoveField(
            model_name='adddevice',
            name='patchswitch3',
        ),
        migrations.RemoveField(
            model_name='adddevice',
            name='patchtag3',
        ),
        migrations.RemoveField(
            model_name='adddevice',
            name='patchuplonks3',
        ),
        migrations.RemoveField(
            model_name='devicetemplate',
            name='patchcross3',
        ),
        migrations.RemoveField(
            model_name='devicetemplate',
            name='patchlist3',
        ),
        migrations.RemoveField(
            model_name='devicetemplate',
            name='patchrouter3',
        ),
        migrations.RemoveField(
            model_name='devicetemplate',
            name='patchswitch3',
        ),
        migrations.RemoveField(
            model_name='devicetemplate',
            name='patchtag3',
        ),
        migrations.RemoveField(
            model_name='devicetemplate',
            name='patchuplonks3',
        ),
        migrations.AddField(
            model_name='adddevice',
            name='patchcross1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='adddevice',
            name='patchlist1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='adddevice',
            name='patchrouter1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='adddevice',
            name='patchswitch1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='adddevice',
            name='patchtag1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='adddevice',
            name='patchuplonks1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='devicetemplate',
            name='patchcross1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='devicetemplate',
            name='patchlist1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='devicetemplate',
            name='patchrouter1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='devicetemplate',
            name='patchswitch1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='devicetemplate',
            name='patchtag1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='devicetemplate',
            name='patchuplonks1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]