# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import random
import re
import time
import uuid
from collections import defaultdict

from django.db import transaction
from django.forms.models import model_to_dict
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response

from app.auto.autoapi import AutoApi
from app.models import AppService, App, AppSegment, Group, AppPrincipals, ServicePrincipals, ServiceResource
from app.models import ServiceHost
from app.serializers import AppServiceSerializer, AppSerializer, GroupSerializer, AppPrincipalsSerializer, \
    ServiceResourceSerializer
from asset.models import Conf
from cmdb import configs
from host.lib.host_tools import autoHostName
from host.models import Hosts, Image
from host.serializers import HostsSerializer
from lb.models import *
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView, HttpResponse
from public.base_exception import APIValidateException
from public.common.tools import get_maskint_by_segment, exchange_maskint, get_segment_by_ip_mask

class GroupList(CmdbListCreateAPIView):
    """
    业务线列表.

    输入/输出参数：
    ● id                        ——   ID(不用输入)
    ● name                      ——   业务线名称(必输)
    ● full_name                 ——   业务线全称(必输)
    ● owner                     ——   负责人
    ● comment                   ——   备注

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """

    paginate_by = None
    queryset = Group.objects.all()          # 查出所有 group 的值

    search_fields = ('name', 'full_name', 'comment')     # 精确查询的字段
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = GroupSerializer       # 业务线的序列化

    @transaction.atomic()
    def perform_create(self, serializer):

        obj = serializer.save()
        obj_dict = model_to_dict(obj)
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.name, json_obj)     # 写日志

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):        # args 相当是一个集合，kwargs 相当是一个字典
        id_list = request.data.getlist('id[]', [])     # 获取 id 列表
        id = request.data.get('id', '')                # 获取 id

        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        groups = Group.objects.filter(id__in=id_list)      # 过滤出 id 在 id_list 的 groups
        uid = str(uuid.uuid1())        # 生成唯一的 id

        group_names = []
        for a in groups:
            group_names.append(a.name)
            self.changeLog(a.id, a.name, 'delete group: ' + a.name, uid=uid)
        if len(App.objects.filter(group__in=group_names)) > 0:       # 判断该组下面还有没有 App
            raise APIValidateException(u'业务线下还有应用,不能删除')   # 抛出异常
        groups.delete()      # 删除相应的 groups
        return Response({"success": True, "msg": "succ!", "errors": []})       # 该函数返回 Response 对象

class GroupDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    业务线详情页

    输入/输出参数：
    ● id                        ——   ID(不用输入)
    ● name                      ——   业务线名称(必输)
    ● full_name                 ——   业务线全称(必输)
    ● owner                     ——   负责人
    ● comment                   ——   备注

    """

    paginate_by = None
    queryset = Group.objects.all()                                 # 查询所有数据
    serializer_class = GroupSerializer                             # 序列化业务线对象

    @transaction.atomic()                                          # 对业务线的删除操作
    def perform_destroy(self, instance):
        id = instance.id
        if len(App.objects.filter(group=instance.name)) > 0:       # 过滤出 group == instance.name 的 App 对象（检查该业务线下有没有 App）
            raise APIValidateException(u'业务线下存在应用,不能删除')
        instance.delete()                                          # 如果该业务线下没有 App 则删除
        self.changeLog(id, instance.name, 'delete group: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):

        id = self.kwargs.get('pk', '')               # 获取主键 id

        name = self.request.data.get('name', '')     # 获取 name

        groups = Group.objects.filter(id=id)         # 过滤出相应 id 的组

        if len(groups) <= 0:                         # 没有相应的业务线
            raise APIValidateException(u'业务线不存在')
        if not name:                                      # name 不能为空
            raise APIValidateException(u'name不能为空')
        group = groups[0]
        if name != group.name:                            # 如果 App 中业务线的名称与传进来的名称不相符则更新 App 中的业务线的名称
            App.objects.filter(group=group.name).update(group=name)     # 更新 App 中业务线的名称
        obj = serializer.save()
        obj_dict = model_to_dict(obj)         # 将 model 转化为 dict（字典）
        json_obj = json.dumps(obj_dict)       # 将 dict 对象转换为 str 形式
        self.changeLog(obj.id, obj.name, json_obj)

class AppList(CmdbListCreateAPIView):
    """
    应用列表/创建应用.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● name                      ——   名称
    ● group                     ——   业务线
    ● search                    ——   搜索(名称/备注)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   名称(必输)
    ● group                     ——   业务线名称
    ● segment                   ——   网段(多个网段用换行表示)
    ● comment                   ——   备注
    ● auto                      ——   是否在auto创建(on:是)

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """

    paginate_by = None
    queryset = App.objects.all()

    filter_fields = ('group', 'name', )     # 过滤的字段
    search_fields = ('name', 'comment')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = AppSerializer

    def get_queryset(self):
        queryset = App.objects.all().order_by("-id")
        id = self.request.query_params.get('id', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    @transaction.atomic()
    def perform_create(self, serializer):
        obj = serializer.save()

        # 配置网段
        segment = self.request.data.get('segment', '')
        auto = self.request.data.get('auto', '')
        if segment:
            for s in segment.split("\n"):
                maskint = get_maskint_by_segment(s)
                if not maskint:
                    raise APIValidateException(u'网段不合法')
                AppSegment.objects.create(app_id=obj.id, segment=s)

        obj_dict = model_to_dict(obj)
        obj_dict['segment'] = segment.split("\n")
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.name, json_obj)
        if auto == 'on':
            AutoApi().addProject(obj.name, obj.cname, obj.comment)

        # 增添负责人信息
        users = self.request.data.getlist("user_name[]", [])
        for user in users:
            AppPrincipals.objects.create(app_id=obj.id, user_name=user, type=2)

        # 增添负责人信息
        sas = self.request.data.getlist("sa_name[]", [])
        for sa in sas:
            AppPrincipals.objects.create(app_id=obj.id, user_name=sa, type=1)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        results = []
        app_ids = []
        for h in serializer.data:
            app_ids.append(h['id'])
        appsegment_dict = defaultdict(list)
        for seg in AppSegment.objects.filter(app_id__in=app_ids):
            appsegment_dict[seg.app_id].append(seg.segment)
        for h in serializer.data:
            t = h
            t['segment'] = ''
            if appsegment_dict.has_key(h['id']):
                t['segment'] = "\n".join(appsegment_dict[h['id']])

            t['user_name'] = []
            for a in AppPrincipals.objects.filter(app_id=t['id']).filter(type=2):
                t['user_name'].append(a.user_name)

            t['sa_name'] = []
            for a in AppPrincipals.objects.filter(app_id=t['id']).filter(type=1):
                t['sa_name'].append(a.user_name)
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(AppService.objects.filter(app_id__in=id_list)) > 0:
            raise APIValidateException(u'应用下还有服务,不能删除')

        #获取 app_principals 表中要删除数据集合
        for id in id_list:
            principals = AppPrincipals.objects.filter(app_id=id)       # 循环获取集合
            principals.delete()                             # 批量删除负责人表中的数据
            if id == configs.RESOURCE_POOL_ID:
                raise APIValidateException(u'应用为资源池,不能删除')
        apps = App.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in apps:
            self.changeLog(a.id, a.name, 'delete application: ' + a.name, uid=uid)
        apps.delete()

        AppSegment.objects.filter(app_id__in=id_list).delete() # 删除网段
        return Response({"success": True, "msg": "succ!", "errors": []})

class AppDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    应用详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   名称(必输)
    ● group                     ——   业务线名称
    ● segment                   ——   网段(多个网段用换行表示)
    ● comment                   ——   备注
    """

    paginate_by = None
    queryset = App.objects.all()
    serializer_class = AppSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if id == configs.RESOURCE_POOL_ID:
            raise APIValidateException(u'应用 ' + instance.name + u' 为资源池,不能删除')
        if len(AppService.objects.filter(app_id=id)):
            raise APIValidateException(u'应用 ' + instance.name + u' 下还有服务,不能删除')
        instance.delete()

        AppSegment.objects.filter(app_id=id).delete()
        self.changeLog(id, instance.name, 'delete application: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):
        id = self.kwargs.get('pk', '')
        app = App.objects.filter(id=id)
        oldname = ''
        if len(app) > 0:
            oldname = app[0].name
        obj = serializer.save()

        # 配置网段
        AppSegment.objects.filter(app_id=obj.id).delete() # 先删除网段
        segment = self.request.data.get('segment', '')
        if segment:
            for s in segment.split("\n"):
                maskint = get_maskint_by_segment(s)
                if not maskint:
                    raise APIValidateException(u'网段不合法')
                AppSegment.objects.create(app_id=obj.id, segment=s)

        # user 相应更新
        old_users = AppPrincipals.objects.filter(app_id=id)
        old_users.delete()      # 先删除旧数据

        new_principals = self.request.data.getlist('user_name[]')  # 创建新负责人的数据
        for principal in new_principals:
                AppPrincipals.objects.create(app_id=id,user_name=principal,type=2)

        new_sas = self.request.data.getlist('sa_name[]')  # 创建新负责人的数据
        for new_sa in new_sas:
            AppPrincipals.objects.create(app_id=id, user_name=new_sa, type=1)


        obj_dict = model_to_dict(obj)
        obj_dict['segment'] = segment.split("\n")
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.name, json_obj)
        AutoApi().updateProject(oldname, obj.name, obj.cname, obj.comment)

