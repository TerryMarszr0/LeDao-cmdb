# -*- coding: utf-8 -*-
import json, time, uuid
from host.aliyunapi.baseapi import AliyunBase
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from host.lib.host_tools import HostValidate
from host.models import Hosts
from django.db import transaction
from app.models import ServiceHost
from asset.models import Room


class AliyunSLBApi(AliyunBase):

    # 获取区域下的slb实例列表
    def getAllSLB(self):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            return True, result['LoadBalancers']['LoadBalancer']
        except Exception, ex:
            return False, str(ex)

    def getSLBByAddr(self, ip):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_Address(ip)
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            return True, result['LoadBalancers']['LoadBalancer']
        except Exception, ex:
            return False, str(ex)

    def getAllSLBHost(self):
        status, result = self.getAllSLB()
        if not status:
            return status, result
        host_list = self.changeToHost(result)
        return status, host_list

    def changeToHost(self, slb_list):
        host_list = []
        room_dict = {}
        for room in Room.objects.all():
            if room.region_id:
                room_dict[room.region_id] = room
        for e in slb_list:
            host = {}
            host['hostname'] = e['LoadBalancerName']
            host['ip'] = e['Address']
            host['type'] = 'aliyun'
            host['attribute'] = 'SLB'
            host['env'] = 'prod'
            host['state'] = 'free'
            host['ctime'] = int(time.time())
            host['aliyun_id'] = e['LoadBalancerId']
            host['region_id'] = e['RegionId']
            host['zone_id'] = e['MasterZoneId']
            if room_dict.has_key(host['region_id']):
                host['room_name'] = room_dict[host['region_id']].name
            host_list.append(host)
        return host_list

def importSLB():
    slbapi = AliyunSLBApi('cn-shanghai')
    res, result = slbapi.getAllSLBHost()
    if not res:
        return False
    if len(result) <= 0:
        return False
    for h in result:
        res, host = HostValidate().checkAddHost(**h)
        if not res:
            print (h['aliyun_id'] + ":" + host)
            continue
        host['ctime'] = int(time.time())
        host['instance_id'] = str(uuid.uuid1())
        _host = Hosts.objects.create(**host)
        print _host.ip
        ServiceHost.objects.create(service_id=_host.service_id, host_id=_host.id)

