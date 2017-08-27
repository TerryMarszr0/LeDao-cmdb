#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-05-10
# Modify Date: 2017-05-10
#***************************************************************#

import os, sys, json, new
project_path = os.path.abspath('../..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from cmdb.configs import logger
from public.redis.mq import Q
from multiprocessing import Process
import importlib
from django.db import connection
from cmdb import configs

def run_task_job(queue_key):
    q = Q(queue_key)
    while True:
        ############### 解决mysql连接关闭的问题 ###############
        try:
            connection.close()
            print True
        except Exception, ex:
            print str(ex)
            logger.error(str(ex))
        ############### 解决mysql连接关闭的问题 ###############

        msg = q.pop()
        try:
            task_data = json.loads(msg[1])
            print task_data
            task = task_data['task']
            task_list = task.split(".")
            module = importlib.import_module(".".join(task_list[:-1]))
            reload(module)
            TaskClass = getattr(module, task_list[-1])
            obj = new.instance(TaskClass)
            obj.run(task_data['id'], **json.loads(task_data['params']))
        except Exception, ex:
            print str(ex)
            logger.error(str(ex))

if __name__ == "__main__":

    # run_task_job(configs.CMDB_TASK)
    # run_task_job(configs.ZABBIX_TASK)

    proc_record = []
    for i in range(5):
        p = Process(target=run_task_job, args=(configs.CMDB_TASK, ))
        p.start()
        proc_record.append(p)

    # 为了保证zabbix状态和cmdb一致,只能用一个进程执行zabbix异步任务
    p = Process(target=run_task_job, args=(configs.ZABBIX_TASK, ))
    p.start()
    proc_record.append(p)
    for p in proc_record:
        p.join()
