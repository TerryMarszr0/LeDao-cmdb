#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: import_network.py
# Create Date: 2017-06-02
# Modify Date: 2017-06-02
#***************************************************************#

import os, sys, redis, requests, json, time

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from django.core.mail import send_mail
from public.redis.mq import MQ
from users.auth.ssoapi import login_sso
from fortress.libs.fortresslib import gen_keys
from host.aliyunapi.ecsapi import AliyunNetworkApi
from IPy import IP
from asset.models import Network, IpAddress, Room
from public.common.tools import exchange_maskint
from host.models import Hosts


def importAliyunNetwork():
    networkapi = AliyunNetworkApi()
    status, result = networkapi.getVpcList(1, 10)
    print result
    if not status:
        return False, result
    results = result['results']
    for r in results:
        page = 1
        while True:
            status, result = networkapi.getVSwitchList(r['VpcId'], page, 20)
            print result
            if not status:
                return status, result
            vswicths = result['results']
            if len(vswicths) <= 0:
                break
            page += 1
            for s in vswicths:
                cidrblock = s['CidrBlock']
                cidrblock_arr = cidrblock.split("/")
                if len(cidrblock_arr) != 2:
                    continue
                zoneid = s['ZoneId']
                room = Room.objects.filter(zone_id=zoneid)
                if len(room) <= 0:
                    continue
                room = room[0]
                mask = exchange_maskint(int(cidrblock_arr[1]))
                gateway_arr = cidrblock_arr[0].split(".")
                gateway_arr[3] = "255"
                current_time = int(time.time())
                if len(Network.objects.filter(network=cidrblock_arr[0], maskint=cidrblock_arr[1])) > 0:
                    continue
                obj = Network.objects.create(network=cidrblock_arr[0], maskint=cidrblock_arr[1], env='prod', room_id=room.id, mask=mask, gateway="0.0.0.0", vlan=gateway_arr[2], ctime=current_time)
                for ip in IP(cidrblock):
                    state = 'free'
                    if str(ip).endswith(".0") or str(ip).endswith(".255"):
                        state = 'reserve'
                    if len(Hosts.objects.filter(ip=ip)) > 0:
                        state = 'used'
                    IpAddress.objects.create(network_id=obj.id, ip=ip, ctime=current_time, state=state)


if __name__ == "__main__":
    importAliyunNetwork()