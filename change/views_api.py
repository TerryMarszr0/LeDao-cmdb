# -*- coding: utf-8 -*-
import time, json

from change.models import Change
from change.serializers import ChangeSerializer
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from public.base_exception import APIValidateException

class ChangeList(generics.ListAPIView):
    """
    变更记录列表.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● username                  ——   操作人
    ● resource                  ——   变更资源类型
    ● res_id                    ——   变更资源id
    ● index                     ——   变更记录索引
    ● action                    ——   变更类型(create, update, delete)
    ● start_time                ——   起始时间(大于等于起始时间)
    ● end_time                  ——   结束时间(小于结束时间)
    ● search                    ——   搜索(message, index)

    输出参数：
    ● id                        ——   PK
    ● uuid                      ——   变更任务id
    ● username                  ——   操作人
    ● resource                  ——   变更资源类型
    ● res_id                    ——   变更资源id
    ● index                     ——   变更记录索引
    ● action                    ——   变更类型(create, update, delete)
    ● message                   ——   变更内容
    ● change_time               ——   变更时间
    ● ctime                     ——   创建时间
    """
    paginate_by = None
    queryset = Change.objects.all()
    filter_fields = ('username', 'resource', 'res_id', 'index', 'action')
    search_fields = ('message', 'index')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ChangeSerializer

    def get_queryset(self):
        queryset = Change.objects.all().order_by('-change_time')
        id = self.request.query_params.get('id', None)
        end_time = self.request.query_params.get('end_time', None)
        start_time = self.request.query_params.get('start_time', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)

        if end_time:
            try:
                etime_struct = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                end_time = int(time.mktime(etime_struct))
                queryset = queryset.filter(change_time__lt=end_time)
            except:
                raise APIValidateException(u'时间格式必须为:Y-m-d H:M:S')

        if start_time:
            try:
                stime_struct = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                start_time = int(time.mktime(stime_struct))
                queryset = queryset.filter(change_time__gte=start_time)
            except:
                raise APIValidateException(u'时间格式必须为:Y-m-d H:M:S')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        results = []
        for h in serializer.data:
            t = h
            t['change_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t['change_time']))
            t['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t['ctime']))
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

class ChangeDetail(generics.RetrieveAPIView):
    """
    变更记录详情页

    输出参数：
    ● id                        ——   PK
    ● uuid                      ——   变更任务id
    ● username                  ——   操作人
    ● resource                  ——   变更资源类型
    ● res_id                    ——   变更资源id
    ● index                     ——   变更记录索引
    ● action                    ——   变更类型(create, update, delete)
    ● message                   ——   变更内容
    ● change_time               ——   变更时间
    ● ctime                     ——   创建时间
    """
    paginate_by = None
    queryset = Change.objects.all()
    serializer_class = ChangeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(serializer.data['ctime']))
        data['change_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(serializer.data['change_time']))
        return Response(data)

