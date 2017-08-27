#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, commands

project_path = os.path.abspath('../..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()
import MySQLdb
import os
import json
import sys, time
from host.models import Hosts

query_sql="show status like 'Queries'"
uptime_sql="show status like 'Uptime'"
commit_sql="show global status like 'Com_commit'"
rollback_sql="show global status like 'Com_rollback'"
def exec_sql(sql, host):
	try:
		conn = MySQLdb.connect(host=host,user='zabbix',passwd='zabbix',port=3306)
		cur = conn.cursor()
		cur.execute(sql)
		res = cur.fetchall()[0][1]
		cur.close()
		conn.close()
		return res
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def get_qps(host):
    try:
        last = json.load(open('/tmp/' + host + '_qps_result.txt'))
    except ValueError:
        os.remove('/tmp/' + host + '_qps_result.txt')
        sys.exit()
    query_last = last['query']
    uptime_last = last['uptime']
    commit_last = last['commit']
    rollback_last = last['rollback']
    query = exec_sql(query_sql, host)
    uptime = exec_sql(uptime_sql, host)
    commit = exec_sql(commit_sql, host)
    rollback = exec_sql(rollback_sql, host)
    delta_query = int(query) - int(query_last)
    delta_uptime = int(uptime) - int(uptime_last)
    qps = delta_query / delta_uptime
    delta_commit = int(commit) - int(commit_last)
    delta_rollback = int(rollback) - int(rollback_last)
    tps = ( delta_commit + delta_rollback ) / delta_uptime
    res_new = {'query':query,'uptime':uptime,'commit':commit,'rollback':rollback,'qps':qps,'tps':tps}
    json.dump(res_new,open('/tmp/' + host + '_qps_result.txt','w'))


if __name__ == "__main__":
    zabbix_server = '10.1.20.28'
    for h in Hosts.objects.filter(attribute='RDS', state='online'):
        host = h.hostname

        try:
            if not os.path.exists('/tmp/' + host + '_qps_result.txt'):
                result = {'query':0,'uptime':0,'commit':0,'rollback':0}
                os.mknod('/tmp/' + host + '_qps_result.txt')
                json.dump(result,open('/tmp/' + host + '_qps_result.txt','w'))
            now = int(time.time())
            last_mod = os.path.getmtime('/tmp/' + host + '_qps_result.txt')
            if now - last_mod > 59:
                get_qps(host)
                get_res = json.load(open('/tmp/' + host + '_qps_result.txt'))
                command = 'zabbix_sender -s "' + host + '" -z ' + zabbix_server + ' -k "Mysql.qps" -o ' + str(get_res['qps'])
                status, output = commands.getstatusoutput(command)
                print status, output
                command = 'zabbix_sender -s "' + host + '" -z ' + zabbix_server + ' -k "Mysql.tps" -o ' + str(get_res['tps'])
                status, output = commands.getstatusoutput(command)
                print status, output
        except Exception, ex:
            print str(ex)

        status, output = commands.getstatusoutput("sh get_mysql_stats_wrapper.sh runnint-master " + host)
        print status, output
        if status != 0:
            print 'error'
            continue
        f = open('/tmp/' + host + '-mysql_cacti_stats.txt')
        for txt in f.readlines():
            for kv in txt.split(" "):
                kv_list = kv.split(':')
                if len(kv_list) != 2:
                    continue
                key = kv_list[0].replace("_", "-")
                value = kv_list[1]
                command = 'zabbix_sender -s "' + host + '" -z ' + zabbix_server + ' -k "MySQL.' + key + '" -o ' + value
                status, output = commands.getstatusoutput(command)
                print status, output
        f.close()
