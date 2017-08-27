# -*- coding: utf-8 -*-
from django.db import models
from host.models import Hosts

class App(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=120, null=True, default='', unique=True)
    cname = models.CharField(max_length=120, null=True, default='')
    group = models.CharField(db_column='group', max_length=30, null=True, default='')
    comment = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'app_app'

# ----------------------------------------------------------------------------------------------------------------------
class AppPrincipals(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    app_id = models.IntegerField(db_column='app_id', null=True, default=0)
    user_name = models.CharField(db_column='user_name', max_length=120, null=True, default='')
    type = models.IntegerField(db_column='type', null=True, default=0, verbose_name=u"1 - 系统管理员  2 - 负责人")

    class Meta:
        db_table = 'app_app_principals'
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
class ServicePrincipals(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    service_id = models.IntegerField(db_column='service_id', null=True, default=0)
    user_name = models.CharField(db_column='user_name', max_length=120, null=True, default='')

    class Meta:
        db_table = 'app_service_principals'
# ----------------------------------------------------------------------------------------------------------------------
class AppService(models.Model):
    TYPE = (
        ('tomcat', 'tomcat'),
        ('dubbo', 'dubbo'),
        ('apache', 'apache'),
        ('nginx', 'nginx'),
        ('java', 'java'),
        ('php', 'php'),
        ('golang', 'golang'),
        ('python', 'python'),
        ('memcache', 'memcache'),
        ('mysql', 'mysql'),
        ('PostgreSQL', 'PostgreSQL'),
        ('redis', 'redis'),
        ('mongodb', 'mongodb'),
        ('nodejs', 'nodejs'),
        ('Gearman', 'Gearman'),
        ('ActiveMQ', 'ActiveMQ'),
        ('worker', 'worker'),
        ('zookeeper', 'zookeeper'),
        ('static', 'static'),
        ('other', 'other'),
    )
    STATE = (
        ('online', u'启用'),
        ('offline', u'禁用'),
    )
    id = models.AutoField(db_column='id', primary_key=True)
    app_id = models.IntegerField(db_column='app_id', null=True, default=0)
    name = models.CharField(db_column='name', unique=True, max_length=120, null=True, default='')
    type = models.CharField(db_column='type', max_length=30, choices=TYPE, null=True, default='other')
    comment = models.CharField(max_length=255, null=True, default='')
    vcs_rep = models.CharField(max_length=255, null=True, default='')
    state = models.CharField(max_length=30, choices=STATE, null=False, default='online')

    class Meta:
        db_table = 'app_service'

class AppSegment(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    app_id = models.IntegerField(db_column='app_id', null=True, default=0)
    segment = models.CharField(db_column='segment', max_length=60, null=True, default='')

    class Meta:
        db_table = 'app_appsegment'

class ServiceHost(models.Model):
    STATE = (
        ('Up', 'Up'),
        ('Down', 'Down'),
    )

    id = models.AutoField(db_column='id', primary_key=True , verbose_name='id' )
    service_id = models.IntegerField(db_column='service_id', null=True, default=0)
    host_id = models.IntegerField(db_column='host_id', null=True, default=0)
    state = models.CharField(max_length=30, null=False, choices=STATE, default='Down')

    class Meta:
        db_table = 'app_servicehost'
        unique_together = ('service_id', 'host_id')

####################################################################################################
class ServiceResource(models.Model):
    id = models.AutoField(db_column='id', primary_key=True , verbose_name='id' )
    service = models.CharField(db_column='service', max_length=50, null=True, default='')
    key = models.CharField(db_column='key', max_length=50, null=True, default='')
    max = models.FloatField(null=True, default=0)
    min = models.FloatField(null=True, default=0)
    avg = models.FloatField(null=True, default=0)
    ctime = models.BigIntegerField(null=True, default=0)
    class Meta:
        db_table = 'app_service_resource'
####################################################################################################


class Group(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=30, null=True, default='', unique=True)
    full_name = models.CharField(max_length=120, null=True, default='')
    owner = models.CharField(max_length=120, null=True, default='')
    comment = models.CharField(max_length=255, null=True, default='')

    class Meta:
        db_table = 'app_group'


# class UtilizationRate(models.Model):
#     id = models.AutoField(db_column='id', primary_key=True)
#     service_id = models.IntegerField(null=True, default=0)
#     load = models.FloatField(null=True, default=None)
#     cpu = models.FloatField(null=True, default=None)
#     memory = models.FloatField(null=True, default=None)
#     iops = models.FloatField(null=True, default=None)
#     qps = models.FloatField(null=True, default=None)
#     tps = models.FloatField(null=True, default=None)
#     ctime = models.IntegerField(null=True, default=0)
#
#     class Meta:
#         db_table = 'app_utilizationrate'

