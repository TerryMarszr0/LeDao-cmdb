from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AsyncTask(models.Model):
    TASK_STATE=(
        ('unexecuted', 'unexecuted'),
        ('ready', 'ready'),
        ('running', 'running'),
        ('success', 'success'),
        ('failure', 'failure'),
    )
    id = models.AutoField(primary_key=True)
    task = models.CharField(max_length=255, null=True, default='')
    params = models.TextField(null=True, default='')
    state = models.CharField(max_length=30, null=True, default='ready')
    result = models.CharField(max_length=255, null=True, default='')
    ctime = models.IntegerField(null=True, default=0)
    cuser = models.CharField(max_length=60, null=True, default='')
    start_time = models.IntegerField(null=True, default=0)
    finish_time = models.IntegerField(null=True, default=0)
