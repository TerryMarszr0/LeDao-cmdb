#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: stats_service_util.py
# Create Date: 2017-07-03
# Modify Date: 2017-07-03
#***************************************************************#

import os
import sys

project_path = os.path.abspath('../..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from public.common.mysqldb import DBOP
from host.models import Hosts

zabbixdb = '10.1.20.65'
dbuser = 'zabbix'
dbpassword = 'zabbix'
dbname = 'zabbix'
dbop = DBOP(zabbixdb, dbuser, dbpassword, dbname)

def get_interface(ip):
    sql = "select hostid, ip from interface where ip=%s"
    return dbop.getOne(sql, ip)


if __name__ == "__main__":
    for h in Hosts.objects.filter(env='prod'):
        get_interface(h.ip)