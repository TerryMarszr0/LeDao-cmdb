# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    pid = models.IntegerField(db_column='pid', null=False, default=0)
    name = models.CharField(db_column='name', max_length=120, null=True, default='', unique=True)
    path = models.CharField(max_length=360, null=True, default='')
    tag = models.CharField(max_length=120, null=True, default='')       # 标签
    weight = models.IntegerField(db_column='weight', null=True, default=0)     # 权重

    def has_child(self):              # 供菜单选择是生成树状菜单时使用
        return Menu.objects.filter(pid=self.id).count()

    def children(self):
        return Menu.objects.filter(pid=self.id)

    def superPermission(self):
        list = [u"系统管理"]
        return list

    def staffPermission(self):
        list = [u"查看业务线",u"授权审批",u"授权查询",u"任务查询"]
        return list

    class Meta:
        db_table = 'home_menu'

class GroupMenu(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    group_id = models.IntegerField(db_column='group_id', null=False, default=0)
    menu_id = models.CharField(db_column='menu_id', max_length=720, null=True, default='')

    class Meta:
        db_table = 'auth_group_menus'

class DefaultGroup(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    group_name = models.CharField(db_column='group_name', max_length=128, null=False, default='')

    class Meta:
        db_table = 'auth_default_group'
# Create your models here.
