# -*- coding: utf-8 -*-
import time, json, uuid
from rest_framework import filters
from host.models import Hosts, Image, ImageTag, HostDeleted, HostPassword
from host.serializers import HostsSerializer, ImageSerializer, HostPasswordSerializer, HostInfoSerializer, HostInfo
from rest_framework.response import Response
from public.base_exception import APIValidateException
from django.db import transaction
from app.models import AppService, App, ServiceHost
from cmdb import configs
from django.forms.models import model_to_dict
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView
from collections import defaultdict
from rest_framework import status
from host.lib.host_tools import HostValidate, changeHostNameById, sshGetHostName
from host.aliyunapi.ecsapi import AliyunECSApi, importECS
from fortress.models import AuthRecord
from host.task.hosttask import HostMonitorTask, DelMonitorTask
from cmdb.configs import logger
from asset.models import IpAddress
from public.common.tools import Prpcrypt
from rest_framework import permissions
from host.lib.host_tools import autoHostName
from app.models import ServiceHost
from lb.models import LB, ServiceLB


class ServiceHostsList(CmdbListCreateAPIView):
    """
    服务主机列表.

    查询参数：
    ● service_name              ——   服务名称(必输)
    ● env                       ——   环境(prod-生产环境, stg-预发环境, uat-集成测试环境, test-测试环境, dev-开发环境)
    ● type                      ——   主机类型
    ● attribute                 ——   属性
    ● room_id                   ——   机房id
    ● conf_id                   ——   配置id
    ● model_id                  ——   型号id
    ● state                     ——   状态(free、online、offline、unuse)

    输入/输出参数：
    ● id                        ——   PK
    ● instance_id               ——   实例id
    ● sn                        ——   序列号
    ● type                      ——   主机类型(server, vm, net, aliyun, storage)
    ● attribute                 ——   属性(server, xen, switch, xenparent, dockerparent, docker, route, firewall, storage)
    ● service_id                ——   服务id
    ● service_id[]              ——   服务id列表
    ● service_name              ——   服务名称
    ● room_id                   ——   机房id
    ● location                  ——   u位
    ● rack_id                   ——   机柜id
    ● conf_id                   ——   配置id
    ● model_id                  ——   型号id
    ● pid                       ——   宿主机id(即宿主机的主机id)
    ● state                     ——   状态(free、online、offline、unuse)
    ● hostname                  ——   主机名
    ● ip                        ——   ip
    ● oobip                     ——   管理ip
    ● ctime                     ——   创建时间
    ● expiration_time           ——   过保时间(到期时间)
    ● aliyun_id                 ——   阿里云实例id

    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_fields = ('room_id', 'type', 'attribute', 'conf_id', 'model_id', 'state', 'env')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    def get_queryset(self):
        queryset = Hosts.objects.exclude(state='deleted')
        service_name = self.request.query_params.get('service_name', None)
        env = self.request.query_params.get('env', None)
        if not service_name:
            raise APIValidateException(u'service_name不能为空')
        service = AppService.objects.filter(name=service_name)
        if len(service) <= 0:
            raise APIValidateException(u'服务不存在')
        if len(service) > 1:
            raise APIValidateException(u'服务名称重复')
        service_id = service[0].id
        hostids = []
        for s in ServiceHost.objects.filter(service_id=service_id):
            hostids.append(s.host_id)
        if env:
            queryset = queryset.filter(env=env)
        queryset = queryset.filter(id__in=hostids)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        results = HostValidate().formatHostList(serializer.data)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

class HostsList(CmdbListCreateAPIView):
    """
    主机列表/创建主机.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● sn                        ——   序列号(查询多个用逗号隔开)
    ● app_id                    ——   应用id
    ● app_name                  ——   应用名称
    ● img_id                    ——   镜像id
    ● service_id                ——   服务id
    ● service_name              ——   服务名称
    ● env                       ——   环境(prod-生产环境, stg-预发环境, uat-集成测试环境, test-测试环境, dev-开发环境)
    ● type                      ——   主机类型
    ● attribute                 ——   属性
    ● room_id                   ——   机房id
    ● conf_id                   ——   配置id
    ● model_id                  ——   型号id
    ● service_type              ——   服务类型(tomcat,nginx,apache,redis,memcache等)
    ● pid                       ——   宿主机id(即宿主机的主机id)
    ● ip                        ——   ip
    ● state                     ——   状态(free、online、offline、release、broken、delete、install)
    ● search                    ——   搜索内容(hostname、ip)

    输入/输出参数：
    ● id                        ——   PK
    ● instance_id               ——   实例id
    ● sn                        ——   序列号
    ● type                      ——   主机类型(server, vm, net, aliyun, storage)(必输)
    ● attribute                 ——   属性(ECS, RDS, SLB, server, xen, kvm, vmware, switch, xenparent, dockerparent, docker, route, firewall, storage)(必输)
    ● service_id                ——   服务id
    ● service_name              ——   服务名称
    ● env                       ——   环境(prod-生产环境, stg-预发环境, uat-集成测试环境, test-测试环境, dev-开发环境)(必输)
    ● room_id                   ——   机房id(必输)
    ● location                  ——   u位
    ● rack_id                   ——   机柜id
    ● conf_id                   ——   配置id
    ● model_id                  ——   型号id
    ● pid                       ——   宿主机id(即宿主机的主机id)
    ● state                     ——   状态(free、online、offline、release、broken、delete、install)(必输)
    ● hostname                  ——   主机名(必输)
    ● ip                        ——   ip
    ● oobip                     ——   管理ip
    ● ctime                     ——   创建时间
    ● expiration_time           ——   过保时间(到期时间)
    ● aliyun_id                 ——   阿里云实例id

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_fields = ('room_id', 'type', 'attribute', 'conf_id', 'model_id', 'pid', 'state', 'env', 'img_id', 'ip')
    search_fields = ('hostname', 'ip', 'oobip')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def _allowed_methods(self):
        return ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS']

    def get_queryset(self):
        queryset = Hosts.objects.exclude(state='deleted')
        id = self.request.query_params.get('id', None)
        sn = self.request.query_params.get('sn', None)
        service_type = self.request.query_params.get('service_type', None)
        app_id = self.request.query_params.get('app_id', None)
        service_name = self.request.query_params.get('service_name', None)
        app_name = self.request.query_params.get('app_name', None)
        group = self.request.query_params.get('group', None)
        service_id = self.request.query_params.get('service_id', None)
        sort = self.request.query_params.get('sort', 'id')
        order = self.request.query_params.get('order', 'desc')
        if order.lower() == 'desc':
            sort = "-" + sort
        queryset = queryset.order_by(sort)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        if sn:
            sn_arr = sn.split(",")
            queryset = queryset.filter(sn__in=sn_arr)

        service_id_list = None
        service_type_ids = []
        if service_type:
            for g in AppService.objects.filter(type=service_type):
                service_type_ids.append(g.id)
            service_id_list = service_type_ids

        group_service_ids = []
        if group:
            for g in App.objects.filter(group=group):
                group_service_ids.append(g.id)
            if service_id_list == None:
                service_id_list = group_service_ids
            else:
                service_id_list = list(set(service_id_list).intersection(set(group_service_ids)))
        app_service_ids = []
        if app_id:
            for service in AppService.objects.filter(app_id=app_id):
                app_service_ids.append(service.id)
            if service_id_list == None:
                service_id_list = app_service_ids
            else:
                service_id_list = list(set(service_id_list).intersection(set(app_service_ids)))
        elif app_name:
            app = App.objects.filter(name=app_name)
            aid = 0
            if len(app) > 0:
                aid = app[0].id
            for service in AppService.objects.filter(app_id=aid):
                app_service_ids.append(service.id)
            if service_id_list == None:
                service_id_list = app_service_ids
            else:
                service_id_list = list(set(service_id_list).intersection(set(app_service_ids)))

        if service_id:
            hostids = []
            for s in ServiceHost.objects.filter(service_id=service_id):
                hostids.append(s.host_id)
            queryset = queryset.filter(id__in=hostids)
        elif service_name:
            appservice = AppService.objects.filter(name=service_name)
            sid = None
            if len(appservice) > 0:
                sid = appservice[0].id
            hostids = []
            for s in ServiceHost.objects.filter(service_id=sid):
                hostids.append(s.host_id)
            queryset = queryset.filter(id__in=hostids)

        if service_type or app_id or app_name or group:
            hostids = []
            if len(service_id_list) > 0:
                for s in ServiceHost.objects.filter(service_id__in=service_id_list):
                    hostids.append(s.host_id)
            hostids = list(set(hostids))
            queryset = queryset.filter(id__in=hostids)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        results = HostValidate().formatHostList(serializer.data)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    @transaction.atomic()
    def perform_create(self, serializer):
        envs = []
        for c in Hosts.HOST_ENV_CHOICES:
            envs.append(c[0])
        types = []
        for t in Hosts.HOST_TYPE_CHOICES:
            types.append(t[0])
        attributes = []
        for a in Hosts.HOST_ATTRIBUTE_CHOCIES:
            attributes.append(a[0])
        ip = self.request.data.get('ip', '')
        oobip = self.request.data.get('oobip', '')
        sn = self.request.data.get('sn', '')
        mac = self.request.data.get('mac', '')
        env = self.request.data.get('env', '')
        type = self.request.data.get('type', '')
        attribute = self.request.data.get('attribute', '')
        hostname = self.request.data.get('hostname', '')
        service_ids = self.request.data.getlist('service_id[]', [])
        aliyun_id = self.request.data.get('aliyun_id', None)
        status, msg = HostValidate().checkAddHost(hostname=hostname, ip=ip, oobip=oobip, sn=sn, mac=mac, env=env, type=type, attribute=attribute, aliyun_id=aliyun_id)
        if not status:
            raise APIValidateException(msg)
        current_time = int(time.time())
        if type == 'server':
            service_id = configs.FREE_SERVER_ID
        elif type == 'vm':
            service_id = configs.FREE_VM_ID
        else:
            service_id = 0
        free_list = (configs.FREE_SERVER_ID, configs.FREE_VM_ID)
        for sid in service_ids:
            if sid in free_list:
                raise APIValidateException(u'不能选择资源池')
        state = 'offline'
        if service_id in free_list and len(service_ids) <= 0:
            state = 'free'
        if len(service_ids) > 0:
            serivce = AppService.objects.filter(id__in=service_ids)
            if len(serivce) < len(service_ids):
                raise APIValidateException(u'服务不存在')
        else:
            service_ids.append(service_id)
        obj = serializer.save(ctime=current_time, state=state, service_id=service_ids[0], instance_id=str(uuid.uuid1()))
        ###################### 将ip设为已使用 ######################
        if ip:
            IpAddress.objects.filter(ip=ip).update(state='used')
        ###################### 将ip设为已使用 ######################
        for sid in service_ids:
            ServiceHost.objects.create(service_id=sid, host_id=obj.id)
        dict_obj = model_to_dict(obj)
        dict_obj['service_ids'] = service_ids
        json_obj = json.dumps(dict_obj)
        self.changeLog(obj.id, obj.ip, json_obj)

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(Hosts.objects.filter(id__in=id_list, state='online')) > 0:
            raise APIValidateException(u'online状态的主机,不能删除')
        hosts = Hosts.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        hids = []
        iplist = []
        for a in hosts:
            hids.append(a.id)
            iplist.append(a.ip)
            h = model_to_dict(a)
            h['state'] = 'deleted'
            HostDeleted.objects.create(**h)
            self.changeLog(a.id, a.ip, 'delete host: ' + a.ip, uid=uid)
            ###################### 删除主机的时候删除对应的监控 ######################
            try:
                DelMonitorTask().addTask(request.user.username, ip=a.ip)
            except Exception, ex:
                logger.error(str(ex))
            ###################### 删除主机的时候删除对应监控 ######################

        ServiceHost.objects.filter(host_id__in=hids).delete()
        hosts.delete()

        ###################### 将ip设为空闲 ######################
        IpAddress.objects.filter(ip__in=iplist).update(state='free')
        ###################### 将ip设为空闲 ######################

        ###################### 删除主机的时候删除对应的授权信息 ######################
        AuthRecord.objects.filter(host_id__in=hids).delete()
        ###################### 删除主机的时候删除对应的授权信息 ######################

        return Response({"success": True, "msg": "succ!", "errors": []})

class HostsDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    主机详情页

    输入/输出参数：
    ● id                        ——   PK
    ● instance_id               ——   实例id
    ● sn                        ——   序列号
    ● type                      ——   主机类型(server, vm, net, aliyun, storage)(必输)
    ● attribute                 ——   属性(ECS, RDS, SLB, server, xen, switch, xenparent, dockerparent, docker, route, firewall, storage)(必输)
    ● service_id                ——   服务id
    ● service_name              ——   服务名称
    ● room_id                   ——   机房id(必输)
    ● location                  ——   u位
    ● rack_id                   ——   机柜id
    ● conf_id                   ——   配置id
    ● model_id                  ——   型号id
    ● pid                       ——   宿主机id(即宿主机的主机id)
    ● state                     ——   状态(free、online、offline、release、broken、delete、install)(必输)
    ● hostname                  ——   主机名(必输)
    ● ip                        ——   ip
    ● oobip                     ——   管理ip
    ● ctime                     ——   创建时间
    ● expiration_time           ——   过保时间(到期时间)
    ● aliyun_id                 ——   阿里云实例id
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    serializer_class = HostsSerializer

    def put(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许put操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def perform_destroy(self, instance):
        if instance.state == 'online':
            raise APIValidateException(u'online状态的主机不能删除')
        # host = Hosts.objects.filter(id=instance.id)
        # if len(host) <= 0:
        #     raise APIValidateException(u'主机不存在')
        h = model_to_dict(instance)
        ServiceHost.objects.filter(host_id=instance.id).delete()
        h['state'] = 'deleted'
        HostDeleted.objects.create(**h)
        instance.delete()

        ###################### 删除主机的时候删除对应的授权信息 ######################
        AuthRecord.objects.filter(host_id=instance.id).delete()
        ###################### 删除主机的时候删除对应的授权信息 ######################

        ###################### 将ip设为空闲 ######################
        IpAddress.objects.filter(ip=instance.ip).update(state='free')
        ###################### 将ip设为空闲 ######################

        ###################### 删除主机的时候删除对应的监控 ######################
        try:
            DelMonitorTask().addTask(self.request.user.username, ip=instance.ip)
        except Exception, ex:
            logger.error(str(ex))
        ###################### 删除主机的时候删除对应监控 ######################

        self.changeLog(instance.id, instance.ip, 'delete host: ' + instance.ip)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @transaction.atomic()
    def perform_update(self, serializer):
        id = self.kwargs.get('pk', None)
        state = self.request.data.get('state', None)
        service_id = self.request.data.get('service_id', None)
        hostname = self.request.data.get('hostname', None)
        ip = self.request.data.get('ip', None)
        host = Hosts.objects.filter(id=id)
        if len(host) <= 0:
            raise APIValidateException(u'主机不存在')
        host = host[0]
        if host.state == 'online':
            raise APIValidateException(u'不能修改online状态的主机信息')
        if state != None and state != host.state:
            raise APIValidateException(u'只能通过changestate api修改主机状态')
        if service_id != None and service_id != host.service_id:
            raise APIValidateException(u'只能通过changeservice api修改主机所属服务')
        if hostname and hostname != host.hostname:
            raise APIValidateException(u'只能通过changehostname api修改主机名')
        if ip and ip != host.ip:
            raise APIValidateException(u'不能修改ip, 请删除主机重新录入')
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.ip, json_obj)


