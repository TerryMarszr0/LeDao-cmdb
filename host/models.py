# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Hosts(models.Model):
    HOST_ENV_CHOICES = (
        ('prod', 'prod'),
        ('stg', 'stg'),
        ('uat', 'uat'),
        ('test', 'test'),
        ('dev', 'dev'),
    )

    HOST_TYPE_CHOICES = (
        # ('aliyun', 'aliyun'),
        ('server', 'server'),
        ('net', 'net'),
        ('vm', 'vm'),
        ('storage', 'storage'),
        ('other', 'other'),
    )

    HOST_ATTRIBUTE_CHOCIES = (
        # ('ECS','ECS'),
        # ('SLB','SLB'),
        # ('RDS','RDS'),
        ('server','server'),
        ('kvmparent','kvmparent'),
        ('xenparent','xenparent'),
        ('vmwareparent','vmwareparent'),
        ('dockerparent','dockerparent'),
        ('xen','xen'),
        ('kvm','kvm'),
        ('vmware','vmware'),
        ('docker','docker'),
        ('net','net'),
        ('switch','switch'),
        ('route','route'),
        ('ap','ap'),
        ('firewall','firewall'),
        ('storage', 'storage'),
        ('other', 'other'),
    )

    HOST_ALIYUN_TYPE_CHOCIES = (
        ('ECS','ECS'),
        # ('SLB','SLB'),
        # ('RDS','RDS'),
    )

    HOST_STATE_CHOCIES = (
        ('online', 'online'),
        ('offline', 'offline'),
        ('free', 'free'),
        # ('unuse', 'unuse'),
        # ('install', 'install'),
        # ('broken', 'broken'),
    )

    id = models.AutoField(db_column='id', primary_key=True)
    instance_id = models.CharField(db_column='instance_id', unique=True, null=False, default='', max_length=128)
    sn = models.CharField(db_column='sn', null=True, default='', max_length=90)
    mac = models.CharField(db_column='mac', null=True, default='', max_length=90)
    type = models.CharField(db_column='type', choices=HOST_TYPE_CHOICES, null=True, default='', max_length=30)
    attribute = models.CharField(db_column='attribute', choices=HOST_ATTRIBUTE_CHOCIES, null=True, default='', max_length=30)
    env = models.CharField(db_column='env', max_length=30, choices=HOST_ENV_CHOICES, null=True, default='')
    model_id = models.IntegerField(db_column='model_id', null=True, default=0)
    conf_id = models.IntegerField(db_column='conf_id', null=True, default=0)
    room_id = models.IntegerField(db_column='room_id', null=True, default=0)
    rack_id = models.IntegerField(db_column='rack_id', null=True, default=0)
    position = models.CharField(db_column='location', null=True, max_length=60, default='')
    pid = models.IntegerField(db_column='pid', null=True, default=0)
    state = models.CharField(db_column='state', null=True, choices=HOST_STATE_CHOCIES, max_length=30, default='offline')
    hostname = models.CharField(db_column='hostname', null=True, default='', max_length=100)
    img_id = models.IntegerField(db_column='img_id', null=True, default=0)
    service_id = models.IntegerField(db_column='service_id', null=True, default=0)
    ctime = models.IntegerField(db_column='ctime', null=True, default=None)
    description = models.CharField(db_column='description', null=True, max_length=255, default='')
    ip = models.CharField(db_column='ip', max_length=60, null=True, default='')
    oobip = models.CharField(db_column='oobip', max_length=60, null=True, default='')
    publicip = models.CharField(db_column='publicip', max_length=60, null=True, default='')
    expiration_time = models.IntegerField(db_column='expiration_time', null=True, default=None)
    shiptime = models.IntegerField(db_column='shiptime', null=True, default=None)
    amount = models.FloatField(db_column='amount', null=True, default=0)
    aliyun_id = models.CharField(db_column='aliyun_id', null=True, default='', max_length=128)
    cpu = models.CharField(db_column='cpu', null=True, default='', max_length=255)
    memory = models.CharField(db_column='memory', null=True, default='', max_length=255)
    disk = models.CharField(db_column='disk', null=True, default='', max_length=500)
    os_name = models.CharField(db_column='os_name', null=True, default='', max_length=255)
    kernel = models.CharField(db_column='kernel', null=True, default='', max_length=120)
    region_id = models.CharField(db_column='region_id', null=True, default='', max_length=60)
    zone_id = models.CharField(db_column='zone_id', null=True, default='', max_length=60)

    class Meta:
        db_table = 'host_hosts'

