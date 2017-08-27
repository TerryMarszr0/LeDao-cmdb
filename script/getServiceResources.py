# -*- coding:utf-8 -*-
import os
import sys

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

import json, requests
import heapq
import time
import datetime

from app.models import ServiceHost, AppService, ServiceResource
from host.models import Hosts


class ZabbixBase:
    def __init__(self, url="http://alizabbix.mwbyd.cn/api_jsonrpc.php"):
        self.url = url
        self.status = False
        self.header = {"Content-Type": "application/json"}
        self.api_data = {
            'jsonrpc': '2.0',
            'method': '',
            'params': '',
            'id': 0
        }
        self._set_auth_session()

    def _set_auth_session(self):
        self.api_data['method'] = 'user.login'
        self.api_data['params'] = {
            'user': "zabbixapi",
            'password': "RJ45^8#fe@pnd"
        }
        status, response = self._request()
        if status:
            self.status = True
            self.api_data['auth'] = response['result']
            self.api_data['id'] = 1
        else:
            print response

    def _request(self):
        try:
            post_data = json.dumps(self.api_data)
            response = requests.post(self.url, data=post_data, headers=self.header)

            result_body = json.loads(response.text)
            if result_body.has_key('error'):
                return False, result_body['error']['data']
            return True, result_body
        except Exception as ex:
            return False, str(ex)

    def execute(self, method, params):
        self.api_data['method'] = method
        self.api_data['params'] = params
        return self._request()

class ZabbixAPi(ZabbixBase):

    def getHistory(self, history=0, itemids=[], limit=1000):
        method = 'history.get'
        params = {
            "output": "extend",
            "history": history,
            "itemids": itemids,
            'limit': limit,
        }
        return self.execute(method, params)

    def getOneDayHistory(self, history=0, itemids=[], time_from = 0, time_till = 0):
        method = 'history.get'
        params = {
            "output": "extend",
            "history": history,
            "itemids": itemids,
            "time_from": time_from,
            "time_till": time_till
        }
        return self.execute(method, params)

    # 获取 hostid
    def getHost(self):
        method = 'host.get'
        params = {
            "output": "extend"
        }
        return self.execute(method, params)

    def getItem(self, hostids=[], key='system'):
        method = 'item.get'
        params = {
        "output": "extend",
        "hostids": hostids,
        "search": {
            "key_": key
        },
        "sortfield": "name"
        }
        return self.execute(method, params)

