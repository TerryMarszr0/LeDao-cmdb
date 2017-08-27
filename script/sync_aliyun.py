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

from host.aliyunapi.ecsapi import importECS, delByAliyunId, AliyunECSApi
from host.aliyunapi.baseapi import import_img
from host.aliyunapi.slbapi import importSLB


if __name__ == "__main__":
    import_img()
    delByAliyunId()
    importECS()
    # updateHostname();
    importSLB()
    # print AliyunSLBApi().getAllSLBHost()