# Generated by Django 3.2.5 on 2021-08-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0062_cameramonitor'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsibleOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=10000)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='devicecapibility',
            name='commString',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
