#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-04-28
# Modify Date: 2017-04-28
#***************************************************************#

import os
import sys

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from host.aliyunapi.ecsapi import AliyunECSApi
from host.aliyunapi.baseapi import import_img
from host.models import Image, Hosts
import time

def update_host_img():
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
            imageId = h['imageId']
            images = Image.objects.filter(image_id=imageId)
            if len(images) > 0:
                Hosts.objects.filter(aliyun_id=h['aliyun_id']).update(img_id=images[0].id)

if __name__ == "__main__":
    import_img()
    update_host_img()