# -*- coding: utf-8 -*-
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.inventory import Inventory
from ansible.runner import Runner
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
import os

class MyInventory(Inventory):
    """
    this is my ansible inventory object.
    """
    def __init__(self, resource):
        """
        resource的数据格式是一个列表字典，比如
            {
                "group1": {
                    "hosts": [{"hostname": "10.10.10.10", "port": "22", "username": "test", "password": "mypass"}, ...],
                    "vars": {"var1": value1, "var2": value2, ...}
                }
            }

        如果你只传入1个列表，这默认该列表内的所有主机属于my_group组,比如
            [{"hostname": "10.10.10.10", "port": "22", "username": "test", "password": "mypass"}, ...]
        """
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
    """
    This is a General object for parallel execute modules.
    """
    def __init__(self, *args, **kwargs):
        super(MyRunner, self).__init__(*args, **kwargs)
        self.results_raw = {}

    def run(self, module_name='shell', module_args='', timeout=10, forks=10, pattern='*',
            become=False, become_method='sudo', become_user='root', become_pass='', transport='paramiko'):
        """
        run module from andible ad-hoc.
        module_name: ansible module_name
        module_args: ansible module args
        """
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
        """
        {'failed': {'localhost': ''}, 'ok': {'jumpserver': ''}}
        """
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


class Command(MyInventory):
    """
    this is a command object for parallel execute command.
    """
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.results_raw = {}

    def run(self, command, module_name="command", timeout=10, forks=10, pattern=''):
        """
        run command from andible ad-hoc.
        command  : 必须是一个需要执行的命令字符串， 比如
                 'uname -a'
        """
        data = {}

        if module_name not in ["raw", "command", "shell"]:
            raise CommandValueError("module_name",
                                    "module_name must be of the 'raw, command, shell'")
        hoc = Runner(module_name=module_name,
                     module_args=command,
                     timeout=timeout,
                     inventory=self.inventory,
                     pattern=pattern,
                     forks=forks,
                     )
        self.results_raw = hoc.run()

    @property
    def result(self):
        result = {}
        for k, v in self.results_raw.items():
            if k == 'dark':
                for host, info in v.items():
                    result[host] = {'dark': info.get('msg')}
            elif k == 'contacted':
                for host, info in v.items():
                    result[host] = {}
                    if info.get('stdout'):
                        result[host]['stdout'] = info.get('stdout')
                    elif info.get('stderr'):
                        result[host]['stderr'] = info.get('stderr')
        return result

    @property
    def state(self):
        result = {}
        if self.stdout:
            result['ok'] = self.stdout
        if self.stderr:
            result['err'] = self.stderr
        if self.dark:
            result['dark'] = self.dark
        return result

    @property
    def exec_time(self):
        """
        get the command execute time.
        """
        result = {}
        all = self.results_raw.get("contacted")
        for key, value in all.iteritems():
            result[key] = {
                    "start": value.get("start"),
                    "end"  : value.get("end"),
                    "delta": value.get("delta"),}
        return result

    @property
    def stdout(self):
        """
        get the comamnd standard output.
        """
        result = {}
        all = self.results_raw.get("contacted")
        for key, value in all.iteritems():
            result[key] = value.get("stdout")
        return result

    @property
    def stderr(self):
        """
        get the command standard error.
        """
        result = {}
        all = self.results_raw.get("contacted")
        for key, value in all.iteritems():
            if value.get("stderr") or value.get("warnings"):
                result[key] = {
                    "stderr": value.get("stderr"),
                    "warnings": value.get("warnings"),}
        return result

    @property
    def dark(self):
        """
        get the dark results.
        """
        return self.results_raw.get("dark")

if __name__ == "__main__":

#   resource =  {
#                "group1": {
#                    "hosts": [{"hostname": "127.0.0.1", "port": "22", "username": "root", "password": "xxx"},],
#                    "vars" : {"var1": "value1", "var2": "value2"},
#                          },
#                }


    resource = [{"hostname": "127.0.0.1", "port": "22", "username": "root", "password": "xx",
                 # "ansible_become": "yes",
                 # "ansible_become_method": "sudo",
                 # # "ansible_become_user": "root",
                 # "ansible_become_pass": "yusky0902",
                 }]
    # cmd = Command(resource)
    # cmd.run('ls', pattern='*')
    # print cmd.results_raw
    # print cmd.result
    print os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
    runner = MyRunner(resource)
    runner.run(module_name='setup', module_args='')
    print (runner.results_raw)