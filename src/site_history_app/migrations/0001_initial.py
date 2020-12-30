# Generated by Django 3.1.4 on 2020-12-30 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='civil_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.CharField(max_length=30)),
                ('Name', models.CharField(max_length=100)),
                ('Area', models.CharField(max_length=30)),
                ('Requester', models.CharField(max_length=30)),
                ('Consultant_name', models.CharField(max_length=30)),
                ('Request_Date', models.DateField(blank=True, null=True)),
                ('New_requirement', models.TextField()),
                ('new_requirement_details', models.TextField()),
                ('attached_mail', models.CharField(max_length=30)),
                ('Status', models.CharField(max_length=30)),
                ('EIC', models.CharField(max_length=30)),
                ('Feed_back', models.DateField(blank=True, null=True)),
                ('Project_Name', models.CharField(max_length=30)),
                ('Site_Status', models.CharField(max_length=30)),
                ('RT_GF', models.CharField(max_length=30)),
                ('ST_Type', models.CharField(max_length=30)),
                ('Tower_Type', models.CharField(max_length=30)),
                ('Height', models.CharField(max_length=30)),
                ('Tower_body', models.CharField(max_length=30)),
                ('Grillage', models.CharField(max_length=30)),
                ('Anchoring', models.CharField(max_length=30)),
                ('Building', models.CharField(max_length=30)),
                ('Consultant_recommendations', models.TextField()),
                ('Action_Taken', models.CharField(max_length=30)),
                ('Remarks', models.TextField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='power_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Site_Name', models.CharField(max_length=100)),
                ('site_id', models.CharField(max_length=30)),
                ('Site_Vendor', models.CharField(max_length=30)),
                ('Site_Region', models.CharField(max_length=30)),
                ('Site_Type', models.CharField(max_length=30)),
                ('Site_State', models.CharField(max_length=30)),
                ('Position', models.CharField(max_length=30)),
                ('Governate', models.CharField(max_length=30)),
                ('Cabients_Type', models.CharField(max_length=30)),
                ('Cabinet_Num', models.CharField(max_length=30)),
                ('Cabinet_Activity', models.CharField(max_length=30)),
                ('System_Voltage', models.IntegerField(default=0)),
                ('Rectifier_Type', models.CharField(max_length=30)),
                ('Rect_Count', models.IntegerField(default=0)),
                ('Needed_Rectifiers', models.IntegerField(default=0)),
                ('Battery_Type', models.CharField(max_length=30)),
                ('Bat_Count', models.IntegerField(default=0)),
                ('Needed_Batteries', models.IntegerField(default=0)),
                ('Power_Cabinet', models.CharField(max_length=30)),
                ('Power_Conumption', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=20, null=True)),
                ('Generated_Power', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=20, null=True)),
                ('FC_Comp_Name', models.CharField(max_length=30)),
                ('FC_Comp_Count', models.IntegerField(default=0)),
                ('Battery_cabinet', models.CharField(max_length=30)),
                ('Bat_Cab_Count', models.IntegerField(default=0)),
            ],
        ),
    ]