# Generated by Django 5.0.4 on 2024-04-20 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SnapshotSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_name', models.CharField(max_length=100)),
                ('vm_uuid', models.CharField(max_length=100)),
                ('snapshot_time', models.TimeField()),
                ('snapshot_date', models.DateField()),
                ('cluster_ip', models.CharField(max_length=100)),
                ('cluster_uuid', models.CharField(max_length=100)),
            ],
        ),
    ]
