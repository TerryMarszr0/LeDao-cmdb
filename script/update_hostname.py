#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-05-19
# Modify Date: 2017-05-19
#***************************************************************#

import os
import sys

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from host.lib.host_tools import sshGetHostName
from host.models import Hosts
from asset.models import Conf


def updateConf():
    for h in Hosts.objects.all():
        if not h.cpu:
            continue
        if not h.memory:
            continue
        core = h.cpu
        mem = int(int(h.memory)/1000)
        conf = Conf.objects.filter(cpu=core, memory=mem)
        if len(conf) <= 0:
            continue
        conf = conf[0]
        Hosts.objects.filter(id=h.id).update(conf_id=conf.id)

def updateHostname():
    for h in Hosts.objects.all():
        status, hostname = sshGetHostName(h.ip)
        if not status:
            continue
        print status, hostname
        if hostname:
            Hosts.objects.filter(id=h.id).update(hostname=hostname)

if __name__ == "__main__":
    updateHostname()
    # updateConf()

