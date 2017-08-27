# -*- coding: utf-8 -*-
import json, time, uuid
from baseapi import AliyunBase
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
# from host.lib.host_tools import HostValidate
# from host.models import Hosts


class AliyunRDSApi(AliyunBase):

    # 获取区域下的ecs实例列表
    def getInstanceList(self, pageNumber, pageSize):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_PageNumber(pageNumber)
        request.set_PageSize(pageSize)
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            print result
            result = json.loads(result)
            data = {'count': result['TotalRecordCount'], 'results': result['Items']['DBInstance']}
            return True, data
        except Exception, ex:
            return False, str(ex)

    # 根据实例id获取实例信息
    def getInstanceListByID(self, instanceIds):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_PageSize(100)
        request.set_InstanceIds(instanceIds)
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            return True, result['Instances']['Instance']
        except Exception, ex:
            return False, str(ex)

    def getECSHostList(self, pageNumber, pageSize):
        status, result = self.getInstanceList(pageNumber, pageSize)
        if not status:
            return status, result
        host_list = self.changeToHost(result['results'])
        result['results'] = host_list
        return status, result

    def getECSHostListByID(self, instanceIds):
        status, result = self.getInstanceListByID(instanceIds)
        if not status:
            return status, result
        host_list = self.changeToHost(result['results'])
        result['results'] = host_list
        return status, result

    def changeToHost(self, ecs_list):
        host_list = []
        for e in ecs_list:
            host = {}
            host['hostname'] = e['HostName']
            if len(e['VpcAttributes']['PrivateIpAddress']['IpAddress']) > 0:
                host['ip'] = e['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
            else:
                host['ip'] = ''
            host['type'] = 'aliyun'
            host['attribute'] = 'RDS'
            host['env'] = 'prod'
            host['publicip'] = ",".join(e['PublicIpAddress']['IpAddress'])
            host['state'] = 'free'
            host['ctime'] = int(time.mktime(time.strptime(e['CreationTime'], '%Y-%m-%dT%H:%MZ')))
            host['shiptime'] = int(time.mktime(time.strptime(e['CreationTime'], '%Y-%m-%dT%H:%MZ')))
            host['expiration_time'] = int(time.mktime(time.strptime(e['ExpiredTime'], '%Y-%m-%dT%H:%MZ')))
            host['aliyun_id'] = e['DBInstanceId']
            host['cpu'] = e['Cpu']
            host['memory'] = e['Memory']
            host['region_id'] = e['RegionId']
            host['os_name'] = e['OSName']
            host_list.append(host)
        return host_list