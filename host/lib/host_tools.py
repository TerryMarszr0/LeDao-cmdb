# -*- coding: utf-8 -*-
import time, os, json
from host.models import Hosts, Image
from asset.models import AssetModel, Conf, Room, Rack
from app.models import AppService, ServiceHost
from cmdb import configs
from collections import defaultdict
from cmdb.configs import logger
import commands
from host.task.hosttask import ChangeHostnameTask
from django.forms.models import model_to_dict

class HostValidate():

    def checkAddHost(self, **kwargs):

        host = {}
        envs = []
        for c in Hosts.HOST_ENV_CHOICES:
            envs.append(c[0])
        types = []
        for t in Hosts.HOST_TYPE_CHOICES:
            types.append(t[0])
        attributes = []
        for a in Hosts.HOST_ATTRIBUTE_CHOCIES:
            attributes.append(a[0])
        ip = ''
        oobip = ''
        sn = ''
        mac = ''
        env = ''
        type = ''
        attribute = ''
        hostname = ''
        if kwargs.has_key('ip'):
            ip = kwargs['ip']
        if kwargs.has_key('oobip'):
            oobip = kwargs['oobip']
        if kwargs.has_key('sn'):
            sn = kwargs['sn']
        if kwargs.has_key('mac'):
            mac = kwargs['mac']
        if kwargs.has_key('env'):
            env = kwargs['env']
        if kwargs.has_key('type'):
            type = kwargs['type']
        if kwargs.has_key('attribute'):
            attribute = kwargs['attribute']
        if kwargs.has_key('hostname'):
            hostname = kwargs['hostname']
        aliyun_id = None
        if kwargs.has_key('aliyun_id'):
            aliyun_id = kwargs['aliyun_id']
        if aliyun_id:
            if len(Hosts.objects.filter(aliyun_id=aliyun_id).exclude(state='deleted')) > 0:
                return False, u'阿里云id已存在'
            host['aliyun_id'] = aliyun_id
        if ip:
            if len(Hosts.objects.filter(ip=ip).exclude(state='deleted')) > 0:
                return False, 'ip ' + ip + u' 已使用'
        else:
            return False, u'ip 不能为空'
        if hostname:
            if len(Hosts.objects.filter(hostname=hostname).exclude(state='deleted')) > 0:
                return False, u'主机名 ' + hostname + u' 重复'
            host['hostname'] = hostname
        else:
            return False, u'主机名不能为空'
        if oobip:
            host['oobip'] = oobip
            if len(Hosts.objects.filter(oobip=oobip).exclude(state='deleted')) > 0:
                return False, u'管理ip ' + oobip + u' 已经使用'
        if sn:
            host['sn'] = sn
            if len(Hosts.objects.filter(sn=sn).exclude(state='deleted')) > 0:
                return False, u'sn ' + sn + u' 已经存在'
        if mac:
            host['mac'] = mac
            if len(Hosts.objects.filter(oobip=oobip).exclude(state='deleted')) > 0:
                return False, u'mac ' + mac + u' 已经存在'
        if env not in envs:
            return False, u'env 必须为:' + " ".join(envs)
        if type not in types:
            return False, u'type 必须为:' + " ".join(types)
        if attribute not in attributes:
            return False, u'attribute 必须为:' + " ".join(attributes)
        host['ip'] = ip
        host['env'] = env
        host['type'] = type
        host['attribute'] = attribute
        if kwargs.has_key('os_name'):
            host['os_name'] = kwargs['os_name']
        if kwargs.has_key('cpu'):
            host['cpu'] = kwargs['cpu']
        if kwargs.has_key('memory'):
            host['memory'] = kwargs['memory']
        if kwargs.has_key('region_id'):
            host['region_id'] = kwargs['region_id']
        if kwargs.has_key('zone_id'):
            host['zone_id'] = kwargs['zone_id']
        if kwargs.has_key('amount'):
            host['amount'] = kwargs['amount']

        if kwargs.has_key('model') and kwargs['model']:
            model = AssetModel.objects.filter(name=kwargs['model'])
            if len(model) <= 0:
                return False, 'no this model:' + str(kwargs['model'])
            host['model_id'] = model[0].id
        if kwargs.has_key('conf') and kwargs['conf']:
            conf = Conf.objects.filter(name=kwargs['conf'])
            if len(conf) <= 0:
                return False, 'no this conf:' + str(kwargs['conf'])
            host['conf_id'] = conf[0].id
        if kwargs.has_key('room_name') and kwargs['room_name']:
            room = Room.objects.filter(name=kwargs['room_name'])
            if len(room) <= 0:
                return False, 'no this room:' + str(kwargs['room_name'])
            host['room_id'] = room[0].id
        if kwargs.has_key('rack_name') and kwargs['rack_name']:
            rack = Rack.objects.filter(name=kwargs['rack_name'])
            if len(rack) <= 0:
                return False, 'no this rack:' + str(kwargs['rack_name'])
            host['rack_id'] = rack[0].id
        if kwargs.has_key('image') and kwargs['image']:
            os = Image.objects.filter(name=kwargs['image'])
            if len(os) <= 0:
                return False, 'no this image:' + str(kwargs['image'])
            host['img_id'] = os[0].id
        if kwargs.has_key('service_name') and kwargs['service_name']:
            service_name = kwargs['service_name']
            service = AppService.objects.filter(name=service_name)
            if len(service) <= 0:
                return False, 'no this service:' + service_name
            host['service_id'] = service[0].id
        if not host.has_key('service_id') or not host['service_id']:
            if type == 'server':
                host['service_id'] = configs.FREE_SERVER_ID
            elif type == 'vm':
                host['service_id'] = configs.FREE_VM_ID
            else:
                host['service_id'] = 0
        if kwargs.has_key('parent_ip') and kwargs['parent_ip']:
            if host['type'] not in ('vm'):
                return False, 'only vm has parent'
            host = Hosts.objects.filter(ip=kwargs['parent_ip'])
            if len(host) <= 0:
                return False, 'no this server:' + str(kwargs['parent_ip'])
            host['pid'] = host[0].id
        host['state'] = 'offline'
        if host['service_id'] in (configs.FREE_SERVER_ID, configs.FREE_VM_ID):
            host['state'] = 'free'
        host['ctime'] = int(time.time())
        return True, host

    def formatHostList(self, hostlist):
        results = []
        conf_ids = []
        room_ids = []
        rack_ids = []
        service_ids = []
        img_ids = []
        hostids = []
        for h in hostlist:
            conf_ids.append(h['conf_id'])
            room_ids.append(h['room_id'])
            rack_ids.append(h['rack_id'])
            # service_ids.append(h['service_id'])
            img_ids.append(h['img_id'])
            hostids.append(h['id'])

        host_service = defaultdict(list)
        host_servicelist = defaultdict(list)
        for s in ServiceHost.objects.filter(host_id__in=hostids):
            host_service[s.host_id].append(s.service_id)
            service_ids.append(s.service_id)
            host_servicelist[s.host_id].append(model_to_dict(s))

        conf_dict = {}
        for conf in Conf.objects.filter(id__in=conf_ids):
            conf_dict[conf.id] = conf
        room_dict = {}
        for room in Room.objects.filter(id__in=room_ids):
            room_dict[room.id] = room
        rack_dict = {}
        for rack in Rack.objects.filter(id__in=rack_ids):
            rack_dict[rack.id] = rack
        group_dict = {}
        for group in AppService.objects.filter(id__in=service_ids):
            group_dict[group.id] = group
        img_dict = {}
        for os in Image.objects.filter(id__in=img_ids):
            img_dict[os.id] = os

        for h in hostlist:
            t = h
            t['conf_name'] = ''
            if conf_dict.has_key(h['conf_id']):
                t['conf_name'] = conf_dict[h['conf_id']].name
            t['room_name'] = ''
            t['room_cname'] = ''
            if room_dict.has_key(h['room_id']):
                t['room_name'] = room_dict[h['room_id']].name
                t['room_cname'] = room_dict[h['room_id']].cn_name
            t['rack_name'] = ''
            if rack_dict.has_key(h['rack_id']):
                t['rack_name'] = rack_dict[h['rack_id']].name
            t['service_name'] = []
            t['service_id'] = []
            if host_service.has_key(h['id']):
                servicelist = []
                t['service_id'] = host_service[h['id']]
                for sid in host_service[h['id']]:
                    if group_dict.has_key(sid):
                        servicelist.append(group_dict[sid].name)
                if len(servicelist) > 0:
                    t['service_name'] = servicelist
            t['img_name'] = ''
            if img_dict.has_key(h['img_id']):
                t['img_name'] = img_dict[h['img_id']].name
            t['host_service'] = host_servicelist.get(h['id'], [])
            results.append(t)
        return results

