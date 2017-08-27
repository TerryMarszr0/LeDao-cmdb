#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-04-28
# Modify Date: 2017-04-28
#***************************************************************#

import os
import sys

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from host.aliyunapi.ecsapi import importECS
import xlrd
from app.models import App, AppService

def readAppService():
    fname = u"service.xlsx"
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        # sh = bk.sheet_by_name(u"平台汇总")
        sh = bk.sheet_by_index(0)
    except:
        print "no sheet in %s named Sheet1" % fname

    nrows = sh.nrows
    row_list = []
    for i in range(1, nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)
    return row_list

def importData(row_list):
    app_comment = ''
    app_name = ''
    service_name_list = ['free-server', 'free-vm', 'free-aliyun']
    for r in row_list:
        service_name_list.append(r[7].strip())
    for s in AppService.objects.all():
        if s.name not in service_name_list:
            print ('delete:' + s.name)
            AppService.objects.filter(id=s.id).delete()
    for r in row_list:
        if r[3] == u'简称':
            continue
        if r[0] != '':
            app_comment = r[0]
        if r[3] != '':
            app_name = r[3].strip()
        service_comment = r[6].strip()
        service_name = r[7].strip()
        app = App.objects.filter(name=app_name)
        if len(app) <= 0:
            app = App.objects.create(name=app_name, comment=app_comment)
        else:
            app = app[0]
        if len(AppService.objects.filter(name=service_name)) > 0:
            continue
        print service_name
        AppService.objects.create(app_id=app.id, name=service_name, comment=service_comment, type='java')

def readApp():
    fname = u"appservice.xlsx"
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_index(0)
    except:
        print "no sheet in %s named Sheet1" % fname

    nrows = sh.nrows
    row_list = []
    for i in range(1, nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)
    return row_list

def importApp(app_list):
    for a in app_list:
        if len(a) != 2:
            continue
        a[0] = a[0].strip()
        a[1] = a[1].strip()
        app = App.objects.filter(name=a[1])
        if len(app) > 0:
            continue
        App.objects.create(name=a[1], comment=a[0])

def updateServiceApp():
    for s in AppService.objects.all():
        name_arr = s.name.split("_")
        app = App.objects.filter(name=name_arr[0])
        if len(app) > 0:
            AppService.objects.filter(id=s.id).update(app_id=app[0].id)

def updateAppName():
    for a in App.objects.all():
        App.objects.filter(id=a.id).update(name=a.name.strip(), comment=a.comment.strip())

    for s in AppService.objects.all():
        AppService.objects.filter(id=s.id).update(name=s.name.strip())

if __name__ == "__main__":
    # row_list = readAppService()
    # importData(row_list)

    updateAppName()
    row_list = readApp()
    importApp(row_list)
    updateServiceApp()