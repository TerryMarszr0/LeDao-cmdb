#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-05-05
# Modify Date: 2017-05-05
#***************************************************************#

import os
import sys, re

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django, xlrd
django.setup()

import MySQLdb
from app.models import AppService, ServiceHost
from host.models import Hosts
from cmdb import configs


def get_iplist_from_walle(name):

    db = MySQLdb.connect("10.1.20.15", "walle", "www.Mwbyd91@", "walle")
    db.set_character_set('utf8')
    cursor = db.cursor()
    sql = "select hosts from project where name=%s"
    try:
        cursor.execute(sql, (name, ))
        results = cursor.fetchall()
        if len(results) <= 0:
            return False
        hosts = results[0]
        db.close()
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ip_list = []
        for _ip in reip.findall(hosts[0]):
            ip_list.append(_ip)
        return ip_list
    except Exception as ex:
        print str(ex)
        db.close()
        return False

def get_iplist_from_auto(name):
    db = MySQLdb.connect("10.1.26.36", "mwcmdb", "www.Mwbyd91@", "mw_auto_one")
    db.set_character_set('utf8')
    cursor = db.cursor()
    sql = "select c.ip from templates as a, template_zones as b, zones as c where a.id=b.template_id and b.zone_id=c.id and a.name=%s"
    try:
        cursor.execute(sql, (name, ))
        results = cursor.fetchall()
        if len(results) <= 0:
            return False
        db.close()
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ip_list = []
        for hosts in results:
            for _ip in reip.findall(hosts[0]):
                ip_list.append(_ip)
        return ip_list
    except Exception as ex:
        print str(ex)
        db.close()
        return False

def get_ip_env_from_auto():
    db = MySQLdb.connect("10.1.26.36", "mwcmdb", "www.Mwbyd91@", "mw_auto_one")
    db.set_character_set('utf8')
    cursor = db.cursor()
    sql = "select a.ip, b.env from zones as a,template_zones as b where b.zone_id=a.id"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) <= 0:
            return False
        db.close()
        return results
    except Exception as ex:
        print str(ex)
        db.close()
        return False

def readApp():
    fname = u"service.xlsx"
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        # sh = bk.sheet_by_name(u"Sheet1")
        sh = bk.sheet_by_index(0)
    except:
        print "no sheet in %s named Sheet1" % fname

    nrows = sh.nrows
    row_list = []
    for i in range(1, nrows):
        row_data = sh.row_values(i)
        row_list.append(row_data)
    return row_list

def sync_walle(r):
    service_name = r[7]
    sys = r[9]
    name = r[10]
    if not sys.lower().startswith('walle'):
        return
    service = AppService.objects.filter(name=service_name)
    if len(service) <= 0:
        return
    service = service[0]
    hosts = get_iplist_from_walle(name)
    if not hosts:
        return False
    for h in hosts:
        host = Hosts.objects.filter(ip=h)
        if len(host) <= 0:
            print h
            continue
        host = host[0]
        # print "ip:" + host.ip
        if len(ServiceHost.objects.filter(service_id=service.id, host_id=host.id)) <= 0:
            ServiceHost.objects.filter(host_id=host.id, service_id__in=(configs.FREE_ALIYUN_ID, configs.FREE_SERVER_ID, configs.FREE_VM_ID)).delete()
            ServiceHost.objects.create(service_id=service.id, host_id=host.id)
            Hosts.objects.filter(id=host.id).update(state='online', service_id=service.id)

def sync_auto(r):
    service_name = r[7]
    sys = r[9]
    name = r[10]
    if not sys.lower().startswith('auto'):
        return
    service = AppService.objects.filter(name=service_name)
    if len(service) <= 0:
        return
    service = service[0]
    hosts = get_iplist_from_auto(name)
    if not hosts:
        return False
    for h in hosts:
        host = Hosts.objects.filter(ip=h)
        if len(host) <= 0:
            print h
            continue
        host = host[0]
        # print "ip:" + host.ip
        if len(ServiceHost.objects.filter(service_id=service.id, host_id=host.id)) <= 0:
            ServiceHost.objects.filter(host_id=host.id, service_id__in=(configs.FREE_ALIYUN_ID, configs.FREE_SERVER_ID, configs.FREE_VM_ID)).delete()
            ServiceHost.objects.create(service_id=service.id, host_id=host.id)
            Hosts.objects.filter(id=host.id).update(state='online', service_id=service.id)
env_dict = {
    1: 'dev',
    2: 'test',
    3: 'uat',
    4: 'prod',
}

def sync_env_by_auto():
    results = get_ip_env_from_auto()
    if not results:
        return False
    for r in results:
        ip = r[0]
        env_code = r[1]
        if env_code == 0:
            continue
        Hosts.objects.filter(ip=ip).update(env=env_dict[env_code])
        print ip + "\t" + env_dict[env_code]

if __name__ == "__main__":
    row_list = readApp()
    for r in row_list:
        if r[9].lower().startswith('walle'):
            sync_walle(r)
        elif r[9].lower().startswith('auto'):
            sync_auto(r)
    sync_env_by_auto()