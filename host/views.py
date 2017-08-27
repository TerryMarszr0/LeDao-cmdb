# -*- coding: utf-8 -*-
import json
from django.forms.models import model_to_dict
from app.models import App, AppService, ServiceHost
from asset.models import Room, AssetModel, Conf
from fortress.models import AuthRecord
from host.models import Hosts, Image, HostInfo
from public.base import PublicView


# import pwd
# Create your views here.

class AddHostPageView(PublicView):
    template_name = 'host/add.html'

    def get_context_data(self, **kwargs):
        context = super(AddHostPageView, self).get_context_data(**kwargs)
        context['type'] = Hosts.HOST_TYPE_CHOICES
        context['attribute'] = Hosts.HOST_ATTRIBUTE_CHOCIES
        context['env'] = Hosts.HOST_ENV_CHOICES
        rooms = []
        for room in Room.objects.filter(state='online'):
            t = {}
            t['id'] = room.id
            t['cn_name'] = room.cn_name
            rooms.append(t)
        context['rooms'] = rooms
        models = []
        for m in AssetModel.objects.all():
            t = {}
            t['id'] = m.id
            t['name'] = m.name
            models.append(t)
        context['models'] = models
        confs = []
        for c in Conf.objects.all():
            t = {}
            t['id'] = c.id
            t['name'] = c.name
            confs.append(t)
        context['confs'] = confs
        os_arr = []
        for o in Image.objects.all():
            t = {}
            t['id'] = o.id
            t['name'] = o.name
            os_arr.append(t)
        context['img_list'] = os_arr
        context['header_title'] = u'新增资产'
        context['path1'] = u'资产管理'
        context['path2'] = u'新增资产'
        return context

class AddAliyunPageView(PublicView):
    template_name = 'host/add_aliyun.html'

    def get_context_data(self, **kwargs):
        context = super(AddAliyunPageView, self).get_context_data(**kwargs)
        context['instance_type'] = Hosts.HOST_ALIYUN_TYPE_CHOCIES
        context['env'] = Hosts.HOST_ENV_CHOICES
        rooms = []
        for room in Room.objects.filter(state='online'):
            t = {}
            t['id'] = room.id
            t['cn_name'] = room.cn_name
            rooms.append(t)
        context['rooms'] = rooms
        models = []
        for m in AssetModel.objects.all():
            t = {}
            t['id'] = m.id
            t['name'] = m.name
            models.append(t)
        context['models'] = models
        confs = []
        for c in Conf.objects.all():
            t = {}
            t['id'] = c.id
            t['name'] = c.name
            confs.append(t)
        context['confs'] = confs
        os_arr = []
        for o in Image.objects.all():
            t = {}
            t['id'] = o.id
            t['name'] = o.name
            os_arr.append(t)
        context['env_list'] = Hosts.HOST_ENV_CHOICES
        context['img_list'] = os_arr
        context['header_title'] = u'新增资产'
        context['path1'] = u'资产管理'
        context['path2'] = u'新增资产'
        return context

class UpdateHostPageView(PublicView):
    template_name = 'host/update.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateHostPageView, self).get_context_data(**kwargs)
        context['host_id'] = self.request.GET.get('host_id', 0)
        context['type'] = Hosts.HOST_TYPE_CHOICES
        context['attribute'] = Hosts.HOST_ATTRIBUTE_CHOCIES
        context['env'] = Hosts.HOST_ENV_CHOICES
        rooms = []
        for room in Room.objects.filter(state='online'):
            t = {}
            t['id'] = room.id
            t['cn_name'] = room.cn_name
            rooms.append(t)
        context['rooms'] = rooms
        models = []
        for m in AssetModel.objects.all():
            t = {}
            t['id'] = m.id
            t['name'] = m.name
            models.append(t)
        context['models'] = models
        confs = []
        for c in Conf.objects.all():
            t = {}
            t['id'] = c.id
            t['name'] = c.name
            confs.append(t)
        context['confs'] = confs
        os_arr = []
        for o in Image.objects.all():
            t = {}
            t['id'] = o.id
            t['name'] = o.name
            os_arr.append(t)
        context['img_list'] = os_arr
        context['header_title'] = u'修改资产信息'
        context['path1'] = u'资产管理'
        context['path2'] = u'新增资产'
        return context

