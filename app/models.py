from django.db import models

class SnapshotSchedule(models.Model):
    vm_name = models.CharField(max_length=100)
    vm_uuid = models.CharField(max_length=100)
    snapshot_time = models.TimeField()
    snapshot_date = models.DateField()
    cluster_ip = models.CharField(max_length=100)
    cluster_name = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100, blank=True, null=True)
    snapshot_taken = models.BooleanField(default=False)
    snapshot_execution_datetime = models.CharField(max_length=100,default='none')
    snapshot_name = models.CharField(max_length=200,default='snapshot_by_script')
    snapshot_failed = models.BooleanField(default=False)