class AppServiceList(CmdbListCreateAPIView):
    """
    服务列表/创建服务.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● app_id                    ——   服务id
    ● type                      ——   服务类型
    ● name                      ——   服务名称
    ● state                     ——   状态
    ● search                    ——   搜索(名称/备注)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● app_id                    ——   应用id(必输)
    ● app_name                  ——   应用名称
    ● name                      ——   服务名称(必输)
    ● hostcount                 ——   主机数量(无需输入)
    ● type                      ——   服务类型
    ● comment                   ——   备注
    ● auto                      ——   是否在auto创建(on:是)
    ● vcs_rep                   ——   版本库地址

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """

    paginate_by = None
    queryset = AppService.objects.all()

    filter_fields = ('app_id', 'type', 'name', 'state')
    search_fields = ('name', 'comment')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = AppServiceSerializer

    def get_queryset(self):
        domain = self.request.query_params.get('domain')
        group = self.request.query_params.get('group', '')
        state = self.request.query_params.get('state', 'online')
        queryset = AppService.objects.all().order_by("-id")
        # if domain:
        #     queryset = queryset.filter(id__in=)
        if group:
            appids = []
            for a in App.objects.filter(group=group):
                appids.append(a.id)
            queryset = queryset.filter(app_id__in=list(set(appids)))
        id = self.request.query_params.get('id', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        if state:
            queryset = queryset.filter(state=state)

        return queryset

    @transaction.atomic()
    def perform_create(self, serializer):
        app_id = self.request.data.get('app_id', 0)
        name = self.request.data.get('name', '')
        vcsRep = self.request.data.get('vcs_rep', '')
        auto = self.request.data.get('auto', '')
        type = self.request.data.get('type', '')
        if len(App.objects.filter(id=app_id)) <= 0:
            raise APIValidateException(u'应用不存在')
        if not name:
            raise APIValidateException(u'服务名称不能为空')
        if len(AppService.objects.filter(app_id=app_id, name=name)) > 0:
            raise APIValidateException(u'该应用下存在相同名称的服务')
        if auto == 'on' and not vcsRep:
            raise APIValidateException(u'vcsRep(Git仓库)不能为空')
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)
        normalType = None
        if type in ('java', 'tomcat', 'dubbo'):
            normalType = 'java'
        elif type == 'static':
            normalType = 'webresource'
        elif type == 'php':
            normalType = 'php'
        elif type == 'nodejs':
            normalType = 'nodejs'
        elif type == 'python':
            normalType = 'python'

        if auto == "on":
            apps = App.objects.filter(id=obj.app_id)
            if len(apps) > 0:
                AutoApi().addTemplate(obj.name, apps[0].name, obj.name, obj.id, vcsRep, normalType)

        # 添加负责人信息
        principals_list = self.request.data.getlist('user_name[]',[])
        for principal in principals_list:
            ServicePrincipals.objects.create(service_id=obj.id,user_name=principal)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        state_dict = {}
        for s in AppService.STATE:
            state_dict[s[0]] = s[1]
        results = []
        app_ids = []
        for h in serializer.data:
            app_ids.append(h['app_id'])
        app_dict = {}
        for app in App.objects.filter(id__in=app_ids):
            app_dict[app.id] = app
        serviceids = []
        for h in serializer.data:
            serviceids.append(h['id'])
        service_host_dict = defaultdict(list)
        for s in ServiceHost.objects.filter(service_id__in=serviceids):
            service_host_dict[s.service_id].append(s.host_id)
        lb_id_list = []
        service_hostname_dict = defaultdict(list)
        for ss in ServiceLB.objects.filter(service_id__in=serviceids):
            lb_id_list.append(ss.lb_id)
            lb_hostname = []
            for lb in LB.objects.filter(id__in=lb_id_list):
                server_name = lb.server_name
                lb_hostname.extend(server_name.split(' '))
            service_hostname_dict[ss.service_id].extend(lb_hostname)

        for h in serializer.data:
            t = h
            t['state_name'] = state_dict.get(t['state'], t['state'])
            t['app_name'] = ''
            if app_dict.has_key(h['app_id']):
                t['app_name'] = app_dict[h['app_id']].name
            t['hostcount'] = 0
            if service_host_dict.has_key(h['id']):
                t['hostcount'] = len(service_host_dict.get(h['id']))
            if service_hostname_dict.has_key(h['id']):
                t['hostname'] = service_hostname_dict[h['id']]

            t['principals'] = []       # 前端传递的数据加上负责人字段
            for principal in ServicePrincipals.objects.filter(service_id=t['id']):
                t['principals'].append(principal.user_name)
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(ServiceHost.objects.filter(service_id__in=id_list)) > 0:
            raise APIValidateException(u'服务下还有设备,不能删除')
        for id in id_list:
            if id in (configs.FREE_ALIYUN_ID, configs.FREE_VM_ID, configs.FREE_SERVER_ID, configs.FREE_UNUSE):
                raise APIValidateException(u'服务属于资源池,不能删除')
        services = AppService.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in services:
            self.changeLog(a.id, a.name, 'delete service: ' + a.name, uid=uid)
        services.delete()
        #批量删除 auth_service_principal 表中的数据
        service_principals = ServicePrincipals.objects.filter(service_id__in=id_list)
        service_principals.delete()

        return Response({"success": True, "msg": "succ!", "errors": []})

class AppServiceDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    服务详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● app_id                    ——   资产线id(必输)
    ● name                      ——   名称(必输)
    ● type                      ——   服务类型
    ● comment                   ——   备注
    ● vcs_rep                   ——   版本库地址
    """

    paginate_by = None
    queryset = AppService.objects.all()
    serializer_class = AppServiceSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if id in (configs.FREE_ALIYUN_ID, configs.FREE_VM_ID, configs.FREE_SERVER_ID, configs.FREE_UNUSE):
            raise APIValidateException(u'服务 ' + instance.name + u' 属于资源池,不能删除')
        if len(ServiceHost.objects.filter(service_id=id)) > 0:
            raise APIValidateException(u'服务 ' + instance.name + u' 下还有设备,不能删除')
        instance.delete()
        # 删除auth_service_principals表中的数据
        service_principals = ServicePrincipals.objects.filter(service_id=id)
        service_principals.delete()

        self.changeLog(instance.id, instance.name, 'delete business line: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):
        vcsRep = self.request.data.get('vcs_rep', None)
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)
        apps = App.objects.filter(id=obj.app_id)
        if len(apps) > 0:
            AutoApi().updateTemplate(obj.name, apps[0].name, obj.name, obj.id, vcsRep)

        principals_list = self.request.data.getlist('user_name[]')
        service_principals = ServicePrincipals.objects.filter(service_id=obj.id)     # 删除旧数据
        service_principals.delete()
        for principal in principals_list:
            ServicePrincipals.objects.create(service_id=obj.id,user_name=principal)  # 添加新的数据

class ServiceScaleOutByIp(CmdbListCreateAPIView):
    """
    服务扩容——指定ip.

    输入参数：
    ● service_id                   ——   服务id(必输)
    ● ip                           ——   ip(必输)
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
        data = {'success': True, 'msg': u'服务扩容成功'}
        ip = request.data.get("ip", '')
        service_id = request.data.get("service_id", 0)

        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ip_list = []
        for _ip in reip.findall(ip):
            ip_list.append(_ip)
        if len(ip_list) <= 0:
            raise APIValidateException(u'请传入合法ip')
        app = AppService.objects.filter(id=service_id)
        if len(app) <= 0:
            raise APIValidateException(u'id为' + str(service_id) + u"的服务不存在")

        # if len(Hosts.objects.filter(ip__in=ip_list).exclude(state='free')) > 0:
        #     raise APIValidateException(u'只能扩容free状态的主机')
        resource_pool_list = (configs.FREE_ALIYUN_ID, configs.FREE_VM_ID, configs.FREE_SERVER_ID, configs.FREE_UNUSE)
        if service_id in resource_pool_list:
            raise APIValidateException(u'资源池不能扩容')
        uid = str(uuid.uuid1())
        hosts = Hosts.objects.filter(ip__in=ip_list).exclude(state='deleted')
        hostids = []
        for h in hosts:
            hostids.append(h.id)
            self.changeLog(h.id, h.ip, 'change service_id from ' + str(h.service_id) + ' to ' + str(service_id), uid=uid, action='update')
        # 将free状态的机器改为offline(从资源池拿出来的机器)
        hosts.filter(state='free').update(state='offline')
        hosts.update(service_id=service_id)
        # 分配出去的机器从资源池删除
        ServiceHost.objects.filter(host_id__in=hostids, service_id__in=resource_pool_list).delete()
        for h in hosts:
            if len(ServiceHost.objects.filter(service_id=service_id, host_id=h.id)) > 0:
                continue
            ServiceHost.objects.create(service_id=service_id, host_id=h.id)

            ############################### 更改主机名 ###############################
            try:
                autoHostName(request.user.username, h.id)
            except Exception, ex:
                pass
            ############################### 更改主机名 ###############################

        return Response(data)

