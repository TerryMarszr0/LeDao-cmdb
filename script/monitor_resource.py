# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: update_principals.py
# Create Date: 2017-07-20
# Modify Date: 2017-07-20
# ***************************************************************#
import logging
import os
import sys

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

import json, requests

def getHostInfo():
    HostList = []
    url = 'http://cmdb.mwbyd.cn/api/host/host/'
    r = requests.get(url)
    result_json = r.json()
    count = 0
    while count != result_json['count']:
        url = url if count == 0 else result_json['next']
        r = requests.get(url)
        result_json = r.json()

        result = result_json['results']
        for host in result:
            HostList.append(host)
            count += 1
    return HostList

def getImageInfo():
    ImageList = []
    url = 'http://cmdb.mwbyd.cn/api/host/image/'
    r = requests.get(url)
    result_json = r.json()
    count = 0
    while count != result_json['count']:
        url = url if count == 0 else result_json['next']
        r = requests.get(url)
        result_json = r.json()

        result = result_json['results']
        for image in result:
            ImageList.append(image)
            count += 1
    return ImageList

def monitorResource():

    hosts = getHostInfo()
    images = getImageInfo()
    image_name_test = []
    image_name_uat = []

    for host in hosts:
        if (host['env'] == "test" and host['state'] == "free"):
            image_name_test.append(host['img_name'])
        if (host['env'] == "uat" and host['state'] == "free"):
            image_name_uat.append(host['img_name'])

    image_name_test_set = list(set(image_name_test))
    image_name_uat_set = list(set(image_name_uat))
    for it in image_name_test_set:
        if image_name_test.count(it) < 2:
            alertName = u'测试环境资源池报警'
            content = u'测试环境资源池中模板 ' + it + u' 机器少于2台'
            alarm(alertName, content)

    for iu in image_name_uat_set:
        if image_name_uat.count(iu) < 2:
            alertName = u'集成测试环境资源池报警'
            content = u'集成测试环境资源池中模板 ' + iu + u' 机器少于2台'
            alarm(alertName, content)


def alarm(alertName, content):
    try:
        token = '3066c0ad-75aa-4934-a7e4-7a32e6392748-b7'
        url = 'http://alarm.mwbyd.cn/api/remotealert/fire'
        appId = 103

        serviceName = "RDPOPS_cmdb"

        params = {}
        params['token'] = token
        params['appId'] = appId
        params['serviceName'] = serviceName
        params['alertName'] = alertName
        params['category'] = 4
        params['alertContent'] = content

        logging.info(content)

        response = requests.post(url, data=json.dumps(params), headers={"Content-Type": "application/json"})
        print response.text
        logging.info(response.text)
        data = json.loads(response.text)
        if data['success'] == True:
            return True, 'succ'
        return False, data['msg']
    except Exception, ex:
        logging.error(str(ex))
        return False, str(ex)


if __name__ == "__main__":
    monitorResource()
