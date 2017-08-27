#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, commands

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from host.monitorapi.zabbixapi import ZabbixAPi

if __name__ == "__main__":
    zabbix_server = '10.1.20.28'
    host = sys.argv[1]
    status, result = ZabbixAPi().getHostsByName(host)
    if status:
        if len(result['result']) <= 0:
            status, result = ZabbixAPi().addHost(host, '127.0.0.1', 0, groups=[88], templates=[12429])
            print status, result
    f = open('/tmp/' + host + '-mysql_cacti_stats.txt')
    for txt in f.readlines():
        for kv in txt.split(" "):
            kv_list = kv.split(':')
            if len(kv_list) != 2:
                continue
            key = kv_list[0].replace("_", "-")
            value = kv_list[1]
            command = 'zabbix_sender -s "' + host + '" -z ' + zabbix_server + ' -k "MySQL.' + key + '" -o ' + value + ' -r '
            status, output = commands.getstatusoutput(command)
            print status, output
    f.close()
