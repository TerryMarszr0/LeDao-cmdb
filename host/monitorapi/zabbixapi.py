# -*- coding:utf-8 -*-
import json, requests

from cmdb import configs

class ZabbixBase:
    def __init__(self, url=configs.ZABBIX_API_URL):
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
            'user': configs.ZABBIX_USER,
            'password': configs.ZABBIX_PASSWORD
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

    def getHostGroupsByName(self, *args):
        method = 'hostgroup.get'
        params = {
            "output": "extend",
            "filter": {
                "name": args
            }
        }
        return self.execute(method, params)

    def createHostGroup(self, name):
        method = 'hostgroup.create'
        params = {
            "name": name
        }
        return self.execute(method, params)


    def delGroup(self, groups=[]):
        method = 'hostgroup.delete'
        state, res = self.getHostGroupsByName(*groups)
        if not state:
            return state, res
        result = res.get('result', [])
        groupids = []
        for r in result:
            groupids.append(r.get('groupid'))
        params = groupids
        return self.execute(method, params)

    def getAllTemplates(self):
        method = 'template.get'
        params = {
            "output": "extend",
            "filter": {
            }
        }
        return self.execute(method, params)

    def getTemplatesByName(self, *args):
        method = 'template.get'
        params = {
            "output": "extend",
            "filter": {
                "host": args
            }
        }
        return self.execute(method, params)

    def getHostsByName(self, *args):
        method = 'host.get'
        params = {
            "output": "extend",
            "filter": {
                "host": args
            }
        }
        print params
        return self.execute(method, params)

    def getGroupByHost(self, *args):
        method = 'host.get'
        params = {
            "output": ["hostid"],
            "selectGroups": "extend",
            "filter": {
                "host": args
            }
        }
        return self.execute(method, params)

    def addHost(self, host, ip, proxy_hostid, groups=[], templates=[], status=0, port=10050):
        method = 'host.create'
        group_list = []
        for g in groups:
            group_list.append({'groupid': g})
        template_list = []
        for t in templates:
            template_list.append({'templateid': t})
        params = {
            "host": host,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": port
                }
            ],
            "groups": group_list,
            "status": status,
            "templates": template_list
        }
        if proxy_hostid:
            params['proxy_hostid'] = proxy_hostid
        return self.execute(method, params)

    def changeStatus(self, host, status):
        method = 'host.update'
        state, res = self.getHostsByName(host)
        if not state:
            return state, res
        result = res.get('result', [])
        if len(result) != 1:
            return False, 'get host error'
        result = result[0]
        params = {
            "hostid": result.get('hostid', 0),
            "status": status,
        }
        return self.execute(method, params)

    def changeHost(self, host, status, groups=[], templates=[]):
        method = 'host.update'
        state, res = self.getHostsByName(host)
        if not state:
            return False, res
        result = res.get('result', [])
        if len(result) != 1:
            return False, 'get host error'
        result = result[0]
        params = {
            "hostid": result.get('hostid', 0),
            "groups": groups,
            "templates": templates,
            "status": status,
        }
        return self.execute(method, params)

    def deleteHost(self, host):
        method = 'host.delete'
        state, res = self.getHostsByName(host)
        if not state:
            return state, res
        result = res.get('result', [])
        hostids = []
        for r in result:
            hostids.append(r.get('hostid'))
        params = hostids
        return self.execute(method, params)

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

    def getProxy(self, name):
        method = 'proxy.get'
        params = {
            "output": "extend",
            "filter": {
                "host": name
            }
        }
        return self.execute(method, params)

###################################################################################
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
###################################################################################

ALIYUN_TEMPLATE = {
    'default': 10374,
    'default146': 10001,
    'mysql': 10105,
    'mongodb': 12259,
    'PostgreSQL': 12301,
    'redis': 10135,
    'ActiveMQ': 11496,
    'nginx': 10161,
    'apache': 10161,
    'tomcat': 10160,
}

IDC_TEMPLATE = {
    'default': 10374,
    'default146': 10001,
    'mysql': 10105,
    'mongodb': 12259,
    'PostgreSQL': 12383,
    'redis': 10135,
    'ActiveMQ': 11496,
    'nginx': 10161,
    'apache': 10161,
    'tomcat': 10160,
}