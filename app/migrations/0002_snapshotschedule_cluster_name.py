# Generated by Django 5.0.4 on 2024-04-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapshotschedule',
            name='cluster_name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]