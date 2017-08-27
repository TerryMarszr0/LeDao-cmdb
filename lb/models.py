# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from host.models import Hosts

class LB(models.Model):

    id = models.AutoField(primary_key=True)
    lb_service_id = models.IntegerField(null=False , default=0)
    env = models.CharField(null=False, max_length=30, default='')
    server_name = models.CharField(null=False , max_length=255, default='')
    port = models.IntegerField(null=False , default=0)
    sslport = models.IntegerField(null=False, default=0)
    parameter = models.CharField(max_length=3000, null=False, default='')
    # access_log = models.CharField(max_length=255, null=True, default='')
    # error_log = models.CharField(max_length=255, null=True, default='')
    comment = models.CharField(max_length=255, null=True, default='')
    ctime = models.IntegerField(null=True, default=None)
    cuser = models.CharField(null=True, max_length=60, default='')


    class Meta:
        db_table = 'lb_lb'
        unique_together = ('server_name', 'port', 'env')

class ServiceLB(models.Model):

    UPSTREAM_TYPE_CHOICES = (
        ('wrr', 'wrr'),
        ('ip_hash', 'ip_hash'),
    )

    id = models.AutoField(primary_key=True)
    lb_id = models.IntegerField(null=False , default=0)
    service_id = models.IntegerField(null=False, default=0)
    path = models.CharField(null=False, max_length=255, default='')
    proxy_path = models.CharField(null=False, max_length=255, default='')
    # type = models.CharField(choices=UPSTREAM_TYPE_CHOICES, max_length=30, null=True, default='wrr')
    backend_port = models.IntegerField(null=False , default=0)
    # max_fails = models.IntegerField(null=False , default=0)
    # fail_timeout = models.IntegerField(null=False , default=0)
    location_parameter = models.CharField(max_length=1500, null=False, default='')

    class Meta:
        db_table = 'lb_servicelb'
        unique_together = ('lb_id', 'path')