class ServiceAutoScaleOut(CmdbListCreateAPIView):
    """
    服务自动扩容.

    输入参数：
    ● service_id                   ——   服务id(必输)
    ● env                          ——   环境(必输)
    ● type                         ——   设备类型(必输)
    ● attribute                    ——   属性
    ● img_id                       ——   操作系统id
    ● conf_id                      ——   配置id
    ● segment                      ——   网段
    ● count                        ——   数量(必输)
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
        data = {'success': True, 'msg': u'服务扩容成功'}
        service_id = request.data.get("service_id", 0)
        type = request.data.get("type", '')
        env = request.data.get("env", '')
        attribute = request.data.get("attribute", '')
        img_id = request.data.get("img_id", 0)
        conf_id = request.data.get("conf_id", 0)
        segment = request.data.get("segment", None)
        count = request.data.get("count", 0)

        img_name = request.data.get("img_name", '')
        conf_name = request.data.get("conf_name", '')


        types = []
        for t in Hosts.HOST_TYPE_CHOICES:
            types.append(t[0])
        attributes = []
        for a in Hosts.HOST_ATTRIBUTE_CHOCIES:
            attributes.append(a[0])
        envs = []
        for e in Hosts.HOST_ENV_CHOICES:
            envs.append(e[0])

        if type not in types:
            raise APIValidateException(u'type必须为 ' + " ".join(types) + u' 中的一个')
        if env not in envs:
            raise APIValidateException(u'env必须为 ' + " ".join(envs) + u' 中的一个')
        if attribute and attribute not in attributes:
            raise APIValidateException(u'attribute必须为 ' + " ".join(attribute) + u' 中的一个')
        if img_id and len(Image.objects.filter(id=img_id)) <= 0:
            raise APIValidateException(u'镜像不存在')
        if conf_id and len(Conf.objects.filter(id=conf_id)) <= 0:
            raise APIValidateException(u'配置不存在')
        if not str(count).isdigit() or int(count) < 1 or int(count) > 20:
            raise APIValidateException(u'count必须为1到20的正整数')
        if not img_id and img_name:
            image = Image.objects.filter(name=img_name)
            if len(image) <= 0:
                raise APIValidateException(u'镜像不存在')
            img_id = image[0].id
        if not conf_id and conf_name:
            conf = Conf.objects.filter(name=conf_name)
            if len(conf) <= 0:
                raise APIValidateException(u'配置不存在')
            conf_id = conf[0].id

        count = int(count)
        if service_id in (configs.FREE_ALIYUN_ID, configs.FREE_VM_ID, configs.FREE_SERVER_ID):
            raise APIValidateException(u'资源池不能自动扩容')
        if len(AppService.objects.filter(id=service_id)) <= 0:
            raise APIValidateException(u'服务不存在')
        resource_service_id = 0
        if type == 'server':
            resource_service_id = configs.FREE_SERVER_ID
        elif type == 'vm':
            resource_service_id = configs.FREE_VM_ID
        elif type == 'aliyun':
            resource_service_id = configs.FREE_ALIYUN_ID
        hostids = []
        for s in ServiceHost.objects.filter(service_id=resource_service_id):
            hostids.append(s.host_id)
        hosts = Hosts.objects.filter(type=type, env=env, state='free', id__in=hostids)
        if attribute:
            hosts = hosts.filter(attribute=attribute)
        if img_id:
            hosts = hosts.filter(img_id=img_id)
        if conf_id:
            hosts = hosts.filter(conf_id=conf_id)
        if segment:
            maskint = get_maskint_by_segment(segment)
            if not maskint:
                raise APIValidateException(u'网段不合法')
            mask = exchange_maskint(maskint)
        host_list = []
        for h in hosts:
            if segment:
                host_segment = get_segment_by_ip_mask(h.ip, mask)
                if host_segment != segment:
                    continue
            host_list.append(h)
        if len(host_list) < count:
            raise APIValidateException(u'机器不足无法扩容')
        random.shuffle(host_list)
        hostid_list = []
        for host in host_list[0:count]:
            hostid_list.append(host.id)

        # 删除资源池中的对应机器
        ServiceHost.objects.filter(service_id=resource_service_id, host_id__in=hostid_list).delete()

        uid = str(uuid.uuid1())
        hosts = Hosts.objects.filter(id__in=hostid_list)
        for h in hosts:
            self.changeLog(h.id, h.ip, 'add free host to ' + str(service_id), uid=uid, action='create')
            ServiceHost.objects.create(host_id=h.id, service_id=service_id)
            ############################### 更改主机名 ###############################
            try:
                autoHostName(request.user.username, h.id)
            except Exception, ex:
                pass
            ############################### 更改主机名 ###############################
        hosts.update(service_id=service_id, state='offline')
        return Response(data)

class ServiceGroupList(CmdbListCreateAPIView):
    """
    服务组列表.

    输出参数：
    ● name                      ——   服务组名称

    """

    paginate_by = None
    queryset = AppService.objects.all()

    filter_fields = ()
    search_fields = ()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = AppServiceSerializer

    def list(self, request, *args, **kwargs):
        results = []
        name_list = []
        for a in AppService.objects.all().exclude(id__in=(configs.FREE_UNUSE, configs.FREE_ALIYUN_ID, configs.FREE_SERVER_ID, configs.FREE_VM_ID)):
            name_list.append(a.name.split("_")[0])
        for n in list(set(name_list)):
            results.append({"name": n})
        return Response(results)

class ServiceReduceByIp(CmdbListCreateAPIView):
    """
    服务缩容——指定ip.

    输入参数：
    ● service_id                   ——   服务id(必输)
    ● ip                           ——   ip,多个ip用特殊符号隔开(必输)
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
        return ['DELETE', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        data = {'success': True, 'msg': u'服务缩容成功'}
        ip = request.data.get("ip", '')
        service_id = request.data.get("service_id", 0)

        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ip_list = []
        for _ip in reip.findall(ip):
            ip_list.append(_ip)
        if len(ip_list) <= 0:
            raise APIValidateException(u'请传入合法ip')
        service = AppService.objects.filter(id=service_id)
        if len(service) <= 0:
            raise APIValidateException(u'id为' + str(service_id) + u"的服务不存在")

        # if len(Hosts.objects.filter(ip__in=ip_list).exclude(state='free')) > 0:
        #     raise APIValidateException(u'只能扩容free状态的主机')
        resource_pool_list = (configs.FREE_ALIYUN_ID, configs.FREE_VM_ID, configs.FREE_SERVER_ID, configs.FREE_UNUSE)
        if service_id in resource_pool_list:
            raise APIValidateException(u'资源池不能缩容')
        uid = str(uuid.uuid1())
        hosts = Hosts.objects.filter(ip__in=ip_list).exclude(state='deleted')
        hostids = []
        for h in hosts:
            hostids.append(h.id)
            self.changeLog(h.id, h.ip, 'reduce from service_id ' + str(h.service_id), uid=uid, action='update')
        for h in hosts:
            ServiceHost.objects.filter(service_id=service_id, host_id=h.id).delete()
            # 如果机器不属于任何服务则放入资源池中
            if len(ServiceHost.objects.filter(host_id=h.id)) <= 0:
                sid = configs.FREE_ALIYUN_ID
                if h.type == 'server':
                    sid = configs.FREE_SERVER_ID
                elif h.type == 'vm':
                    sid = configs.FREE_VM_ID
                ServiceHost.objects.create(service_id=sid, host_id=h.id)
                Hosts.objects.filter(id=h.id).update(state='free')

            ############################### 更改主机名 ###############################
            try:
                autoHostName(request.user.username, h.id)
            except Exception, ex:
                pass
            ############################### 更改主机名 ###############################
        return Response(data)

class AppPrincipalsList(CmdbListCreateAPIView):

    queryset = AppPrincipals.objects.all()   # 查出所有 menu 的值

    search_fields = ('user_name')   # 模糊查询的字段
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = AppPrincipalsSerializer  # 业务线的序列化

    @transaction.atomic()          # 发生异常则回滚，保证操作的一致性和完整性
    def perform_create(self, serializer):     # 增添
        obj = serializer.save()

        obj_dict = model_to_dict(obj)                   # 写日志
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.user_name, json_obj)

    #批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):  # args 相当是一个集合，kwargs 相当是一个字典
        id_list = request.data.getlist('id[]', [])  # 获取 id 列表
        id = request.data.get('id', '')  # 获取 id

        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')

        app_principals = AppPrincipals.objects.filter(id__in=id_list)  # 过滤出 id 在 id_list 的 object
        uid = str(uuid.uuid1())  # 生成唯一的 id

        for a in app_principals:
            self.changeLog(a.id, a.app_id, 'delete menu: ' + a.user_name, uid=uid)

        app_principals.delete()  # 删除相应的 menus
        return Response({"success": True, "msg": "succ!", "errors": []})  # 该函数返回 Response 对象

    def get_queryset(self):
        queryset = AppPrincipals.objects.all().order_by("-id")
        return queryset

