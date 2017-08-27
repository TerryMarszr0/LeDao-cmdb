#!/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: sync_aliyun.py
# Create Date: 2017-04-28
# Modify Date: 2017-04-28
#***************************************************************#

import os, sys, redis, requests, json, base64, time

project_path = os.path.abspath('..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from django.core.mail import send_mail
from public.redis.mq import MQ
from users.auth.ssoapi import login_sso
from fortress.libs.fortresslib import gen_keys
from host.aliyunapi.ecsapi import AliyunNetworkApi, AliyunECSTypes
from host.monitorapi.zabbixapi import ZabbixAPi
from public.common.tools import get_segment_by_ip_mask, get_maskint_by_segment, exchange_maskint
from host.task.hosttask import DelMonitorTask
from app.auto.autoapi import GitLabApi
from OpenSSL.crypto import load_privatekey, load_publickey, FILETYPE_PEM, sign
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from public.common.tools import Prpcrypt
from cmdb import configs
from celery import Celery
from host.aliyunapi.slbapi import AliyunSLBApi


class prpcrypt():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC

    #加密函数，如果text不足16位就用空格补足为16位，
    #如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        #这里密钥key 长度必须为16（AES-128）,
        #24（AES-192）,或者32 （AES-256）Bytes 长度
        #目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

app = Celery('tasks', broker='redis://localhost//')
@app.task
def add(x, y):
    return x + y

if __name__ == "__main__":
    # send_mail('test', 'testttttt', 'zabbix@puscene.com', ['chen.shaodong@puscene.com'])
    # q = MQ('mytest')
    # q.publish('2343')
    # ls = q.subscribe()
    # for msg in ls:
    #     if msg['type'] == 'message':
    #         print msg['data']

    # print gen_keys('chen.shaodong@puscene.com')
    # print AliyunNetworkApi().getVpcList(1, 10)
    # print AliyunNetworkApi().getVSwitchList('vpc-114euhjuu', 1, 20)
    # status, result = AliyunECSTypes().getAllTypes()
    # if status:
    #     for r in result:
    #         print r
            # print r['InstanceTypeId'] + "\t" + str(r['CpuCoreCount']) + "\t"  + str(r['MemorySize'])
    # print ZabbixAPi().changeStatus('10.1.20.91', 1)
    # print ZabbixAPi().changeGroupTemplate('10.1.20.91', groups=[59], templates=[10374])
    # print ZabbixAPi().addHost('10.1.20.91', '10.1.20.91', groups=[59], templates=[10374])
    # print ZabbixAPi().getHostGroupsByName('free', 'http 80 templates', u'业务分类-基础业务')
    # print ZabbixAPi().getHostsByName('10.1.20.922')
    # print ZabbixAPi().getProxy('zabbix_proxy_ali22')
    # print get_segment_by_ip_mask('10.1.22.24', '255.255.255.0')
    # print get_maskint_by_segment('10.1.22.24/24')
    # print exchange_maskint(24)
    # print AddMonitorTask().excute(ip='10.1.20.91')
    # print DelMonitorTask().excute(ip=['10.1.20.91'])
    # state, data = GitLabApi().getProjects(0, 1000)
    # print data[0]
    # print len(data)

    # print AliyunSLBApi().getSLBByAddr('10.1.28.166')
    #
    # pc = Prpcrypt(configs.AES_KEY) #初始化密钥
    # e = pc.encrypt("dfdfdfdew34%^234") #加密
    # d = pc.decrypt(e) #解密
    # print "encrypt:", e
    # print "decrypt:", d

    l = []
    if not l:
        print 111
    pass

    print "".join(["1"])

    print int(time.time())
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
