# -*- coding: utf-8 -*-
import time, json

from app.models import AppSegment
from rest_framework import filters

from public.serializers import AsyncTaskSerializer, RedirectSerializer
from public.models import AsyncTask
from public.base_exception import APIValidateException
from rest_framework.response import Response
from public.base import CmdbListCreateAPIView
from collections import defaultdict
from rest_framework import status
from public.redis.mq import Q
from django.forms.models import model_to_dict
from cmdb import configs
from host.serializers import HostsSearchSerializer
from host.models import Hosts
from app.models import ServiceHost
from app.models import AppService
from django.db import models
from app.auto.autoapi import GitLabApi
from lb.models import LB, ServiceLB

class TaskList(CmdbListCreateAPIView):
    """
    任务列表.

    查询参数：
    ● state                     ——   状态
    ● search                    ——   搜索(task, params)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● task                      ——   任务
    ● state                     ——   状态
    ● result                    ——   执行结果
    ● ctime                     ——   创建时间
    ● cuser                     ——   创建用户
    ● start_time                ——   执行时间
    ● finish_time               ——   完成时间
    """

    paginate_by = None
    queryset = AsyncTask.objects.all()

    filter_fields = ('state', )
    search_fields = ('task', 'params')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = AsyncTaskSerializer

    def get_queryset(self):
        queryset = AsyncTask.objects.all().order_by("-ctime")
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
        app_ids = []
        for h in serializer.data:
            app_ids.append(h['id'])
        appsegment_dict = defaultdict(list)
        for seg in AppSegment.objects.filter(app_id__in=app_ids):
            appsegment_dict[seg.app_id].append(seg.segment)
        for h in serializer.data:
            t = h
            if t['ctime']:
                t['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t['ctime']))
            if t['start_time']:
                t['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t['start_time']))
            if t['finish_time']:
                t['finish_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t['finish_time']))
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']


class RedoTask(CmdbListCreateAPIView):
    """
    重做任务.

    输入参数：
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """

    paginate_by = None
    queryset = AsyncTask.objects.all()

    filter_fields = ('state', )
    search_fields = ('task', 'params')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = AsyncTaskSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['POST', 'HEAD', 'OPTIONS']

    def post(self, request, *args, **kwargs):
        id = request.data.get("id", '')
        id_list = request.data.getlist("id[]", [])

        if not id and len(id_list) <= 0:
            raise APIValidateException(u'参数id和id[]不能都为空')
        if id:
            id_list += id.split(",")
        tasks = AsyncTask.objects.filter(id__in=id_list)
        tasks.update(state='ready')
        try:
            q = Q(configs.CMDB_TASK)
            for t in tasks:
                q.push(json.dumps(model_to_dict(t)))
        except Exception, ex:
            configs.logger.error(str(ex))
        return Response({'success': True, 'msg': 'succ!'})

class QuickSearchList(CmdbListCreateAPIView):
    """
    快速搜索列表.

    查询参数：
    ● search                    ——   搜索(服务名,ip,主机名)

    输入/输出参数：
    ● service_id                ——   服务id
    ● name                      ——   服务名称或主机ip
    """

    paginate_by = None
    queryset = Hosts.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = HostsSearchSerializer

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        if not search:
            raise APIValidateException(u'字段search不能为空')
        result = []
        lb_ids = []
        for lb in LB.objects.filter(server_name__icontains=search):
           lb_ids.append(lb.id)
        serviceids = []
        for u in ServiceLB.objects.filter(lb_id__in=lb_ids):
            serviceids.append(u.service_id)
        for s in AppService.objects.filter(id__in=serviceids):
            result.append({'service_id': s.id, 'name': s.name, 'ip': '', 'host_id': 0})
        for s in AppService.objects.filter(name__icontains=search):
            if s.id in serviceids:
                continue
            result.append({'service_id': s.id, 'name': s.name, 'ip': '', 'host_id': 0})
        host_ids = []
        hostid_dict = {}
        for h in Hosts.objects.filter(models.Q(ip__startswith=search) | models.Q(hostname__startswith=search)):
            host_ids.append(h.id)
            hostid_dict[h.id] = h
        if len(host_ids) > 0:
            service_dict = {}
            for s in AppService.objects.all():
                service_dict[s.id] = s
            for sh in ServiceHost.objects.filter(host_id__in=host_ids):
                if not service_dict.has_key(sh.service_id):
                    continue
                service_name = service_dict[sh.service_id].name
                result.append({'service_id': sh.service_id, 'name': service_name + " => " + hostid_dict[sh.host_id].ip, 'ip': hostid_dict[sh.host_id].ip, 'host_id': sh.host_id})
        return Response(result)

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

class GitList(CmdbListCreateAPIView):
    """
    Git仓库地址列表.

    查询参数：
    ● state                     ——   状态
    ● search                    ——   搜索(task, params)

    输出参数：
    ● ssh_url_to_repo           ——   SSH地址
    ● web_url                   ——   http地址
    """

    paginate_by = None
    queryset = AsyncTask.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = AsyncTaskSerializer

    def get(self, request, *args, **kwargs):
        page = 1
        limit = 100
        data = []
        while True:
            state, res = GitLabApi().getProjects(page, limit)
            if not state:
                raise APIValidateException(res)
            data += res
            page += 1
            if len(res) < limit:
                break
        return Response(data)



    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']


class Redirect(CmdbListCreateAPIView):
    """
    创建Orange重定向规则.

    Method: POST

    输入参数：
    ● domain                    ——   域名(必须)
    ● path                      ——   路径(必须)

    输出参数:
    ● domain                    ——   域名
    ● path                      ——   路径
    ● ip_list                   ——   禁用ip列表(["1.1.1.1", "2.2.2.2"])
    ● detail                    ——   失败消息

    Http Status Codes:
    ● 200                       ——   OK(查询或修改成功)
    ● 201                       ——   创建成功

    ● 400                       ——   数据校验错误(比如必输参数没传等)
    ● 401                       ——   未认证(用户未登录或者Token校验失败)
    ● 403                       ——   没有权限
    ● 405                       ——   Http Method不允许

    ● 5XX                       ——   服务器端错误
    """


    paginate_by = None
    queryset = AsyncTask.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = RedirectSerializer
    def get(self, request, *args, **kwargs):
        return Response({'domain': 'xxx', 'path': '/xx/', 'ip_list': ['1.1.1.1', '2.2.2.2'], 'detail': u'不允许get操作'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['POST', 'HEAD', 'OPTIONS']

    def post(self, request, *args, **kwargs):
        domain = request.data.get("domain", '')
        path = request.data.get("path", '')
        if not domain:
           raise APIValidateException(u'domain不能为空')
        if not path:
           raise APIValidateException(u'path不能为空')
        ip_list = ['1.1.1.1', '2.2.2.2']
        return Response({'domain': domain, 'path': path, 'ip_list': ip_list})





