class AppPrincipalsDetail(CmdbRetrieveUpdateDestroyAPIView):

    queryset = AppPrincipals.objects.all()            # 查询所有数据
    serializer_class = AppPrincipalsSerializer        # 序列菜单对象

    @transaction.atomic()                    # 菜单的删除操作
    def perform_destroy(self, instance):

        id = instance.id
        instance.delete()                    # 执行删除操作
        self.changeLog(id, instance.app_id, 'delete app_principals' + instance.user_name)

    @transaction.atomic()                              # 菜单的更新操作
    def perform_update(self, serializer):

        id = self.kwargs.get('pk', '')                 # 获取id ，默认值为 ''
        menu = AppPrincipals.objects.filter(id=id)              # 过滤出相应 id 的菜单名
        if len(menu) <= 0:                             # 没有相应菜单名
            raise APIValidateException(u'没有相应的信息')    # 抛异常

        obj = serializer.save()               # 更新数据

        obj_dict = model_to_dict(obj)                  # 写日志
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.app_id, obj.user_name, json_obj)

#应用资源使用统计
class AppsStatistics(CmdbListCreateAPIView):
    """
       提供应用下资源的使用情况.
       输入参数：
        ● id                        ——   应用id

       输出参数:
        ● app_hosts_counts          ——   应用下面服务器数量
        ● physic_counts             ——   物理机数量
        ● virtual_counts            ——   虚拟机数量
        ● slb_counts                ——   slb数量
        ● ecs_counts                ——   ecs数量
        ● x                         ——   服务类型列表
        ● y                         ——   类型对应的服务器数量列表


    """
    @transaction.atomic()
    def get(self, request, *args, **kwargs):
        # 获取 id
        id = self.kwargs.get('pk', '')

        all_services = []
        all_app_service = AppService.objects.all()
        all_services_type = all_app_service.values_list('type')
        for service_type in all_services_type:
            all_services.append(service_type[0])
        all_services = list(set(all_services))  # 取出所有的服务类型
        services_count_map = {}
        for service in all_services:
            services_count_map[service] = 0  # 服务类型数量统计初始化

        appservices = AppService.objects.filter(app_id=id)
        server_ids = appservices.values_list('id')  # 获取应用下所有的服务 id
        server_id_list = []
        for server_id in server_ids:
            server_id_list.append(server_id[0])

        # 取出应用下所有的服务分类
        server_types = appservices.values_list('type')
        server_type_list = []
        for server_type in server_types:
            server_type_list.append(server_type[0])
        server_type_list = list(set(server_type_list))

        # 获取应用下服务类型--服务id对应关系       idlist {"nginx":[1,2,3],"redis",[4,5,6]}
        server_type_id_map = {}
        for server_type in server_type_list:
            mylist = []
            server_ids = appservices.filter(type=server_type).values_list("id")
            for server_id in server_ids:
                mylist.append(server_id[0])
            server_type_id_map[server_type] = mylist

        # 统计不同服务类型的服务器数量
        for server_type in server_type_list:
            servicehosts = ServiceHost.objects.filter(service_id__in=server_type_id_map[server_type])
            mylist = []  # 这样写的目的是去重
            for servicehost in servicehosts:
                mylist.append(servicehost.host_id)
            services_count_map[server_type] = len(list(set(mylist)))

        app_hosts = ServiceHost.objects.filter(service_id__in=server_id_list)  # 获取所有 app 对应的 host id（可能重复）
        host_ids = app_hosts.values_list('host_id')
        host_id_list = []
        for host_id in host_ids:
            host_id_list.append(host_id[0])
        hosts = Hosts.objects.filter(id__in=host_id_list)  # 获取 app 对应的 host

        app_hosts_counts = hosts.count()  # 应用使用的服务器数量
        physic_counts = hosts.filter(type='server').count()  # 物理机数量
        virtual_counts = hosts.filter(type='vm').count()  # 虚拟机数量
        ecs_counts = hosts.filter(attribute='ECS').count()  # ecs数量
        slb_counts = hosts.filter(attribute='SLB').count()  # slb数量

        Body = {}
        Body['app_hosts_counts'] = app_hosts_counts
        Body['physic_counts'] = physic_counts
        Body['virtual_counts'] = virtual_counts
        Body['ecs_counts'] = ecs_counts
        Body['slb_counts'] = slb_counts
        Body['x'] = services_count_map.keys()
        Body['y'] = services_count_map.values()

        return Response(Body)


