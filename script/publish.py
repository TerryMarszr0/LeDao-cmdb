#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-04-28
# Modify Date: 2017-04-28
#***************************************************************#

import os
import sys, json

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from public.redis.mq import Q
from cmdb import configs


if __name__ == "__main__":
    q = Q(configs.CMDB_TASK)
    q.push(json.dumps({'id': 1, 'task': 'fortress.task.fortresstask.AddFortressUserTask', 'params': json.dumps({'username': 'test899'})}))