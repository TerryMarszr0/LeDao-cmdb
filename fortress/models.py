# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AuthRecord(models.Model):

    ROLE_CHOICES = (
        ('root', 'root'),
        # ('admin', 'admin'),
        ('deploy', 'deploy'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=60, null=True, default='')
    host_id = models.IntegerField( null=True, default=0)
    role = models.CharField(max_length=60, null=True, default='', choices=ROLE_CHOICES)
    cuser = models.CharField(max_length=60, null=True, default='')
    ctime = models.IntegerField(null=True, default=None)
    expiration_time = models.IntegerField(null=True, default=0)

    class Meta:
        db_table='fortress_authrecord'


class ApplyRecord(models.Model):
    STATE_CHOICES = (
        ('pending', u'待审核'),
        ('finish', u'通过'),
        ('refuse', u'拒绝'),
    )
    id = models.AutoField(primary_key=True)
    apply_user = models.CharField(max_length=60, null=True, default='')
    apply_time = models.IntegerField(null=True, default=0)
    role = models.CharField(max_length=60, null=True, default='', choices=AuthRecord.ROLE_CHOICES)
    day = models.IntegerField(null=True, default=7)
    state = models.CharField(max_length=30, null=True, default='', choices=STATE_CHOICES)
    reason = models.CharField(max_length=500, null=True, default='')
    reviewer = models.CharField(max_length=60, null=True, default='')
    audit_time = models.IntegerField(null=True, default=0)
    reviewer_reason = models.CharField(max_length=500, null=True, default='')

    class Meta:
        db_table='fortress_applyrecord'

class ApplyTask(models.Model):
    STATE_CHOICES = (
        ('pending', u'待审核'),
        ('ready', u'待执行'),
        ('running', u'执行中'),
        ('success', u'成功'),
        ('failure', u'失败'),
        ('refuse', u'拒绝'),
    )
    id = models.AutoField(primary_key=True)
    apply_id = models.IntegerField(null=True, default=0)
    host_id = models.IntegerField(null=True, default=0)
    role = models.CharField(max_length=60, null=True, default='', choices=AuthRecord.ROLE_CHOICES)
    day = models.IntegerField(null=True, default=7)
    state = models.CharField(max_length=30, null=True, default='', choices=STATE_CHOICES)
    result = models.CharField(max_length=255, null=True, default='')
    run_time = models.IntegerField(null=True, default=None)
    finish_time = models.IntegerField(null=True, default=None)

    class Meta:
        db_table='fortress_applytask'

class SSHKey(models.Model):

    id = models.AutoField(db_column='id', primary_key=True)
    user_id = models.IntegerField(null=True, default=0, unique=True)
    ssh_key = models.TextField(null=True, default='')
    private_key = models.TextField(null=True, default='')

    class Meta:
        db_table = 'fortress_sshkey'