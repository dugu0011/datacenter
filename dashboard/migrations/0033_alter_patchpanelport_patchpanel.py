# Generated by Django 3.2.5 on 2021-07-22 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_alter_patchpanelport_patchpanel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patchpanelport',
            name='patchpanel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.patchpanel'),
        ),
    ]
