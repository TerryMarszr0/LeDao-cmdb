#coding:utf-8
import types
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.inventory import Inventory
from ansible.runner import Runner
import json, time
import requests



def getHostInfo():
    HostIPList = []
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
            HostIPList.append(host['ip'])
            count += 1
        HostIPList.sort()
    return HostIPList


class MyInventory(Inventory):
    def __init__(self, resource):

        self.resource = resource
        self.inventory = Inventory(host_list=[])
        self.gen_inventory()

    def my_add_group(self, hosts, groupname, groupvars=None):
        """
        add hosts to a group
        """
        my_group = Group(name=groupname)

        # if group variables exists, add them to group
        if groupvars:
            for key, value in groupvars.iteritems():
                my_group.set_variable(key, value)

        # add hosts to group
        for host in hosts:
            # set connection variables
            hostname = host.get("hostname")
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key")
            my_host = Host(name=hostname, port=hostport)
            my_host.set_variable('ansible_ssh_host', hostip)
            my_host.set_variable('ansible_ssh_port', hostport)
            my_host.set_variable('ansible_ssh_user', username)
            my_host.set_variable('ansible_ssh_pass', password)
            my_host.set_variable('ansible_ssh_private_key_file', ssh_key)

            # set other variables
            for key, value in host.iteritems():
                if key not in ["hostname", "port", "username", "password"]:
                    my_host.set_variable(key, value)
            # add to group
            my_group.add_host(my_host)

        self.inventory.add_group(my_group)

    def gen_inventory(self):
        """
        add hosts to inventory.
        """
        if isinstance(self.resource, list):
            self.my_add_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.iteritems():
                self.my_add_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


class MyRunner(MyInventory):
    def __init__(self, *args, **kwargs):
        super(MyRunner, self).__init__(*args, **kwargs)
        self.results_raw = {}
    def run(self, module_name='shell', module_args='', timeout=10, forks=2, pattern='*',
            become=False, become_method='sudo', become_user='root', become_pass='', transport='paramiko'):
        hoc = Runner(module_name=module_name,
                     module_args=module_args,
                     timeout=timeout,
                     inventory=self.inventory,
                     pattern=pattern,
                     forks=forks,
                     become=become,
                     become_method=become_method,
                     become_user=become_user,
                     become_pass=become_pass,
                     transport=transport
                     )
        self.results_raw = hoc.run()
        return self.results_raw

    @property
    def results(self):
        result = {'failed': {}, 'ok': {}}
        dark = self.results_raw.get('dark')
        contacted = self.results_raw.get('contacted')
        if dark:
            for host, info in dark.items():
                result['failed'][host] = info.get('msg')

        if contacted:
            for host, info in contacted.items():
                if info.get('invocation').get('module_name') in ['raw', 'shell', 'command', 'script']:
                    if info.get('rc') == 0:
                        result['ok'][host] = info.get('stdout') + info.get('stderr')
                    else:
                        result['failed'][host] = info.get('stdout') + info.get('stderr')
                else:
                    if info.get('failed'):
                        result['failed'][host] = info.get('msg')
                    else:
                        result['ok'][host] = info.get('changed')
        return result


def getHostInfoByIp(ip_list):
    resource = []
    for ip in ip_list:
        resource.append({
            "hostname": ip,
            "port": "22",
            "username": "root",
            "password": "xxx",
        })
    runner = MyRunner(resource)
    result = runner.run(module_name='setup', module_args='')
    if not result.has_key("contacted"):
        return False
    contacted = result.get('contacted')
    hostinfo_list = []
    for k, v in contacted.items():
        ansible_facts = v.get('ansible_facts')
        ansible_devices = ansible_facts.get('ansible_devices')    # 获取相应的磁盘信息
        disk = {}
        for d, v in ansible_devices.items():
            disk[d] = v['size']
        ansible_processor = ansible_facts.get('ansible_processor')    # 获取处理器信息

        system_type = ansible_facts.get("ansible_distribution")    # 主机类型
        if system_type.lower() == "freebsd":
            system_version = ansible_facts.get("ansible_distribution_release")
            cpu_cores = ansible_facts.get("ansible_processor_count")
        else:
            system_version = ansible_facts.get("ansible_distribution_version")
            cpu_cores = ansible_facts.get("ansible_processor_vcpus")

        cpu = cpu_cores
        if len(ansible_processor) > 0:
            cpu = ansible_processor[0] + ' * ' + unicode(cpu_cores)

        # 遍历 ansible_facts 字典
        network_card = {}
        for key,value in ansible_facts.items():         # 根据特殊字段，获取该主机的 ip 信息
            if (type(value) is types.DictType) and value.has_key('promisc'):
                network_card[key] = value

        hostinfo_list.append({
            'ip': k,
            'kernel': ansible_facts.get('ansible_kernel'),
            'hostname': ansible_facts['ansible_hostname'],
            'memory': ansible_facts.get('ansible_memtotal_mb'),
            'cpu': cpu,
            'sn': ansible_facts.get('ansible_product_serial'),
            'disk': json.dumps(disk),
            'os_name': system_type + ' ' + system_version + ' ' + ansible_facts.get('ansible_architecture'),
            'mac': ansible_facts.get("ansible_default_ipv4").get("macaddress"),
            'network': ansible_facts.get("ansible_default_ipv4").get("network"),
            'gateway': ansible_facts.get("ansible_default_ipv4").get("gateway"),
            'netmask': ansible_facts.get("ansible_default_ipv4").get("netmask"),
            'fqdn': ansible_facts.get("ansible_fqdn"),
            'network_card':json.dumps(network_card)
        })
    return hostinfo_list


class CMDBApi():

    token = ''
    cmdb_url = 'http://test.cmdb.mwbyd.cn'
    api = '/api/host/info/'
    headers = {"Content-Type": "application/json"}

    def __init__(self):
        state, token = self.getToken()
        if state:
            self.headers['Authorization'] = 'Token ' + token

    def getToken(self):
        try:
            response = requests.post(self.cmdb_url + '/api/tokenauth/' + '?format=json',
                                     data=json.dumps({'username': 'cmdb', 'password': 'mwbyd,123'}),
                                     headers={"Content-Type": "application/json"})
            if response.status_code != 200:
                return False, 'fail!'
            data = json.loads(response.text)
            return True, data['token']
        except Exception, ex:
            return False, str(ex)

    def post(self,par):
        try:
            response = requests.post(self.cmdb_url + self.api + '?format=json',data=json.dumps(par),headers=self.headers)
            if response.status_code < 200 or response.status_code >= 300:
                return False, 'fail!'
            data = json.loads(response.text)
            return True, data
        except Exception, ex:
            return False, str(ex)

    def delete(self):
        try:
            response = requests.delete(self.cmdb_url + self.api, headers=self.headers)
            if response.status_code != 200:
                return False, 'fail!'
            data = json.loads(response.text)
            return True, 'succ!'
        except Exception, ex:
            return False, str(ex)



if __name__ == "__main__":
    cmdb_api = CMDBApi()
    cmdb_api.delete()    # 在向ip详情表中增添数据之前先删除旧数据（每天12点更新一次）
    ip_list = getHostInfo()  # 获取 host_hosts 表中的所有的 ip
    hostinfo_list = getHostInfoByIp(ip_list)  # 根据获取的 ip_list 通过 ansible 查找相应的主机信息并保存在 hostinfo_list 中
    for hostinfo in hostinfo_list:  # 向数据库中插入相应 ip 对应的信息
        cmdb_api.post(hostinfo)

