# Generated by Django 3.2.5 on 2021-07-13 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20210713_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='adddatacenterrow',
            name='data_center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.adddatacenter'),
        ),
    ]
