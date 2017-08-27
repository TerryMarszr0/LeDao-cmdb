# -*- coding: utf-8 -*-

from public.task.taskbase import Task
from cmdb import configs
from cmdb.configs import logger
import commands, json
from host.monitorapi.zabbixapi import ZabbixAPi, ALIYUN_TEMPLATE, IDC_TEMPLATE
from host.models import Hosts
from app.models import ServiceHost, AppService, App
from public.common.tools import get_segment_by_ip_mask, get_maskint_by_segment

class ChangeHostnameTask(Task):

    def excute(self, **kwargs):
        ip = kwargs.get('ip', '')
        hostname = kwargs.get('hostname', '')
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
            result_dict = json.loads(output)
            if result_dict['success']:
                msg = "change %s hostname to %s success" % (ip, hostname)
                logger.info(msg)
            else:
                msg = "change %s hostname to %s error: %s" % (ip, hostname, result_dict['msg'])
                logger.info(msg)
            return True, output
        except Exception, e:
            logger.error(str(e))
            return False, str(e)

class ChangeMonitorStateTask(Task):

    queue_key = configs.ZABBIX_TASK

    def excute(self, **kwargs):
        ip = kwargs.get('ip', '')
        state = kwargs.get('state', '')
        if not ip or not state:
            return False, u'ip和state不能为空'
        try:
            # 只监控online状态的主机
            if state in ('online', ):
                status = 0
            else:
                status = 1
            if type == 'aliyun':
                zabbixrestapi = ZabbixAPi()
            else:
                zabbixrestapi = ZabbixAPi(url=configs.ZABBIX_IDC_API_URL)
            res, output = zabbixrestapi.changeStatus(ip, status)
            return True, output
        except Exception, e:
            logger.error(str(e))
            return False, str(e)

class HostMonitorTask(Task):

    queue_key = configs.ZABBIX_TASK

    def excute(self, **kwargs):
        ip = kwargs.get('ip', '')
        state = kwargs.get('state', '')
        type = kwargs.get('type', '')
        attribute = kwargs.get('attribute', '')
        if not ip or not state or not type:
            return False, u'ip, type和state不能为空'

        ip_arr = ip.split(".")

        # 只监控online状态的主机
        if state in ('online', ):
            monitor_status = 0
        else:
            monitor_status = 1
        try:
            hosts = Hosts.objects.filter(ip=ip)
            if len(hosts) <= 0:
                return False, u'主机不存在'
            host = hosts[0]
            if type == 'aliyun':
                zabbixrestapi = ZabbixAPi()
            else:
                zabbixrestapi = ZabbixAPi(url=configs.ZABBIX_IDC_API_URL)

            ######################## 根据应用名称获取或创建组 ########################
            serviceids = []
            for s in ServiceHost.objects.filter(host_id=host.id):
                serviceids.append(s.service_id)
            appnames = []
            service_types = []
            appids = []
            for s in AppService.objects.filter(id__in=serviceids):
                appids.append(s.app_id)
                service_types.append(s.type)
            for a in App.objects.filter(id__in=appids):
                appnames.append(a.name)
            appnames = list(set(appnames))
            res, result = zabbixrestapi.getHostGroupsByName(*appnames)
            if not res:
                return False, result
            groupids = []
            groupnames = []
            for r in result['result']:
                groupnames.append(r['name'])
                groupids.append(r['groupid'])

            # 求服务名和查询出来的zabbix分组的差集,如果存在差集就新建组
            nocreate_groups = list(set(appnames).difference(set(groupnames)))
            if len(nocreate_groups) > 0:
                for g in nocreate_groups:
                    status, result = zabbixrestapi.createHostGroup(g)
                    if not status:
                        return False, result
                    groupids += result['result']['groupids']
            res, result = zabbixrestapi.getGroupByHost(*[ip])
            if not res:
                return False, result
            for allgroups in result['result']:
                for g in allgroups['groups']:
                    # 如果组名在cmdb的应用中找不到则说明是自己分配的组,需要保留
                    if len(App.objects.filter(name=g['name'])) <= 0:
                        groupids.append(g['groupid'])

            ######################## 根据应用名称获取或创建组 ########################

            ######################## 根据service类型获取监控模板id ########################
            tamplate_dict = IDC_TEMPLATE
            if type == 'aliyun':
                tamplate_dict = ALIYUN_TEMPLATE
            if str(ip_arr[2]) == "146":
                tamplateids = [tamplate_dict['default146']]
            else:
                tamplateids = [tamplate_dict['default']]
            for s in list(set(service_types)):
                if tamplate_dict.has_key(s):
                    tamplateids.append(tamplate_dict[s])
            tamplateids = list(set(tamplateids))
            ######################## 根据service类型获取监控模板id ########################

            ######################## 根据ip查询主机,如果不存在则创建主机，如果存在则修改主机组、模板和状态 ########################
            status, result = zabbixrestapi.getHostsByName(ip)
            if not status:
                return False, result
            if len(result['result']) <= 0:
                interface = ip
                if attribute == 'RDS':
                    interface = '127.0.0.1'
                    tamplateids = [12429]
                    proxyid = 0
                else:
                    if type == 'aliyun':
                        proxy_name = "zabbix_proxy_ali" + ip_arr[2]
                    else:
                        proxy_name = "zabbix_proxy" + ip_arr[2]
                    status, result = zabbixrestapi.getProxy(proxy_name)
                    if not status:
                        return False, result
                    proxyid = ''
                    if len(result['result']) > 0:
                        proxyid = result['result'][0]['proxyid']
                    if str(ip_arr[2]) == "146":
                        proxyid = 0

                status, result = zabbixrestapi.addHost(ip, interface, proxyid, groups=groupids, templates=tamplateids, status=monitor_status)
            else:
                if attribute == 'RDS':
                    tamplateids = [12429]
                status, result = zabbixrestapi.changeHost(ip, monitor_status, groups=groupids, templates=tamplateids)
            ######################## 根据ip查询主机,如果不存在则创建主机，如果存在则修改主机组、模板和状态 ########################

            if not status:
                return False, result
            return True, result
        except Exception, e:
            logger.error(str(e))
            return False, str(e)

class DelMonitorTask(Task):

    queue_key = configs.ZABBIX_TASK

    def excute(self, **kwargs):
        ip = kwargs.get('ip', '')
        if not ip:
            return False, u'ip不能为空'
        try:
            if type == 'aliyun':
                zabbixrestapi = ZabbixAPi()
            else:
                zabbixrestapi = ZabbixAPi(url=configs.ZABBIX_IDC_API_URL)
            res, output = zabbixrestapi.deleteHost(ip)
            return True, output
        except Exception, e:
            logger.error(str(e))
            return False, str(e)