# 服务-ips api
# class ServiceHostIpsApi(CmdbListCreateAPIView):
#     """
#        提供服务名以及该服务对应的服务器 ip 列表.
#         输出参数:
#         ● msg                ——   响应信息
#         ● result             ——   相应结果（{服务1：[ip1,ip2,...]},...）
#         ● success            ——   是否成功
#     """
#     @transaction.atomic()
#     def get(self, request, *args, **kwargs):
#         data = {'success': False, 'msg': 'fail!'}
#         if request.method == 'GET':
#             result = {}
#             # 获取服务id列表
#             service_id_list = []
#             service_host_list = ServiceHost.objects.all()
#             for service_host in service_host_list:
#                 service_id_list.append(service_host.service_id)
#             service_id_list = list(set(service_id_list))
#
#             # 获取服务名称：[hostip] 对应关系
#             for service_id in service_id_list:
#                 app_services = AppService.objects.filter(id=service_id)
#                 if len(app_services):
#                     key = app_services[0].name
#                 else:
#                     continue
#                 service_hosts = ServiceHost.objects.filter(service_id=service_id)
#                 host_ip_list = []
#                 for service_host in service_hosts:
#                     hosts = Hosts.objects.filter(id=service_host.host_id).filter()
#                     if len(hosts) and hosts[0].env == "prod":
#                         host_ip_list.append(hosts[0].ip)
#
#                 result[key] = host_ip_list
#
#             data['result'] = result
#             data['success'] = True
#             data['msg'] = 'succ!'
#         else:
#             data['msg'] = 'request method must be GET'
#         return HttpResponse(json.dumps(data), content_type='application/json')

