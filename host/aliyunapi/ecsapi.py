# -*- coding: utf-8 -*-
import json, time, uuid
from host.aliyunapi.baseapi import AliyunBase
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeVpcsRequest, DescribeVSwitchesRequest, CreateInstanceRequest, DescribeInstanceTypesRequest
from host.lib.host_tools import HostValidate
from host.models import Hosts, HostDeleted, Image
from asset.models import Room
from change.models import Change
from django.forms.models import model_to_dict
from app.models import ServiceHost
from host.lib.host_tools import sshGetHostName
from asset.models import IpAddress, Conf
from host.task.hosttask import DelMonitorTask
from cmdb.configs import logger

class AliyunECSApi(AliyunBase):

    """
    创建ECS实例

    zoneId:可用区id
    imageId:镜像id
    instanceType:实例规格
    vSwitchId:专有网络虚拟机交换机id
    securityGroupId:安全组id(sg-11ebjahpj)
    internetChargeType:网络计费类型(PayByBandwidth,PayByTraffic)
    instanceChargeType:实例计费类型(PrePaid：预付费;PostPaid：后付费,按量付费)
    period:实例购买时长
    autoRenew:是否自动续费
    autoRenewPeriod:自动续费时长(1|2|3|6|12)
    systemDiskCategory:系统盘的磁盘种类()
    """
    def createECS(self, zoneId, imageId, instanceType, vSwitchId, securityGroupId, internetChargeType, instanceChargeType):
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_ZoneId(zoneId)
        request.set_ImageId(imageId)
        request.set_InstanceType(instanceType)
        request.set_SecurityGroupId(securityGroupId)
        request.set_InternetChargeType(internetChargeType)
        request.set_InstanceChargeType(instanceChargeType)

        request.set_SystemDiskCategory()

    # 获取区域下的ecs实例列表
    def getInstanceList(self, pageNumber, pageSize):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageNumber(pageNumber)
        request.set_PageSize(pageSize)
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            data = {'count': result['TotalCount'], 'results': result['Instances']['Instance']}
            return True, data
        except Exception, ex:
            return False, str(ex)

    # 根据实例id获取实例信息
    def getInstanceListByID(self, instanceIds):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageSize(100)
        request.set_InstanceIds(json.dumps(instanceIds))
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
        host_list = self.changeToHost(result)
        return status, host_list

    def changeToHost(self, ecs_list):
        host_list = []
        room_dict = {}
        for room in Room.objects.all():
            if room.region_id:
                room_dict[room.region_id] = room
        for e in ecs_list:
            host = {}
            host['hostname'] = e['InstanceName']
            host['imageId'] = e['ImageId']
            if len(e['VpcAttributes']['PrivateIpAddress']['IpAddress']) > 0:
                host['ip'] = e['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
            else:
                host['ip'] = ''
            host['type'] = 'aliyun'
            host['attribute'] = 'ECS'
            host['env'] = 'prod'
            host['publicip'] = ",".join(e['PublicIpAddress']['IpAddress'])
            host['state'] = 'free'
            host['ctime'] = int(time.mktime(time.strptime(e['CreationTime'], '%Y-%m-%dT%H:%MZ')))
            host['shiptime'] = int(time.mktime(time.strptime(e['CreationTime'], '%Y-%m-%dT%H:%MZ')))
            host['expiration_time'] = int(time.mktime(time.strptime(e['ExpiredTime'], '%Y-%m-%dT%H:%MZ')))
            host['aliyun_id'] = e['InstanceId']
            host['cpu'] = e['Cpu']
            host['memory'] = e['Memory']
            host['region_id'] = e['RegionId']
            host['zone_id'] = e['ZoneId']
            host['os_name'] = e['OSName']
            if room_dict.has_key(host['region_id']):
                host['room_name'] = room_dict[host['region_id']].name
            host_list.append(host)
        return host_list

class AliyunNetworkApi(AliyunBase):

    def getVpcList(self, pageNumber, pageSize):
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_PageNumber(pageNumber)
        request.set_PageSize(pageSize)
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            data = {'count': result['TotalCount'], 'results': result['Vpcs']['Vpc']}
            return True, data
        except Exception, ex:
            return False, str(ex)

    def getVSwitchList(self, vpcid, pageNumber, pageSize):
        request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        request.set_VpcId(vpcid)
        request.set_PageNumber(pageNumber)
        request.set_PageSize(pageSize)
        request.set_accept_format('json')
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            data = {'count': result['TotalCount'], 'results': result['VSwitches']['VSwitch']}
            return True, data
        except Exception, ex:
            return False, str(ex)

class AliyunECSTypes(AliyunBase):

    def getAllTypes(self):
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        try:
            result = self.clt.do_action_with_exception(request)
            result = json.loads(result)
            data = result['InstanceTypes']['InstanceType']
            return True, data
        except Exception, ex:
            return False, str(ex)

def importECS():
    ecsapi = AliyunECSApi('cn-shanghai')
    page = 1
    pageSize = 50
    count = 0
    while True:
        res, result = ecsapi.getECSHostList(page, pageSize)
        page += 1
        if not res:
            return res, result
        if len(result['results']) <= 0:
            break
        iplist = []
        for h in result['results']:
            res, host = HostValidate().checkAddHost(**h)
            if not res:
                continue
            imageId = h['imageId']
            images = Image.objects.filter(image_id=imageId)
            if len(images) > 0:
                host['img_id'] = images[0].id
            host['ctime'] = int(time.time())
            host['instance_id'] = str(uuid.uuid1())

            try:
                core = host['cpu']
                mem = int(int(host['memory'])/1000)
                conf = Conf.objects.filter(cpu=core, memory=mem)
                if len(conf) > 0:
                    conf = conf[0]
                    host['conf_id'] = conf.id
            except Exception, ex:
                print str(ex)

            # 获取主机名
            status, hostname = sshGetHostName(host['ip'])
            if status:
                host['hostname'] = hostname

            _host = Hosts.objects.create(**host)
            ServiceHost.objects.create(service_id=_host.service_id, host_id=_host.id)
            iplist.append(_host.ip)
            count += 1
        ################### 将ip设置为已使用 ###################
        if len(iplist) > 0:
            IpAddress.objects.filter(ip__in=iplist).update(state='used')
        ################### 将ip设置为已使用 ###################

    return True, count

def updateHostname():
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
            Hosts.objects.filter(aliyun_id=h['aliyun_id']).update(hostname=h['hostname'])

def delHost(aliyunids, ecsapi):
    idlist = []
    status, result = ecsapi.getECSHostListByID(aliyunids)
    if not status:
        return
    for h in result:
        idlist.append(h['aliyun_id'])
    delid = list(set(aliyunids) ^ set(idlist))
    if len(delid) > 0:
        delHostList = Hosts.objects.filter(aliyun_id__in=delid)
        hostids = []
        iplist = []
        for delhost in delHostList:
            ###################### 删除主机的时候删除对应的监控 ######################
            try:
                DelMonitorTask().addTask('script', ip=delhost.ip)
            except Exception, ex:
                logger.error(str(ex))
            ###################### 删除主机的时候删除对应监控 ######################
            iplist.append(delhost.ip)
            HostDeleted.objects.create(**model_to_dict(delhost))
            hostids.append(delhost.id)
        ServiceHost.objects.filter(host_id__in=hostids).delete()
        ################### 将ip设置为空闲 ###################
        if len(iplist) > 0:
            IpAddress.objects.filter(ip__in=iplist).update(state='free')
        ################### 将ip设置为空闲 ###################
        delHostList.delete()
    print delid

# 根据阿里云id删除不用的阿里云主机(只删除unuse和free状态的主机)
def delByAliyunId():
    aliyunids = []
    ecsapi = AliyunECSApi()
    for h in Hosts.objects.filter(attribute='ECS', state__in=('unuse', 'free')):
        aliyunids.append(h.aliyun_id)
        if len(aliyunids) == 100:
            delHost(aliyunids, ecsapi)
            aliyunids = []
    delHost(aliyunids, ecsapi)