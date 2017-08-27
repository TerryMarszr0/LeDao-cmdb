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
import django, uuid, time, json
django.setup()

from host.models import Hosts, Asset
from change.models import Change
from django.forms.models import model_to_dict
from app.models import ServiceHost

ASSET_TYPE = (
    (1, u"物理机"),
    (2, u"虚拟机"),
    (3, u"交换机"),
    (4, u"路由器"),
    (5, u"防火墙"),
    (6, u"Docker"),
    (7, u"其他")
    )

ASSET_ENV = (
    (1, U'生产环境'),
    (2, U'测试环境')
    )

if __name__ == "__main__":

    for a in Asset.objects.using('jumpserver').all():
        if a.ip.startswith("10.0.") and len(Hosts.objects.filter(ip=a.ip)) <= 0:
            type = 'other'
            attribute = 'other'
            service_id = 0
            if a.asset_type == 1:
                type = 'server'
                attribute = 'server'
                service_id = 1
            elif a.asset_type == 2:
                type = 'vm'
                attribute = 'xen'
                service_id = 2
            elif a.asset_type == 3:
                type = 'net'
                attribute = 'switch'
            memory = ''
            if a.memory:
                memory += a.memory + "G"
            os_name = ''
            if a.system_type:
                os_name += a.system_type
            if a.system_version:
                os_name += " " + a.system_version
            if a.system_arch:
                os_name += " " + a.system_arch
            env = ''
            if a.env == 1:
                env = 'prod'
            elif a.env == 2:
                env = 'test'
            _host = Hosts.objects.create(ip=a.ip, instance_id=str(uuid.uuid1()), hostname=a.hostname, env=env, type=type, attribute=attribute, ctime=int(time.time()),
                                     service_id=service_id, cpu=a.cpu, memory=memory, mac=a.mac, os_name=os_name, amount=a.money)
            ServiceHost.objects.create(service_id=_host.service_id, host_id=_host.id)
            Change.objects.create(uuid=str(uuid.uuid1()), username='admin', resource='host_hosts', res_id=_host.id, action='create',
                                  index=_host.ip, message=json.dumps(model_to_dict(_host)), change_time=int(time.time()), ctime=int(time.time()))
        else:
            h = Hosts.objects.filter(ip=a.ip)
            if len(h) == 1:
                h.update(hostname=a.hostname, amount=a.money)
                _host = h[0]
                Change.objects.create(uuid=str(uuid.uuid1()), username='admin', resource='host_hosts', res_id=_host.id, action='update',
                                  index=_host.ip, message=json.dumps(model_to_dict(_host)), change_time=int(time.time()), ctime=int(time.time()))
