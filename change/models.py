# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Change(models.Model):

    ACTION = (
        ('create', 'create'),
        ('update', 'update'),
        ('delete', 'delete'),
    )

    id = models.AutoField(primary_key=True)
    uuid = models.CharField(db_column='uuid', max_length=128, null=True, default='')
    username = models.CharField(db_column='username', max_length=60, null=True, default='')
    resource = models.CharField(db_column='resource', max_length=60, null=True, default='')
    res_id = models.CharField(db_column='res_id', max_length=64, null=True, default='')
    action = models.CharField(db_column='action', choices=ACTION, max_length=30, null=True, default='')
    index = models.CharField(max_length=100, null=True, default='', db_index=True)
    message = models.TextField(blank=True, default='')
    change_time = models.IntegerField(db_column='change_time', null=True, default=None, db_index=True)
    ctime = models.IntegerField(db_column='ctime', null=True, default=None)

    class Meta:
        index_together = ('resource', 'res_id')
        db_table = 'change_change'