class HostDeleted(models.Model):

    id = models.IntegerField(db_column='id', primary_key=True, default=0)
    instance_id = models.CharField(db_column='instance_id', unique=True, null=False, default='', max_length=128)
    sn = models.CharField(db_column='sn', null=True, default='', max_length=90)
    mac = models.CharField(db_column='mac', null=True, default='', max_length=90)
    type = models.CharField(db_column='type', choices=Hosts.HOST_TYPE_CHOICES, null=True, default='', max_length=30)
    attribute = models.CharField(db_column='attribute', choices=Hosts.HOST_ATTRIBUTE_CHOCIES, null=True, default='', max_length=30)
    env = models.CharField(db_column='env', max_length=30, choices=Hosts.HOST_ENV_CHOICES, null=True, default='')
    model_id = models.IntegerField(db_column='model_id', null=True, default=0)
    conf_id = models.IntegerField(db_column='conf_id', null=True, default=0)
    room_id = models.IntegerField(db_column='room_id', null=True, default=0)
    rack_id = models.IntegerField(db_column='rack_id', null=True, default=0)
    position = models.CharField(db_column='location', null=True, max_length=60, default='')
    pid = models.IntegerField(db_column='pid', null=True, default=0)
    state = models.CharField(db_column='state', null=True, choices=Hosts.HOST_STATE_CHOCIES, max_length=30, default='offline')
    hostname = models.CharField(db_column='hostname', null=True, default='', max_length=100)
    img_id = models.IntegerField(db_column='img_id', null=True, default=0)
    service_id = models.IntegerField(db_column='service_id', null=True, default=0)
    ctime = models.IntegerField(db_column='ctime', null=True, default=None)
    description = models.CharField(db_column='description', null=True, max_length=255, default='')
    ip = models.CharField(db_column='ip', max_length=60, null=True, default='')
    oobip = models.CharField(db_column='oobip', max_length=60, null=True, default='')
    publicip = models.CharField(db_column='publicip', max_length=60, null=True, default='')
    expiration_time = models.IntegerField(db_column='expiration_time', null=True, default=None)
    shiptime = models.IntegerField(db_column='shiptime', null=True, default=None)
    amount = models.FloatField(db_column='amount', null=True, default=0)
    aliyun_id = models.CharField(db_column='aliyun_id', null=True, default='', max_length=128)
    cpu = models.CharField(db_column='cpu', null=True, default='', max_length=255)
    memory = models.CharField(db_column='memory', null=True, default='', max_length=255)
    disk = models.CharField(db_column='disk', null=True, default='', max_length=500)
    os_name = models.CharField(db_column='os_name', null=True, default='', max_length=255)
    kernel = models.CharField(db_column='kernel', null=True, default='', max_length=120)
    region_id = models.CharField(db_column='region_id', null=True, default='', max_length=60)
    zone_id = models.CharField(db_column='zone_id', null=True, default='', max_length=60)

    class Meta:
        db_table = 'host_hostdeleted'

# class HostApp(models.Model):
#
#     id = models.AutoField(db_column='id', primary_key=True)
#     host_id = models.IntegerField(db_column='host_id', null=True, default=0)
#     app_id = models.IntegerField(db_column='app_id', null=True, default=0)
#
#     class Meta:
#         db_table = 'host_hostapp'

class Image(models.Model):

    OS_TYPE_CHOCIES = (
        ('linux', 'linux'),
        ('windows', 'windows'),
    )

    PLATFORM_CHOCIES = (
        ('CentOS', 'CentOS'),
        ('Ubuntu', 'Ubuntu'),
        ('RedHat', 'RedHat'),
        ('Windows Server', 'Windows Server'),
        ('other', 'other'),
    )

    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', null=True, default='', max_length=100, unique=True)
    image_id = models.CharField(db_column='image_id', null=True, default='', max_length=100)
    os_type = models.CharField(db_column='os_type', null=True, default='', max_length=30, choices=OS_TYPE_CHOCIES)
    platform = models.CharField(db_column='platform', null=True, default='', max_length=60, choices=PLATFORM_CHOCIES)
    description = models.CharField(db_column='description', null=True, max_length=255, default='')
    ctime = models.IntegerField(db_column='ctime', null=True, default=0)

    class Meta:
        db_table = 'host_image'

class ImageTag(models.Model):

    id = models.AutoField(db_column='id', primary_key=True)
    img_id = models.IntegerField(db_column='img_id', null=True, default=0)
    tag = models.CharField(db_column='tag', null=True, default='', max_length=255)

    class Meta:
        db_table = 'host_image_tag'

class HostInfo(models.Model):
    """
    HostInfo modle
    """
    id = models.AutoField(db_column=u'id', primary_key=True)
    ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"主机IP")
    network = models.CharField(max_length=32, blank=True, null=True,verbose_name=u"网段")
    gateway = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"网关")
    netmask = models.CharField(max_length=32, blank=True, null=True,verbose_name=u"掩码")
    fqdn = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"fqdn")
    network_card = models.CharField(max_length=1024, blank=True, null=True, verbose_name=u"网卡")
    mac = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"mac")
    os_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"操作系统")
    kernel = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"内核")
    cpu = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"cpu")
    memory = models.IntegerField(blank=True, null=True, verbose_name=u"内存")

    class Meta:
        db_table = 'host_info'

class HostPassword(models.Model):

    ip = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'host_hostpassword'
