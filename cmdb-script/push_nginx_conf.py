#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json, logging, sys, os, commands, fcntl
from collections import defaultdict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

LOG_DIR = '/var/log/cmdb'
RUN_DIR = '/var/run/cmdb'
WORK_DIR = '/data/nginx_conf'

run_env = sys.argv[1]

class CMDBApi():

    api = ''
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    domain = 'http://cmdb.mwbyd.cn'

    def __init__(self, api):
        self.api = api
        if run_env == 'pord':
            self.domain = 'http://cmdb.mwbyd.cn'
        elif run_env == 'dev':
            self.domain = 'http://127.0.0.1'
        else:
            self.domain = 'http://test.cmdb.mwbyd.cn'

    def get(self, **kwargs):
        try:
            response = requests.get(self.domain + self.api + '?format=json', params=kwargs, headers=self.headers)
            if response.status_code == 400:
                return False, response.text
            if response.status_code != 200:
                return False, 'fail!'
            return True, response.text
        except Exception, ex:
            return False, str(ex)

if __name__ == "__main__":

    try:
        service_name = sys.argv[2]
        env = sys.argv[3]
    except Exception, ex:
        logging.error(u"参数错误:" + str(ex))
        print u"参数错误:" + str(ex)
        exit(400)
    logging.basicConfig(filename=LOG_DIR + '/nginx_conf.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

    conf_list = []
    service_conf = defaultdict(list)
    state, data = CMDBApi('/api/lb/nginxconf/' + service_name + '/').get(env=env)
    if not state:
        logging.error(u"获取Nginx配置错误:" + data)
        print u"获取Nginx配置错误:" + data
        exit(100)
    nginx_conf = data
    state, nginxres = CMDBApi('/api/host/host/').get(service_name=service_name, env=env)
    if not state:
        logging.error(u"获取Nginx集群机器错误:" + nginxres)
        print u"获取Nginx集群机器错误:" + nginxres
        exit(101)
    try:
        nginxres = json.loads(nginxres)
        nginxlist = nginxres['results']
    except Exception, ex:
        logging.error(u"获取Nginx集群机器错误:" + str(ex))
        print u"获取Nginx集群机器错误:" + str(ex)
        exit(102)
    if len(nginxlist) <= 0:
        logging.error(service_name + u" Nginx集群主机为空")
        print service_name + u" Nginx集群主机为空"
        exit(103)
    lock_file = RUN_DIR + "/" + service_name + ".lock"
    f_lock = open(lock_file, 'w')
    fcntl.flock(f_lock, fcntl.LOCK_EX) # 互斥锁
    host_file = WORK_DIR + '/' + service_name + ".host"
    nginx_ips = []
    for n in nginxlist:
        nginx_ips.append(n['ip'])
    f = open(host_file, 'w')
    f.write("\n".join(nginx_ips))
    f.close()
    nginx_file = WORK_DIR + '/cmdb_' + service_name + ".conf"
    f = open(nginx_file, 'w')
    f.write(nginx_conf)
    f.close()
    cmd = '/usr/bin/ansible-playbook /etc/ansible/playbooks/nginx_template.yml -i %s --extra-vars "nginx_file=%s"' % (host_file, nginx_file)
    status, output = commands.getstatusoutput(cmd)
    logging.info("code:" + str(status))
    if status != 0:
        print u"推送配置文件失败:" + output
        logging.error(u"推送配置文件失败:" + output)
        exit(500)
    fcntl.flock(f_lock, fcntl.LOCK_UN) # 释放锁
    logging.info("push success!")
    exit(0)


