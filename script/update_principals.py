# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: update_principals.py
# Create Date: 2017-07-20
# Modify Date: 2017-07-20
# ***************************************************************#
import os
import sys

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

import json, requests
from app.models import AppService, ServicePrincipals
from cmdb import configs



def updatePrincipals():
    url = configs.AUTO_DOMAIN + '/gateway/deploy/queryCMDBServiceUser'

    for service in AppService.objects.all():

        principals = ServicePrincipals.objects.filter(service_id=service.id)
        if len(principals) != 0:
            principals.delete()

        data = json.dumps(
            {'token': configs.AUTO_TOKEN, 'cmdbServiceName': service.name, 'env': 2})
        r = requests.post(url, data)         # 访问远哥接口，获取服务负责人信息（data 有格式要求）
        result_json = r.json()
        if not result_json:
            break
        if result_json['result'] == 'error':
            continue

        user_list = result_json['result']['userList']
        users = []
        for user in user_list:
            users.append(user['name'])
        users = list(set(users))
        for user_name in users:
            ServicePrincipals.objects.create(service_id=service.id, user_name=user_name)


if __name__ == "__main__":
    updatePrincipals()


