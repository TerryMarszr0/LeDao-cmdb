#!/bin/python
# -*- coding: utf-8 -*-
import requests, os, re, statsd


def VPC_VlanIP_Check():
    VlanIPList = []
    url = 'http://cmdb.mwbyd.cn/api/asset/network/?format=json&order=asc&limit=20&offset=0&room_id=&env='
    r = requests.get(url)
    result_json = r.json()
    count = 0
    while count != result_json['count']:
        url = url if count == 0 else result_json['next']
        r = requests.get(url)
        result_json = r.json()

        result = result_json['results']
        for network in result:
            VlanIPList.append(network['network'])
            count += 1
    VlanIPList.sort()

    result_list = []
    for VlanIP in VlanIPList:
        ip, lost, delay_time = getPING(VlanIP)
        result = {}
        result['ip'] = ip
        result['lost'] = lost
        result['delay_time'] = delay_time
        result_list.append(result)
    return result_list


def getPING(VlanIP):
    arr = VlanIP.split('.')
    arr[3] = '253'
    IP = '.'.join(arr)
    order = 'ping -c 2 ' + IP
    p = os.popen(order)    # 利用这台机器 ping 其他的主机网关
    x = p.read()           # 将返回的数据放在 x 中
    regLost = r'\d+%'      # 正则表达式匹配丢包率
    regAverage = r'\d+\.\d+/.+ ms'  # 正则匹配延迟时间

    lost = re.search(regLost, x)
    average = re.search(regAverage, x)
    p.close()
    if lost:
        lost = lost.group()[0:]     # 用来提出分组截获的字符串
    if average:
        average = average.group()[0:]
    lost = None if lost == None else lost.split('%')[0]
    delay_time = None if average == None else average.split('/')[1]
    return IP, lost, delay_time


def getIp():
    order = 'ifconfig'
    p = os.popen(order)
    x = p.read()
    regIp = r'inet \d+\.\d+\.\d+\.\d+'
    Ip = re.search(regIp, x)
    p.close()
    ip = None if Ip == None else Ip.group().split(' ')[1]
    return ip


def changeSeparator(Ip):
    list = Ip.split('.')
    return '_'.join(list)


if __name__ == "__main__":
    localIp = changeSeparator(getIp())
    result_list = VPC_VlanIP_Check()
    c = statsd.StatsClient('127.0.0.1', 8125)
    for result in result_list:
        resultIp = changeSeparator(result['ip'])
        c.gauge(localIp + '__to__' + resultIp + '.loss_rate', result['lost'])
        c.gauge(localIp + '__to__' + resultIp + '.delay_time', result['delay_time'])

        print(localIp + '__to__' + resultIp + '.loss_rate', result['lost'])
        print(localIp + '__to__' + resultIp + '.delay_time', result['delay_time'])