def sshChangeHostname(ip, hostname):
    if not ip or not hostname:
        return False, u'ip和hostname不能为空'
    command = 'ssh root@%s -o ConnectTimeout=2 "/usr/bin/python /opt/cmdb-script/change_hostname.py %s %s"' % (configs.FORTRESS_HOST, hostname, ip)
    logger.info(command)
    try:
        status, output = commands.getstatusoutput(command)
        if status != 0:
            logger.error(output)
            return False, output
        logger.info(output)
        result_dict = json.loads(output)[0]
        if result_dict['success'] == "true":
            msg = "change %s hostname to %s success" % (ip, hostname)
            logger.info(msg)
        else:
            msg = "change %s hostname to %s error: %s" % (ip, hostname, result_dict['msg'])
            logger.info(msg)
        return True, output
    except Exception, e:
        logger.error(str(e))
        return False, str(e)

def sshGetHostName(ip):
    if not ip:
        return False, u'ip不能为空'
    command = 'ssh root@%s -o ConnectTimeout=5 "/usr/bin/python /opt/cmdb-script/get_hostname.py %s"' % (configs.FORTRESS_HOST, ip)
    try:
        status, output = commands.getstatusoutput(command)
        if status != 0:
            logger.error(output)
            return False, output
        return True, output
    except Exception, e:
        logger.error(str(e))
        return False, str(e)

