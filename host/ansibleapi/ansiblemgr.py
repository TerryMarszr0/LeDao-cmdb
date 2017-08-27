# # -*- coding: utf-8 -*-
#
# from host.ansibleapi.ansiblebase import MyRunner, Command
# from host.models import Hosts, HostPassword
# from cmdb import settings
# import json, time
#
# def getHostInfoByIp(host_list):
#     resource = []
#     for h in host_list:
#         resource.append({
#             "hostname": h.ip,
#             "port": "22",
#             "username": "root",
#             "password": "xx"
#         })
#
#     runner = MyRunner(resource)
#     result = runner.run(module_name='setup', module_args='')
#     if not result.has_key("contacted"):
#         return False
#     contacted = result.get('contacted')
#     hostinfo_list = []
#     for k,v in contacted.items():
#         ansible_facts = v.get('ansible_facts')
#         ansible_devices = ansible_facts.get('ansible_devices')
#         disk = {}
#         for d, v in ansible_devices.items():
#             disk[d] = v['size']
#         ansible_processor = ansible_facts.get('ansible_processor')
#
#         system_type = ansible_facts.get("ansible_distribution")
#         if system_type.lower() == "freebsd":
#             system_version = ansible_facts.get("ansible_distribution_release")
#             cpu_cores = ansible_facts.get("ansible_processor_count")
#         else:
#             system_version = ansible_facts.get("ansible_distribution_version")
#             cpu_cores = ansible_facts.get("ansible_processor_vcpus")
#
#         cpu = cpu_cores
#         if len(ansible_processor) > 0:
#             cpu = ansible_processor[0] + ' * ' + unicode(cpu_cores)
#         hostinfo_list.append({
#             'ip': k,
#             'kernel': ansible_facts.get('ansible_kernel'),
#             'hostname': ansible_facts['ansible_hostname'],
#             'memory': ansible_facts.get('ansible_memtotal_mb'),
#             'cpu': cpu,
#             'sn': ansible_facts.get('ansible_product_serial'),
#             'disk': json.dumps(disk),
#             'os_name': system_type + ' ' + system_version + ' ' + ansible_facts.get('ansible_architecture'),
#             'mac': ansible_facts.get("ansible_default_ipv4").get("macaddress"),
#         })
#     return hostinfo_list
#
#
#
#
# def updateHostname():
#     for h in getHostInfoByIp(Hosts.objects.all()):
#         Hosts.objects.filter(ip=h['ip']).update(hostname=h['hostname'])
#
# def syncHostInfo():
#     for h in getHostInfoByIp(Hosts.objects.all()):
#         Hosts.objects.filter(ip=h['ip']).update(kernel=h['kernel'], memory=h['memory'], cpu=h['cpu'], sn=h['sn'], disk=h['disk'], os_name=h['os_name'], mac=h['mac'])