class DetailHostPageView(PublicView):
    template_name = 'host/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailHostPageView, self).get_context_data(**kwargs)
        host_id = self.request.GET.get('host_id', 0)
        host = Hosts.objects.get(id=host_id)
        context['host_id'] = host_id
        context['ip'] = host.ip
        context['name'] = host.hostname
        context['type'] = host.type
        if host.type == 'vm':
            host2 = Hosts.objects.filter(id=host.pid)
            context['host_ip'] = host2[0].ip if len(host2) else None
        else:
            host_children = Hosts.objects.filter(pid=host.id)
            ips = []
            if len(host_children) > 0:
                for host_child in host_children:
                    ips.append(host_child.ip)
            context['virtual_machines'] = ', '.join(ips)
        context['attribute'] = host.attribute
        attribute_list = ['kvmparent','xenparent','vmwareparent','dockerparent']
        context['have_virtual_list'] = True if host.attribute in attribute_list else False

        context['aliyun_id'] = host.aliyun_id

        room_name = Room.objects.get(id=host.room_id).name
        context['room_name'] = room_name  # 如果是 idc 机房则还要显示：1.机柜 2.U位 3.型号 4.sn号
        if room_name == 'idc':
            context['rack_id'] = host.rack_id
            context['u'] = host.position
            context['model_id'] = host.model_id
            context['sn'] = host.sn

        context['state'] = host.state

        #获取服务列表
        serviceHosts = ServiceHost.objects.filter(host_id=host.id)
        service_id_list = []
        for serviceHost in serviceHosts:
            service_id_list.append(serviceHost.service_id)
        services = []
        app_ids = []
        for service_id in service_id_list:
            appService = AppService.objects.get(id=service_id)
            services.append(appService.name)    #获取服务列表
            app_ids.append(appService.app_id)  #获取app_id_list

        apps = []
        for app_id in app_ids:
            apps.append(App.objects.get(id=app_id).name)
        apps = list(set(apps))   # 去重

        context['services'] = ', '.join(services)
        context['apps'] = ', '.join(apps)

        # 获取从 ansible 中抓取来的主机信息，在 hostInfo 表中查
        host_info = HostInfo.objects.filter(ip=host.ip)
        if len(host_info):
            info = host_info[0]
            context['getInfoState'] = True
            context['network'] = info.network
            context['gateway'] = info.gateway
            context['netmask'] = info.netmask
            context['fqdn'] = info.fqdn
            context['mac'] = info.mac
            context['os_name'] = info.os_name
            context['kernel'] = info.kernel
            context['cpu'] = info.cpu
            context['memory'] = info.memory

            network_card_list = []
            network_card = json.loads(info.network_card)
            for key,value in network_card.items():
                key = key.split('_')[1]
                network_card_list.append(key)
                if value.has_key('macaddress'):
                    context['macaddress'] = value['macaddress']
            context['network_card_list'] = network_card_list


        else:
            context['getInfoState'] = False


        context['header_title'] = u'主机详细信息'
        context['path1'] = u'资产管理'
        context['path2'] = u'主机详细信息'

        return context

class HostImagePageView(PublicView):
    template_name = 'host/image.html'

    def get_context_data(self, **kwargs):
        context = super(HostImagePageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看系统镜像'
        context['path1'] = u'资产管理'
        context['path2'] = u'查看镜像'
        context['os_types'] = Image.OS_TYPE_CHOCIES
        context['platforms'] = Image.PLATFORM_CHOCIES
        return context

class HostPageView(PublicView):
    template_name = 'host/host.html'

    def get_context_data(self, **kwargs):
        context = super(HostPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看资产'
        context['path1'] = u'资产管理'
        context['path2'] = u'查看资产'
        context['rooms'] = Room.objects.all()
        context['types'] = AppService.TYPE
        context['state'] = Hosts.HOST_STATE_CHOCIES
        context['img_list'] = Image.objects.all()
        context['confs'] = Conf.objects.all()
        context['env'] = Hosts.HOST_ENV_CHOICES
        context['host_types'] = Hosts.HOST_TYPE_CHOICES
        context['attributes'] = Hosts.HOST_ATTRIBUTE_CHOCIES
        context['upstreamstate'] = ServiceHost.STATE
        return context

class AppHostPageView(PublicView):
    template_name = 'host/app_host.html'

    def get_context_data(self, **kwargs):
        context = super(AppHostPageView, self).get_context_data(**kwargs)
        service_id = self.request.GET.get('service_id', '')
        search = self.request.GET.get('search', '')
        if service_id:
            service = AppService.objects.filter(id=service_id)
            if len(service) > 0:
                service = model_to_dict(service[0])
                app = App.objects.filter(id=service['app_id'])
                if len(app) > 0:
                    service['app_name'] = app[0].name
                context['service'] = service
            context['header_title'] = u'查看服务主机'
            context['path2'] = u'查看服务主机'
        else:
            context['header_title'] = u'查看资产'
            context['path2'] = u'查看资产'
        context['path1'] = u'应用管理'
        context['rooms'] = Room.objects.all()
        context['host_types'] = Hosts.HOST_TYPE_CHOICES
        context['attribute'] = Hosts.HOST_ATTRIBUTE_CHOCIES
        context['state'] = Hosts.HOST_STATE_CHOCIES
        context['confs'] = Conf.objects.all()
        context['env'] = Hosts.HOST_ENV_CHOICES
        context['img_list'] = Image.objects.all()
        context['count_list'] = range(1, 21)
        context['service_types'] = AppService.TYPE
        context['apps'] = App.objects.all()
        context['roles'] = AuthRecord.ROLE_CHOICES
        context['search'] = search
        context['upstreamstate'] = ServiceHost.STATE
        return context