class HostsUpload(CmdbListCreateAPIView):
    """
    主机列表/创建主机.

    输入参数：
    ● file                      ——   设备csv文件(必输)

    输出参数：
    ● success                   ——   操作状态:true-上传成功,false-上传失败
    ● msg                       ——   返回消息
    ● errors                    ——   错误提示(list)
    """

    paginate_by = None
    queryset = Hosts.objects.all()
    serializer_class = HostsSerializer

    def _allowed_methods(self):
        return ['POST', 'HEAD', 'OPTIONS']

    def put(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        errors = []
        data = {"success": False, "msg": "succ!", "errors": errors}
        file = request.FILES.get("file", None)
        if file:
            head = []
            body = []
            i = 0
            for content in file.chunks():
                for c in content.split("\n"):
                    if c:
                        if i == 0:
                            head = c.split(",")
                        else:
                            body.append(c.split(","))
                        i += 1
            host_list = []
            for b in body:
                t = {}
                j = 0
                for h in head:
                    try:
                        t[h] = b[j]
                        j += 1
                    except:
                        t[h] = ''
                host_list.append(t)

        validate_host_list = []
        for h in host_list:
            state, msg = HostValidate().checkAddHost(**h)
            if state:
                validate_host_list.append(msg)
            else:
                t = h
                t['error'] = msg
                errors.append(t)
        if len(errors) > 0:
            data['errors'] = errors
            raise APIValidateException(data)

        self.saveUploadHost(validate_host_list)
        data['success'] = True
        return Response(data)

    @transaction.atomic()
    def saveUploadHost(self, host_list):
        iplist = []
        for h in host_list:
            iplist.append(h['ip'])
            if not h.has_key('service_id'):
                h['service_id'] = 0
            obj = Hosts.objects.create(instance_id=str(uuid.uuid1()), **h)
            ServiceHost.objects.create(service_id=h['service_id'], host_id=obj.id)
            dict_obj = model_to_dict(obj)
            dict_obj['service_ids'] = [dict_obj['service_id']]
            json_obj = json.dumps(dict_obj)
            self.changeLog(obj.id, obj.ip, json_obj)
        ###################### 将ip设为空闲 ######################
        IpAddress.objects.filter(ip__in=iplist).update(state='used')
        ###################### 将ip设为空闲 ######################

class ImageList(CmdbListCreateAPIView):
    """
    系统模板列表/创建模板.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● name                      ——   模板名称

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   镜像名称(必输)
    ● image_id                  ——   镜像编号(阿里云中的编码)
    ● img_type                   ——   操作系统类型(linux, windows)
    ● platform                  ——   操作系统平台(CentOS, Ubuntu, RedHat, Windows Server, other)
    ● tag                       ——   标签
    ● ctime                     ——   创建时间

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = Image.objects.all()
    filter_fields = ('name', 'os_type', 'platform', )
    search_fields = ['name', 'description']
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ImageSerializer

    def _allowed_methods(self):
        return ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS']

    def get_queryset(self):
        queryset = Image.objects.all().order_by("-id")
        id = self.request.query_params.get('id', None)

        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        results = []
        img_ids = []
        for h in serializer.data:
            img_ids.append(h['id'])
        ImageTag_dict = defaultdict(list)
        for seg in ImageTag.objects.filter(img_id__in=img_ids):
            ImageTag_dict[seg.img_id].append(seg.tag)
        for h in serializer.data:
            t = h
            t['tag'] = ''
            if ImageTag_dict.has_key(h['id']):
                t['tag'] = "\n".join(ImageTag_dict[h['id']])
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    @transaction.atomic()
    def perform_create(self, serializer):
        name = self.request.data.get('name', '')
        tag = self.request.data.get('tag', '')
        if not name:
            raise APIValidateException('name is required')
        if len(Image.objects.filter(name=name)) > 0:
            raise APIValidateException('os ' + name + ' already exist')
        current_time = int(time.time())
        obj = serializer.save(ctime=current_time)
        if tag:
            for t in tag.split("\n"):
                ImageTag.objects.create(img_id=obj.id, tag=t)
        obj_dict = model_to_dict(obj)
        obj_dict['tag'] = tag.split("\n")
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.name, json_obj)

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(Hosts.objects.filter(img_id__in=id_list)) > 0:
            raise APIValidateException('os already in use can not delete')
        oslist = Image.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in oslist:
            self.changeLog(a.id, a.name, 'delete os: ' + a.name, uid=uid)
        oslist.delete()
        ImageTag.objects.filter(img_id__in=id_list).delete()
        return Response({"success": True, "msg": "succ!", "errors": []})


class ImageDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    系统模板详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   镜像名称(必输)
    ● image_id                  ——   镜像编号(阿里云中的编码)
    ● img_type                  ——   操作系统类型(linux, windows)
    ● platform                  ——   操作系统平台(CentOS, Ubuntu, RedHat, Windows Server, other)
    ● tag                       ——   标签
    ● ctime                     ——   创建时间
    """
    paginate_by = None
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if len(Hosts.objects.filter(img_id=id)):
            raise APIValidateException('os ' + instance.name + ' already in use can not delete')
        instance.delete()
        ImageTag.objects.filter(img_id=id).delete()
        self.changeLog(instance.id, instance.name, 'delete image: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)

        # 配置网段
        ImageTag.objects.filter(img_id=obj.id).delete() # 先删除网段
        tag = self.request.data.get('tag', '')
        if tag:
            for t in tag.split("\n"):
                ImageTag.objects.create(img_id=obj.id, tag=t)

        obj_dict = model_to_dict(obj)
        obj_dict['tag'] = tag.split("\n")
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.name, json_obj)


class ChangeHostState(CmdbListCreateAPIView):
    """
    修改主机状态.

    输入参数：
    ● id[]                      ——   主机id列表
    ● id                        ——   主机id(多个id用逗号隔开)
    ● state                     ——   状态(必输)
    注:id[]和id不能都为空
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']


    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        state_list = []
        for s in Hosts.HOST_STATE_CHOCIES:
            state_list.append(s[0])
        data = {'success': True, 'msg': u'修改主机状态操作成功'}

        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        ip = request.data.get('ip', '')
        if ip:
            try:
                intid = Hosts.objects.get(ip=ip).id
                id_list.append(str(intid))
            except Exception, ex:
                raise APIValidateException(u'ip不存在')


        state = request.data.get("state", '')
        if len(id_list) <= 0 and not id and not ip:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if id:
            id_list += id.split(",")
        if state not in state_list:
            raise APIValidateException(u'state必须为 ' + " ".join(state_list) + u' 中的一个')
        host_list = Hosts.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for h in host_list:
            if h.service_id in (configs.FREE_SERVER_ID, configs.FREE_VM_ID) and state not in ('free', 'unuse'):
                raise APIValidateException(u'资源池中的机器只能改为free或unuse状态')
            if state == 'free':
                service_id = 0
                if h.type == "server":
                    service_id = configs.FREE_SERVER_ID
                elif h.type == 'vm':
                    service_id = configs.FREE_VM_ID
                self.changeLog(h.id, h.ip, 'change host state from ' + h.state + ' to ' + state + ' and change service_id from ' + str(h.service_id) + ' to ' + str(service_id), uid=uid)
            else:
                self.changeLog(h.id, h.ip, 'change host state from ' + h.state + ' to ' + state, uid=uid)
        if state == 'free':
            for h in host_list:
                service_id = 0
                if h.type == "server":
                    service_id = configs.FREE_SERVER_ID
                elif h.type == 'vm':
                    service_id = configs.FREE_VM_ID
                Hosts.objects.filter(id=h.id).update(service_id=service_id, state=state)
                ServiceHost.objects.filter(host_id=h.id).delete()
                ServiceHost.objects.create(host_id=h.id, service_id=service_id)
        else:
            host_list.update(state=state)
        for h in host_list:
            ################################# 添加监控或修改监控状态 #################################
            try:
                HostMonitorTask().addTask(request.user.username, ip=h.ip, state=state, type=h.type, attribute=h.attribute)
            except Exception, ex:
                logger.error(str(ex))
                print str(ex)
            ################################# 添加监控或修改监控状态 #################################
        return Response(data)

class ChangeHostService(CmdbListCreateAPIView):
    """
    修改主机所属服务.

    输入参数：
    ● id[]                      ——   主机id列表
    ● id                        ——   主机id(多个id用逗号隔开)
    ● service_id[]              ——   服务id列表
    ● service_id                ——   服务id(必输,多个id用逗号隔开)
    注:id[]和id不能都为空,service_id[]和service_id不能同时为空
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        data = {'success': True, 'msg': u'主机移动操作成功'}
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        service_id = request.data.get("service_id", '')
        service_id_list = request.data.getlist("service_id[]", '')
        if len(service_id_list) <= 0 and not service_id:
            raise APIValidateException(u'service_id[]和service_id不能同时为空')
        if service_id:
            service_id_list += service_id.split(",")
        # old_service_id = request.data.get("old_service_id", 0)
        # if not old_service_id:
        #     raise APIValidateException(u'old_service_id不能为空')
        if len(id_list) <= 0 and not id:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if id:
            id_list += id.split(",")
        service_id_list = list(set(service_id_list))
        service_list = AppService.objects.filter(id__in=service_id_list)
        if len(service_list) < len(service_id_list):
            raise APIValidateException(u"服务不存在")
        if len(Hosts.objects.filter(id__in=id_list, state='online')) > 0:
            raise APIValidateException(u'不能移动online状态的主机')
        host_list = Hosts.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        # 先删除老的主机挂载信息
        ServiceHost.objects.filter(host_id__in=id_list).delete()
        for service in service_list:
            for h in host_list:
                if service.id in (configs.FREE_VM_ID, configs.FREE_SERVER_ID):
                    self.changeLog(h.id, h.ip, 'change host service_id from ' + str(h.service_id) + ' to ' + str(service.id) + ' and change host state from ' + h.state + ' to free', uid=uid)
                else:
                    self.changeLog(h.id, h.ip, 'change host service_id from ' + str(h.service_id) + ' to ' + str(service.id), uid=uid)
            if service.id in (configs.FREE_VM_ID, configs.FREE_SERVER_ID):
                raise APIValidateException(u'不能移动到资源池,请把主机状态改为free')
            # 将主机移动到指定服务下
            for hid in id_list:
                # 如果目标服务下没有该主机则将主机移动过去
                if len(ServiceHost.objects.filter(service_id=service.id, host_id=hid)) <= 0:
                    ServiceHost.objects.create(service_id=service.id, host_id=hid)
                    ############################### 更改主机名 ###############################
                    try:
                        autoHostName(request.user.username, hid)
                    except Exception, ex:
                        pass
                    ############################### 更改主机名 ###############################
        host_list.update(service_id=service.id, state='offline')
        return Response(data)

class MountHostService(CmdbListCreateAPIView):
    """
    挂载主机.

    输入参数：
    ● id[]                      ——   主机id列表
    ● id                        ——   主机id(多个id用逗号隔开)
    ● service_id[]              ——   服务id列表
    ● service_id                ——   服务id(必输,多个id用逗号隔开)
    注:id[]和id不能都为空,service_id[]和service_id不能都为空
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['POST', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        data = {'success': True, 'msg': u'主机挂载操作成功'}
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        service_id = request.data.get("service_id", '')
        service_id_list = request.data.getlist("service_id[]", '')
        if len(service_id_list) <= 0 and not service_id:
            raise APIValidateException(u'service_id[]和service_id不能同时为空')
        if service_id:
            service_id_list += service_id.split(",")

        if len(id_list) <= 0 and not id:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if id:
            id_list += id.split(",")
        service_id_list = list(set(service_id_list))
        service_list = AppService.objects.filter(id__in=service_id_list)
        if len(service_list) < len(service_id_list):
            raise APIValidateException(u"服务不存在")
        if len(Hosts.objects.filter(id__in=id_list, state='online')) > 0:
            raise APIValidateException(u'不能挂载online状态的主机')
        host_list = Hosts.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        free_service_list = (configs.FREE_VM_ID, configs.FREE_SERVER_ID)

        # 将主机从资源池中删除
        ServiceHost.objects.filter(service_id__in=free_service_list, host_id__in=id_list).delete()

        for service in service_list:
            for h in host_list:
                if service.id in (configs.FREE_VM_ID, configs.FREE_SERVER_ID):
                    self.changeLog(h.id, h.ip, 'change host service_id from ' + str(h.service_id) + ' to ' + str(service.id) + ' and change host state from ' + h.state + ' to free', uid=uid)
                else:
                    self.changeLog(h.id, h.ip, 'change host service_id from ' + str(h.service_id) + ' to ' + str(service.id), uid=uid)
            if service.id in free_service_list:
                raise APIValidateException(u'不能挂载到资源池,请把主机状态改为free')

            # 将主机挂载到指定服务下
            for hid in id_list:
                # 如果目标服务下没有该主机则将主机挂载过去
                if len(ServiceHost.objects.filter(service_id=service.id, host_id=hid)) <= 0:
                    ServiceHost.objects.create(service_id=service.id, host_id=hid)
                    ############################### 更改主机名 ###############################
                    try:
                        autoHostName(request.user.username, hid)
                    except Exception, ex:
                        pass
                    ############################### 更改主机名 ###############################
        host_list.update(service_id=service.id, state='offline')
        return Response(data)

class AddAliyunInstance(CmdbListCreateAPIView):
    """
    阿里云设备录入.

    输入参数：
    ● aliyun_id                 ——   阿里云实例id(多个id用换行隔开)(必输)
    ● attribute                 ——   实例类型(必输)
    ● service_id[]              ——   服务id列表
    ● amount                    ——   费用(必输)
    注:id[]和id不能都为空
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['POST', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        errors = []
        env_list = []
        for e in Hosts.HOST_ENV_CHOICES:
            env_list.append(e[0])
        data = {'success': True, 'msg': 'succ!', 'errors': []}
        env = request.data.get('env', 'prod')
        aliyun_id = request.data.get('aliyun_id', '')
        attribute = request.data.get('attribute', 'ECS')
        service_ids = request.data.getlist('service_id[]', [])
        amount = request.data.get('amount', 0)
        if not env:
            raise APIValidateException(u'env不能为空')
        if env not in env_list:
            raise APIValidateException(u'env必须为' + ",".join(env_list) + u'中的一个')
        if not aliyun_id:
            raise APIValidateException(u'实例id不能为空')
        id_list = aliyun_id.split('\n')
        if len(id_list) > 100:
            raise APIValidateException(u'实例id不能超过100个')
        if attribute != 'ECS':
            raise APIValidateException(u'实例类型只支持ECS')
        status, result = AliyunECSApi().getECSHostListByID(id_list)
        if not status:
            raise APIValidateException(result)
        service_ids = list(set(service_ids))
        if len(service_ids) > 0 and len(AppService.objects.filter(id__in=service_ids)) < len(service_ids):
            raise APIValidateException(u'服务不存在')
        host_list = []
        service_id = 0
        if len(service_ids) > 0:
            service_id = service_ids[0]
        for h in result:
            t = h
            t['env'] = env
            t['amount'] = amount
            t['service_id'] = service_id
            res, host = HostValidate().checkAddHost(**t)
            if not res:
                t['error'] = host
                errors.append(t)
                continue
            host_list.append(host)
        if len(errors) > 0:
            data['errors'] = errors
            data['success'] = False
            data['msg'] = 'fail!'
            raise APIValidateException(data)
        for host in host_list:
            host['instance_id'] = str(uuid.uuid1())
            h = Hosts.objects.create(**host)
            for s in service_ids:
                ServiceHost.objects.create(service_id=s, host_id=h.id)
        return Response(data)

class ChangeHostName(CmdbListCreateAPIView):
    """
    修改主机名.

    输入参数：
    ● id                        ——   主机id(必输)
    ● hostname                  ——   主机名(必输)
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        cuser = request.user.username
        data = {'success': True, 'msg': u'修改主机名操作成功'}
        id = request.data.get('id', '')
        hostname = request.data.get("hostname", '')
        status, host = changeHostNameById(cuser, id, hostname)
        if not status:
            raise APIValidateException(host)
        self.changeLog(id, host['ip'], 'change hostname from ' + host['hostname'] + " to " + hostname)
        return Response(data)

class SyncAliyun(CmdbListCreateAPIView):
    """
    同步阿里云主机.

    输入参数：
    无
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['POST', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        status, count = importECS()
        if not status:
            raise APIValidateException(u'同步阿里云主机失败:' + count)
        msg = u'同步成功:'
        if count == 0:
            msg += u'本次同步没有新增主机'
        elif count > 0:
            msg += u'本次同步新增' + str(count) + u'台主机'
        return Response({'success': True, 'msg': msg})

class UpdateFromAliyun(CmdbListCreateAPIView):
    """
    更新阿里云主机.

    输入参数：
    ● id                        ——   主机id(必输)
    """
    paginate_by = None
    queryset = Hosts.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        cuser = request.user.username
        data = {'success': True, 'msg': u'修改主机名操作成功'}
        id = request.data.get('id', '')
        hostname = request.data.get("hostname", '')
        status, host = changeHostNameById(cuser, id, hostname)
        if not status:
            raise APIValidateException(host)
        self.changeLog(id, host['ip'], 'change hostname from ' + host['hostname'] + " to " + hostname)
        return Response(data)

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        id = request.data.get('id', 0)
        if not id:
            raise APIValidateException(u'主机id不能为空')
        hosts = Hosts.objects.filter(id=id)
        if len(hosts) <= 0:
            raise APIValidateException(u'主机不存在')
        host = hosts[0]
        if host.state == 'online':
            raise APIValidateException(u'不能修改online状态的主机信息')
        if not host.aliyun_id or host.type != 'aliyun':
            raise APIValidateException(u'不是阿里云主机不能更新')
        status, aliyun_host = AliyunECSApi().getECSHostListByID([host.aliyun_id])
        if not status:
            raise APIValidateException(aliyun_host)
        if len(aliyun_host) <= 0:
            raise APIValidateException(u'阿里云主机不存在')
        aliyun_host = aliyun_host[0]
        status, hostname = sshGetHostName(aliyun_host['ip'])
        if not status:
            hostname = aliyun_host['hostname']
        hosts.update(ip=aliyun_host['ip'], hostname=hostname, publicip=aliyun_host['publicip'], cpu=aliyun_host['cpu'],
               memory=aliyun_host['memory'], os_name=aliyun_host['os_name'])
        self.changeLog(id, host.ip, json.dumps(model_to_dict(host)))
        return Response({'success': True, 'msg': 'succ!'})

class PwdPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff

class HostPasswordApi(CmdbListCreateAPIView):

    """
    查看/修改主机密码.

    查询参数：
    ● ip                        ——   主机ip(必输)

    输入/输出参数：
    ● ip                        ——   主机ip(必输)
    ● password                  ——   root密码(必输)
    """

    permission_classes = (PwdPermission,)

    paginate_by = None
    queryset = HostPassword.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostPasswordSerializer

    def get(self, request, *args, **kwargs):
        ip = request.GET.get('ip', '')
        if not ip:
            raise APIValidateException(u'ip不能为空')
        if len(Hosts.objects.filter(ip=ip)) <= 0:
            raise APIValidateException(u'主机不存在')
        pwd = HostPassword.objects.filter(ip=ip)
        if len(pwd) <= 0:
            raise APIValidateException(u'未保存该主机密码')
        pwd = pwd[0].password
        pc = Prpcrypt(configs.AES_KEY)
        pwd = pc.decrypt(pwd)
        return Response({"password": pwd})

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'PATCH', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        data = {'success': True, 'msg': u'修改主机密码操作成功'}
        ip = request.data.get('ip', '')
        password = request.data.get("password", '')
        if not ip:
            raise APIValidateException(u'ip不能为空')
        if not password:
            raise APIValidateException(u'password不能为空')
        if len(Hosts.objects.filter(ip=ip)) <= 0:
            raise APIValidateException(u'主机不存在')
        pc = Prpcrypt(configs.AES_KEY)
        password = pc.encrypt(str(password))
        HostPassword.objects.filter(ip=ip).delete()
        HostPassword.objects.create(ip=ip, password=password)
        self.changeLog(ip, ip, 'change root password')
        return Response(data)

class HostInfoByAnsibleApi(CmdbListCreateAPIView):
    """
       主机详情页.

       输入/输出参数：
       ● id                        ——   PK(无需输入)
       ● ip                        ——   ip地址
       ● network                   ——   网段
       ● gateway                   ——   网关
       ● netmask                   ——   掩码
       ● fqdn                      ——   fqdn
       ● network_card              ——   网卡
       ● mac                       ——   mac地址
       ● os_name                   ——   系统名称
       ● kernel                    ——   内核版本
       ● cpu                       ——   cpu
       ● memory                    ——   内存

    """
    serializer_class = HostInfoSerializer

    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic()     #删除所有的数据
    def delete(self, request, *args, **kwargs):
        hosts = HostInfo.objects.all()
        hosts.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})
