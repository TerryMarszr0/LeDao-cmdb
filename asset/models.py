# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from host.models import Hosts

# Create your models here.

class Room(models.Model):
    STATE = (
        ('online', 'online'),
        ('offline', 'offline'),
    )
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', unique=True, null=True, max_length=100, default='')
    region_id = models.CharField(db_column='region_id', null=True, max_length=100, default='')
    zone_id = models.CharField(db_column='zone_id', null=True, max_length=100, default='')
    cn_name = models.CharField(db_column='cn_name', max_length=100, null=True, default='', unique=True)
    tag = models.CharField(db_column='tag', max_length=30, null=True, default='')
    comment = models.CharField(db_column='comment', max_length=255, null=True, default='')
    location = models.CharField(db_column='location', null=True, max_length=255, default='')
    state = models.CharField(db_column='state', max_length=30, choices=STATE, null=True, default='online')
    ctime = models.IntegerField(db_column='ctime', null=True, default=0)

    class Meta:
        db_table = 'asset_room'


class Rack(models.Model):
    TYPE = (
        (0, '刀片笼子'),
        (1, '机柜'),
    )
    STATE = (
        ('online', 'online'),
        ('offline', 'offline'),
    )
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=100, null=True, default='')
    height = models.IntegerField(db_column='height', default=24, null=True)
    type = models.IntegerField(db_column='type', null=True, default=1, choices=TYPE)
    room_id = models.IntegerField(Room, db_column='room_id', null=True, default=0)
    comment = models.CharField(db_column='comment', max_length=255, null=True, default='')
    state = models.CharField(db_column='state', max_length=30, choices=STATE, null=True, default='')
    ctime = models.IntegerField(db_column='ctime', null=True, default=0)

    class Meta:
        db_table = 'asset_rack'

class AssetModel(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=100, null=True, default='', unique=True)
    size = models.IntegerField(db_column='size', null=True, default=0)
    firm_name = models.CharField(db_column='firm_name', max_length=255, null=True, default=0)
    comment = models.CharField(db_column='comment', max_length=255, null=True, default='')
    ctime = models.IntegerField(db_column='ctime', null=True, default=0)

    class Meta:
        db_table = 'asset_model'


class AssetType(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=100, null=True, default='')
    cn_name = models.CharField(db_column='cn_name', max_length=100, null=True, default='')
    comment = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'asset_type'


class Conf(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=60, null=True, default='')
    cpu = models.CharField(db_column='cpu', max_length=255, null=True, default='')
    disk = models.CharField(db_column='disk', max_length=255, null=True, default='')
    memory = models.CharField(db_column='memory', max_length=255, null=True, default='')
    raid = models.CharField(db_column='raid', max_length=255, null=True, default='')
    comment = models.CharField(db_column='comment', null=True, max_length=255, default='')
    ctime = models.IntegerField(db_column='ctime', null=True, default=0)

    class Meta:
        db_table = 'asset_conf'


class Network(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    room_id = models.IntegerField(null=False, default=0)
    env = models.CharField(max_length=30, choices=Hosts.HOST_ENV_CHOICES, null=False)
    network = models.CharField(max_length=30, null=False)
    mask = models.CharField(max_length=30, null=False)
    maskint = models.IntegerField(null=False, default=24)
    gateway = models.CharField(max_length=30, null=False)
    vlan = models.IntegerField(null=False, default=0)
    ctime = models.IntegerField(db_column='ctime', null=False, default=0)

    class Meta:
        db_table = 'asset_network'
        unique_together = ('network', 'maskint')


class IpAddress(models.Model):
    IP_STATE = (
        ('free', 'free'),
        ('used', 'used'),
        ('reserve', 'reserve'),
    )

    id = models.AutoField(db_column='id', primary_key=True)
    network_id = models.IntegerField(null=True, default=0)
    ip = models.CharField(max_length=30, null=True, default='', unique=True)
    state = models.CharField(max_length=30, null=True, default='')
    ctime = models.IntegerField(db_column='ctime', null=True, default=0)

    class Meta:
        db_table = 'asset_ipaddress'