def autoHostName(cuser, id):
    if not id:
        return False, u'id不能为空'
    host = Hosts.objects.filter(id=id)
    if len(host) <= 0:
        return False, u'主机不存在'
    if host[0].env != 'test':
        return False, u'不是测试环境'
    servicehost = ServiceHost.objects.filter(host_id=host[0].id)
    if len(servicehost) <= 0:
        return False, u'找不到服务'
    service_id = servicehost[0].service_id
    service = AppService.objects.filter(id=service_id)
    if len(service) <= 0:
        return False, u'服务不存在'
    iplast = ''
    ip_list = host[0].ip.split(".")
    if len(ip_list) == 4:
        iplast = ip_list[3]

    # 主机名生成规则为:小写服务名称 + ip最后一位 + .mwee. + 环境
    hostname = service[0].name.lower().replace("_", "-") + str(iplast) + ".mwee." + host[0].env

    if hostname == host[0].hostname:
        return False, u'主机名与原来一致'
    if len(Hosts.objects.filter(hostname=hostname).exclude(state='deleted', id=id)) > 0:
        return False, u'主机名重复'
    host.update(hostname=hostname)
    try:
        ChangeHostnameTask().addTask(cuser, ip=host[0].ip, hostname=hostname)
    except Exception, ex:
        print str(ex)
    return True, 'succ'

def changeHostNameById(cuser, id, hostname):
    if not id:
        return False, u'id不能为空'
    host = Hosts.objects.filter(id=id)
    if len(host) <= 0:
        return False, u'主机不存在'
    if not hostname:
        return False, u'主机名不能为空'
    if hostname == host[0].hostname:
        return False, u'主机名与原来一致'
    if len(Hosts.objects.filter(hostname=hostname).exclude(state='deleted', id=id)) > 0:
        return False, u'主机名重复'
    old_host = model_to_dict(host[0])
    host.update(hostname=hostname)
    try:
        ChangeHostnameTask().addTask(cuser, ip=host[0].ip, hostname=hostname)
    except Exception, ex:
        print str(ex)
    return True, old_host
