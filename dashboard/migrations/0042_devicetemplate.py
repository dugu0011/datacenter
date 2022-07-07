# Generated by Django 3.2.5 on 2021-07-27 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_auto_20210727_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_height', models.IntegerField(blank=True, null=True)),
                ('Device_Asset_Tag', models.CharField(blank=True, max_length=50, null=True)),
                ('Device_Description', models.CharField(blank=True, max_length=200, null=True)),
                ('Unit_Location', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('Device_Information', models.CharField(blank=True, max_length=300, null=True)),
                ('type_of_device', models.CharField(blank=True, max_length=300, null=True)),
                ('network_device_category', models.CharField(blank=True, max_length=50, null=True)),
                ('network_sub_category', models.CharField(blank=True, max_length=50, null=True)),
                ('network_number_of_ports', models.IntegerField(blank=True, null=True)),
                ('network_uplink_ports_wan', models.IntegerField(blank=True, null=True)),
                ('network_connection_type_fibre', models.CharField(blank=True, max_length=50, null=True)),
                ('network_connection_type_ehthernet', models.CharField(blank=True, max_length=50, null=True)),
                ('network_connection_type_both', models.CharField(blank=True, max_length=50, null=True)),
                ('security_device_category', models.CharField(blank=True, max_length=50, null=True)),
                ('security_number_of_ports_lan', models.IntegerField(blank=True, null=True)),
                ('security_network_uplink_ports_wan', models.IntegerField(blank=True, null=True)),
                ('security_connection_type_fibre', models.CharField(blank=True, max_length=50, null=True)),
                ('security_connection_type_ehthernet', models.CharField(blank=True, max_length=50, null=True)),
                ('security_connection_type_both', models.CharField(blank=True, max_length=50, null=True)),
                ('patch_position', models.CharField(blank=True, max_length=50, null=True)),
                ('patch_category_type_inter', models.CharField(blank=True, max_length=50, null=True)),
                ('patch_category_type_cross', models.CharField(blank=True, max_length=50, null=True)),
                ('patch_category_type_isp', models.CharField(blank=True, max_length=50, null=True)),
                ('patch_category_type_other', models.CharField(blank=True, max_length=50, null=True)),
                ('path_number_of_ports', models.IntegerField(blank=True, null=True)),
                ('server_number_of_ports', models.IntegerField(blank=True, null=True)),
                ('server_type_fibre', models.CharField(blank=True, max_length=50, null=True)),
                ('server_type_ehthernet', models.CharField(blank=True, max_length=50, null=True)),
                ('server_type_both', models.CharField(blank=True, max_length=50, null=True)),
                ('chassis_number_of_blades', models.IntegerField(blank=True, null=True)),
                ('chassis_total_blades_slots', models.IntegerField(blank=True, null=True)),
                ('chassis_type_fibre', models.CharField(blank=True, max_length=50, null=True)),
                ('chassis_type_ehthernet', models.CharField(blank=True, max_length=50, null=True)),
                ('chassis_type_both', models.CharField(blank=True, max_length=50, null=True)),
                ('load_number_of_ports', models.IntegerField(blank=True, null=True)),
                ('load_uplink_ports_wan', models.IntegerField(blank=True, null=True)),
                ('load_type_fibre', models.CharField(blank=True, max_length=50, null=True)),
                ('load_type_ehthernet', models.CharField(blank=True, max_length=50, null=True)),
                ('storage_number_of_controllers', models.IntegerField(blank=True, null=True)),
                ('storage_number_of_disks', models.IntegerField(blank=True, null=True)),
                ('storage_capicity_range', models.IntegerField(blank=True, null=True)),
                ('storage_capicity_input', models.CharField(blank=True, max_length=50, null=True)),
                ('storage_type_fibre', models.CharField(blank=True, max_length=50, null=True)),
                ('storage_type_ehthernet', models.CharField(blank=True, max_length=50, null=True)),
                ('storage_type_both', models.CharField(blank=True, max_length=50, null=True)),
                ('tapelib_number_of_magazine', models.IntegerField(blank=True, null=True)),
                ('tapelib_number_io_station', models.IntegerField(blank=True, null=True)),
                ('tapelib_type', models.CharField(blank=True, max_length=50, null=True)),
                ('tapelib_number_tape_capacity', models.IntegerField(blank=True, null=True)),
                ('tapelib_storage_capacity', models.CharField(blank=True, max_length=50, null=True)),
                ('tapelib_space_occupied', models.CharField(blank=True, max_length=50, null=True)),
                ('pdu_category', models.CharField(blank=True, max_length=50, null=True)),
                ('pdu_number_of_power_ports', models.CharField(blank=True, max_length=50, null=True)),
                ('pdu_type', models.CharField(blank=True, max_length=50, null=True)),
                ('pdu_position', models.CharField(blank=True, max_length=50, null=True)),
                ('ups_max_loads', models.CharField(blank=True, max_length=50, null=True)),
                ('ups_number_of_power_ports', models.CharField(blank=True, max_length=50, null=True)),
                ('cctv_url', models.CharField(blank=True, max_length=50, null=True)),
                ('IP_Address_col1', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('IP_Address_col2', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('IP_Address_col3', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('IP_Address_col4', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('deviceMake', models.CharField(blank=True, max_length=200, null=True)),
                ('deviceModel', models.CharField(blank=True, max_length=200, null=True)),
                ('installDate', models.DateField(blank=True, null=True)),
                ('expiryDate', models.DateField(blank=True, null=True)),
                ('deviceOwner', models.CharField(blank=True, max_length=200, null=True)),
                ('deviceWatt', models.FloatField(blank=True, default=0.0)),
                ('deviceSupplies', models.IntegerField(blank=True, null=True)),
                ('deviceConn', models.CharField(blank=True, max_length=200, null=True)),
                ('Special_Notes', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=True)),
                ('data_center_rack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.adddatacenterrackcabinet')),
                ('datacenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.adddatacenter')),
                ('date_center_row', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.adddatacenterrow')),
            ],
        ),
    ]
