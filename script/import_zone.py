#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-04-28
# Modify Date: 2017-04-28
#***************************************************************#

import os
import sys, time

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from host.aliyunapi.baseapi import AliyunZoneApi
from host.aliyunapi.ecsapi import AliyunECSApi
from asset.models import Room
from host.models import Hosts

def updateRoom():
    ecsapi = AliyunECSApi('cn-shanghai')
    page = 1
    pageSize = 50
    while True:
        res, result = ecsapi.getECSHostList(page, pageSize)
        page += 1
        if not res:
            break
        if len(result['results']) <= 0:
            break
        for h in result['results']:
            rooms = Room.objects.filter(zone_id=h['zone_id'])
            if len(rooms) <= 0:
                continue
            room = rooms[0]
            Hosts.objects.filter(aliyun_id=h['aliyun_id']).update(room_id=room.id, zone_id=h['zone_id'])

if __name__ == "__main__":
    aliyunapi = AliyunZoneApi()
    status, zonelist = aliyunapi.getAllZone()
    if status:
        for zone in zonelist:
            if len(Room.objects.filter(zone_id=zone['ZoneId'])) > 0:
                continue
            Room.objects.create(name=zone['ZoneId'], region_id=aliyunapi.regionId, zone_id=zone['ZoneId'], cn_name=zone['LocalName'], comment=zone['LocalName'], ctime=int(time.time()), state='online')
    updateRoom()