# class ServiceInformationSaveApi(CmdbListCreateAPIView):       # 服务资源使用统计 from Zabbix
#     """
#        从Zabbix中获取的资源数据保存到数据库.
#         输入参数：
#         ● id                        ——   ID(不用输入)
#         ● service                   ——   服务名称(必输)
#         ● key                       ——   监控的属性名
#         ● max                       ——   最大值
#         ● min                       ——   最小值
#         ● avg                       ——   平均值
#         ● ctime                     ——   时间戳
#     """
#     serializer_class = ServiceResourceSerializer
#     @transaction.atomic()
#     def perform_create(self, serializer):
#         ctime = int(time.time())
#         service_resource = self.request.data.get('data', '')
#         for service, resource in service_resource.items():
#             for key, value in resource.items():
#                 if value:
#                     ServiceResource.objects.create(service=service, key=key, max=value[0], min=value[1], avg=value[2], ctime=ctime)

class ServiceInformationShowApi(CmdbListCreateAPIView):
    """
        向前端提供来自 Zabbix 中的服务资源使用信息.
        输入参数：
        ● id                      ——   服务id

       输出参数:
        ● cpu_usage_rate          ——   cpu 使用率
        ● cpu_load                ——   cpu 负载
        ● memory                  ——   内存
        ● net_in                  ——   流量（入）
        ● net_out                 ——   流量（出）
    """
    serializer_class = ServiceResourceSerializer
    @transaction.atomic()
    def get(self, request, *args, **kwargs):
        # 获取 id
        id = self.kwargs.get('pk', '')
        service = AppService.objects.get(id=id)
        sources = ServiceResource.objects.filter(service=service.name)
        # 取进一周的数据
        year_sources = []
        # 取当前日期凌晨的时间戳
        cur_time = int(time.time())
        today_start_time = cur_time - (cur_time + 28800) % 86400   # 28800 = 86400/3  原因是时间戳的启始时间是 1970.1.1,08.00.00 北京时间
        for i in range(1, 365):     # 控制取多少天的数据
            time_from = today_start_time - i*86400
            time_till = time_from + 86400
            oneday_sources = sources.filter(ctime__gte=time_from).filter(ctime__lt=time_till)

            if len(oneday_sources):
                year_sources.append(oneday_sources)
            else:
                break
        year_sources.reverse()      # 使日期从大到小

        data = {}
        data['cpu_usage_rate'] = {"max":[],"min":[],"avg":[]}
        data['cpu_load'] = {"max":[],"min":[],"avg":[]}
        data['memory'] = {"max":[],"min":[],"avg":[]}
        data['net_in'] = {"max":[],"min":[],"avg":[]}
        data['net_out'] = {"max":[],"min":[],"avg":[]}

        for day_source in year_sources:     # 遍历每一天的数据
            for source in day_source:       # 遍历每一天中的每一个 key
                if source.avg:              # 如果有数据则添加到表中,否则跳过(没有数据则不显示而不是显示 0)
                    data[source.key]['max'].append({"value": [source.ctime*1000, source.max]})      # 到 echart 的时间戳格式不一样，要乘以 1000
                    data[source.key]['min'].append({"value": [source.ctime*1000, source.min]})
                    data[source.key]['avg'].append({"value": [source.ctime*1000, source.avg]})

        return Response(data)
