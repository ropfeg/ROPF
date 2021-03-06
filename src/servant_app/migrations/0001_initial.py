# Generated by Django 3.1.4 on 2020-12-30 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='general_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.CharField(max_length=30)),
                ('option', models.CharField(max_length=1)),
                ('region', models.CharField(choices=[('Alex', 'Alex'), ('Cairo', 'Cairo'), ('Delta', 'Delta'), ('Giza', 'Giza'), ('Upper', 'Upper')], max_length=30, null=True)),
                ('sub_region', models.CharField(max_length=30)),
                ('longitude', models.FloatField(blank=True, default=None, null=True)),
                ('latitude', models.FloatField(blank=True, default=None, null=True)),
                ('site_type', models.CharField(max_length=30)),
                ('height', models.FloatField(blank=True, default=None, null=True)),
                ('structure_type', models.CharField(max_length=30)),
                ('cluster_avg', models.FloatField(blank=True, default=None, null=True)),
                ('guarded_status', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=30, null=True)),
                ('north_sinai_status', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=30, null=True)),
                ('power_source_status', models.CharField(choices=[('VF_CP', 'VF_CP'), ('VF_Gen', 'VF_Gen'), ('VF_Hybrid', 'VF_Hybrid'), ('ET_CP', 'ET_CP'), ('OR_CP', 'OR_CP'), ('TE_CP', 'TE_CP'), ('VF_PC', 'VF_PC'), ('OR_Gen', 'OR_Gen'), ('ET_Gen', 'ET_Gen'), ('TE_Gen', 'TE_Gen'), ('VF_Solar', 'VF_Solar')], max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='radio_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.CharField(max_length=30)),
                ('rank', models.CharField(choices=[('Medium', 'Medium'), ('Critical', 'Critical'), ('High', 'High'), ('Very Low', 'Very Low'), ('Low', 'Low'), ('Not Ranked', 'Not Ranked')], max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tx_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_id', models.CharField(max_length=30)),
                ('cascaded_sites', models.IntegerField(default=0)),
            ],
        ),
    ]
