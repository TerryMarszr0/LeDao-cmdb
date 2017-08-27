#!/bin/env python
import MySQLdb
import os
import json
import sys
import time, commands

HOST = sys.argv[2]
def exec_sql(sql):
	try:
		conn = MySQLdb.connect(host=HOST,user='zabbix',passwd='zabbix',port=3306)
		cur = conn.cursor()
		cur.execute(sql)
		res = cur.fetchall()[0][1]
		cur.close()
		conn.close()
		return res
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
query_sql="show status like 'Queries'"
uptime_sql="show status like 'Uptime'"
commit_sql="show global status like 'Com_commit'"
rollback_sql="show global status like 'Com_rollback'"
if not os.path.exists('/tmp/' + HOST + '_qps_result.txt'):
	result = {'query':0,'uptime':0,'commit':0,'rollback':0}
	os.mknod('/tmp/' + HOST + '_qps_result.txt')
	json.dump(result,open('/tmp/' + HOST + '_qps_result.txt','w'))
def get_qps():
    try:
        last = json.load(open('/tmp/' + HOST + '_qps_result.txt'))
    except ValueError:
        os.remove('/tmp/' + HOST + '_qps_result.txt')
        sys.exit()
    query_last = last['query']
    uptime_last = last['uptime']
    commit_last = last['commit']
    rollback_last = last['rollback']
    query = exec_sql(query_sql)
    uptime = exec_sql(uptime_sql)
    commit = exec_sql(commit_sql)
    rollback = exec_sql(rollback_sql)               
    delta_query = int(query) - int(query_last)
    delta_uptime = int(uptime) - int(uptime_last)
    qps = delta_query / delta_uptime
    delta_commit = int(commit) - int(commit_last)
    delta_rollback = int(rollback) - int(rollback_last)
    tps = ( delta_commit + delta_rollback ) / delta_uptime
    res_new = {'query':query,'uptime':uptime,'commit':commit,'rollback':rollback,'qps':qps,'tps':tps}
#	os.remove('/tmp/' + HOST + '_qps_result.txt')
    json.dump(res_new,open('/tmp/' + HOST + '_qps_result.txt','w'))




now = int(time.time())
last_mod = os.path.getmtime('/tmp/' + HOST + '_qps_result.txt')
if now - last_mod > 59:
	get_qps()
if sys.argv[1] == 'qps':
	get_res = json.load(open('/tmp/' + HOST + '_qps_result.txt'))
	print get_res['qps']
if sys.argv[1] == 'tps':
	get_res = json.load(open('/tmp/' + HOST + '_qps_result.txt'))
	print get_res['tps']

