class ResourcesStatistics:
    za = None
    hostid_list = []
    ip_hostid_dict = {}
    Resources = {}
    time_from = 0
    time_till = 0


    def __init__(self):
        #初始化时间戳
        cur_time = int(time.time())
        self.time_till = cur_time - (cur_time + 28800) % 86400 # 获取今天凌晨的时间戳
        self.time_from = self.time_till - 86400  # 获取昨天凌晨的时间戳
        self.za = ZabbixAPi()

        for host in self.za.getHost()[1]['result']:
            if host['status'] == '0':
                self.hostid_list.append(host['hostid'])
                self.ip_hostid_dict[host['name']] = host['hostid']

    def getResultOneDay(self, ip_list, name, zabbix_key=""):
        # 获取服务对应的 ip_list --> host_id_list
        self.hostid_list = []
        for ip in ip_list:
            if self.ip_hostid_dict.has_key(ip):
                self.hostid_list.append(self.ip_hostid_dict[ip])
        if len(self.hostid_list) == 0:
            self.Resources[name] = 0
            return None
        print(self.hostid_list)
        matrix = [None] * 1441  # 初始化矩阵
        for i in range(len(matrix)):
            matrix[i] = [] * 1
        #################################################### memory ####################################################
        if name == "memory":
            for hostid in self.hostid_list: # 每个服务器的使用情况（内存 = 总量 - 空闲 ）
                total_memory_item = self.za.getItem(hostid, "vm.memory.size[total]")[1]['result']
                if total_memory_item:
                    total_memory_type = total_memory_item[0]['value_type']
                    print(total_memory_item[0]['itemid'])
                    total_memory_result = self.za.getHistory(total_memory_type, total_memory_item[0]['itemid'], 1)[1]['result']
                    if total_memory_result:
                        total_memory = total_memory_result[0]['value']

                        free_memory_item = self.za.getItem(hostid, "vm.memory.size[free]")[1]['result']    # 因为该 hostid 的total_memory存在所以，free_memory一定存在
                        free_memory_type = free_memory_item[0]['value_type']
                        free_memory_result = self.za.getOneDayHistory(free_memory_type, free_memory_item[0]['itemid'], self.time_from, self.time_till)[1]['result']
                        for free_memory in free_memory_result:
                            index = (int(free_memory['clock']) - self.time_from) / 60
                            matrix[index].append(float(total_memory) - float(free_memory['value']))

        ####################################################非 memory###################################################
        else:
            itemid_list = []
            itemResultList = self.za.getItem(self.hostid_list, zabbix_key)[1]['result']
            if itemResultList:
                value_type = itemResultList[0]['value_type']

                for item in itemResultList:
                    itemid_list.append(item['itemid'])
                print(itemid_list)
                # 遍历item结果集
                for itemid in itemid_list:
                    result = self.za.getOneDayHistory(value_type, itemid, self.time_from, self.time_till)[1]['result']
                    if result:
                        for r in result:
                            index = (int(r['clock']) - self.time_from) / 60
                            if name == 'cpu_usage_rate':
                                matrix[index].append(100.0 - float(r['value']))
                            else:
                                matrix[index].append(float(r['value']))
        ################################################################################################################
        # 求每分钟的数据峰值，最小值, 平均值
        for i in range(1440):
            lenth = len(matrix[i])
            if lenth > 0:
                sum = 0.0
                heap = []
                for j in range(lenth):
                    sum += matrix[i][j]
                    heapq.heappush(heap, float(matrix[i][j]))
                avg = float('%.4f' % (sum/lenth))

                peak_sum = 0.0
                valley_sum = 0.0
                # 最大前10%
                peak_list = heapq.nlargest(lenth / 10 + 1, heap)
                for peak in peak_list:
                    peak_sum += peak
                max = float('%.4f' % (peak_sum/len(peak_list)))

                # 最大前10%
                valley_list = heapq.nsmallest(lenth / 10 + 1, heap)
                for valley in valley_list:
                    valley_sum += valley
                min = float('%.4f' % (valley_sum / len(valley_list)))

                matrix[i] = [max,min,avg]
            else:
                matrix[i] = [0.0, 0.0, 0.0]

        # 通过每分钟的数据统计出一天的最大值，最小值，平均值
        heap = []
        sum = 0.0
        for i in range(1440):
            heapq.heappush(heap, float(matrix[i][0]))
            heapq.heappush(heap, float(matrix[i][1]))
            sum += float(matrix[i][2])
        max_oneday = heapq.nlargest(1, heap)
        min_oneday = heapq.nsmallest(1, heap)
        avg_oneday = float('%.4f' % (sum / 1440))

        matrix_oneday = [max_oneday[0],min_oneday[0],avg_oneday]
        self.Resources[name] = matrix_oneday

def get_services_ips():
    result = {}
    # 获取服务id列表
    service_id_list = []
    service_host_list = ServiceHost.objects.all()
    for service_host in service_host_list:
        service_id_list.append(service_host.service_id)
    service_id_list = list(set(service_id_list))

    # 获取服务名称：[hostip] 对应关系
    for service_id in service_id_list:
        app_services = AppService.objects.filter(id=service_id)
        if len(app_services):
            key = app_services[0].name
        else:
            continue
        service_hosts = ServiceHost.objects.filter(service_id=service_id)
        host_ip_list = []
        for service_host in service_hosts:
            hosts = Hosts.objects.filter(id=service_host.host_id)
            if len(hosts) and hosts[0].env == "prod":
                host_ip_list.append(hosts[0].ip)

        result[key] = host_ip_list
    return result

def getData():
    services_ip_dict = get_services_ips()
    Data = {}
    Rs = ResourcesStatistics()
    print(Rs.time_from, Rs.time_till)
    count = 0
    for service, ip_list in services_ip_dict.items():
        count += 1
        print(service,count)
        Rs.Resources = {}
        Rs.getResultOneDay(ip_list, 'cpu_usage_rate', 'system.cpu.util[,idle]')  # cpu 使用率
        Rs.getResultOneDay(ip_list, 'cpu_load', 'system.cpu.load[percpu,avg1]')  # cpu 负载
        Rs.getResultOneDay(ip_list, 'memory')  # 内存使用
        Rs.getResultOneDay(ip_list, 'net_in', 'net.if.in[eth0]')  # 入流量
        Rs.getResultOneDay(ip_list, 'net_out', 'net.if.out[eth0]')  # 出流量
        Data[service] = Rs.Resources
    return Rs.time_from, Data


if __name__ == "__main__":
    time, data = getData()
    for service, resource in data.items():
        for key, value in resource.items():
            if value:
                ServiceResource.objects.create(service=service, key=key, max=value[0], min=value[1], avg=value[2],ctime=time)
