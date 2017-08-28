# -*- coding: utf-8 -*-
import time, json, uuid
from rest_framework import filters
from asset.models import Room, Rack, AssetModel, Conf, Network, IpAddress, RackU
from asset.serializers import RoomSerializer, RackSerializer, AssetModelSerializer, ConfSerializer, NetworkSerializer, IpAddressSerializer
from rest_framework.response import Response
from public.base_exception import APIValidateException
from host.models import Hosts
from django.db import transaction
from django.forms.models import model_to_dict
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView
from IPy import IP
from rest_framework import status
from public.common.tools import check_ip


class RoomList(CmdbListCreateAPIView):
    """
    机房列表/创建机房.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● name                      ——   机房名称
    ● state                     ——   状态(online、offline)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   机房名称(必输)
    ● cn_name                   ——   中文名称(必输)
    ● region_id                 ——   区域编号
    ● tag                       ——   标签
    ● location                  ——   机房位置
    ● state                     ——   状态(online、offline)(必输)
    ● comment                   ——   机房描述
    ● ctime                     ——   创建时间

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = Room.objects.all()
    filter_fields = ('name', 'state')
    search_fields = ('name', 'cn_name', 'location')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all().order_by("-id")
        id = self.request.query_params.get('id', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    @transaction.atomic()
    def perform_create(self, serializer):
        current_time = int(time.time())
        obj = serializer.save(ctime=current_time)
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(Hosts.objects.filter(room_id__in=id_list)) > 0 or len(Rack.objects.filter(room_id__in=id_list)) > 0:
            raise APIValidateException('room already in use can not delete')
        rooms = Room.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in rooms:
            self.changeLog(a.id, a.name, 'delete room: ' + a.name, uid=uid)
        rooms.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})


class RoomDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    机房详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   机房名称(必输)
    ● cn_name                   ——   中文名称(必输)
    ● region_id                 ——   区域编号
    ● tag                       ——   标签
    ● location                  ——   机房位置
    ● state                     ——   状态(online、offline)(必输)
    ● comment                   ——   机房描述
    ● ctime                     ——   创建时间
    """
    paginate_by = None
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if len(Hosts.objects.filter(room_id=id)) > 0 or len(Rack.objects.filter(room_id=id)) > 0:
            raise APIValidateException('room ' + instance.name + ' already in use can not delete')
        instance.delete()
        self.changeLog(id, instance.name, 'delete room: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)


class RackList(CmdbListCreateAPIView):
    """
    机柜列表/创建机柜.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● name                      ——   机房名称
    ● state                     ——   状态(online、offline)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   机柜名称(必输)
    ● height                    ——   U数(必输)
    ● type                      ——   机柜类型(0-刀片笼子、1-机柜)(必输)
    ● room_id                   ——   机房(必输)
    ● state                     ——   状态(online、offline)(必输)
    ● comment                   ——   机柜描述
    ● ctime                     ——   创建时间(无需输入)
    """
    paginate_by = None
    queryset = Rack.objects.all()

    filter_fields = ('name', 'state')
    search_fields = ('name', 'comment')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = RackSerializer

    def get_queryset(self):
        queryset = Rack.objects.all()
        id = self.request.query_params.get('id', None)

        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    @transaction.atomic()
    def perform_create(self, serializer):
        current_time = int(time.time())
        obj = serializer.save(ctime=current_time)
        for i in range(1, obj.height + 1):
            RackU.objects.create(rack_id=obj.id, uid=i, host_id=0)
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        room_dict = {}
        for r in Room.objects.all():
            room_dict[r.id] = r.name
        type_dict = {}
        for t in Rack.TYPE:
            type_dict[t[0]] = t[1]
        results = []
        for d in serializer.data:
            t = d
            t['room_name'] = room_dict.get(t['room_id'], '')
            t['type_name'] = type_dict.get(t['type'], '')
            results.append(t)

        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)


class RackDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    机柜详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   机柜名称(必输)
    ● height                    ——   U数(必输)
    ● type                      ——   机柜类型(0-刀片笼子、1-机柜)(必输)
    ● room_id                   ——   机房(必输)
    ● state                     ——   状态(online、offline)(必输)
    ● comment                   ——   机柜描述
    ● ctime                     ——   创建时间(无需输入)
    """
    paginate_by = None
    queryset = Rack.objects.all()
    serializer_class = RackSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        RackU.objects.filter(rack_id=instance.id).delete()
        instance.delete()
        self.changeLog(id, instance.name, 'delete rack: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):
        obj = serializer.save()
        u = RackU.objects.filter(rack_id=obj.id)
        if len(u) < obj.height:
            for i in range(len(u) + 1, obj.height + 1):
                RackU.objects.create(rack_id=obj.id, uid=i, host_id=0)
        if len(u) > obj.height:
            RackU.objects.filter(uid__gt=obj.height).delete()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)

class ModelList(CmdbListCreateAPIView):
    """
    设备型号列表/创建设备型号.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● search                    ——   机房名称(型号/厂商/备注)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   名称(必输)
    ● size                      ——   尺寸(必输)
    ● firm_name                 ——   厂商(必输)
    ● comment                   ——   备注
    ● ctime                     ——   创建时间(无需输入)

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = AssetModel.objects.all()

    search_fields = ('name', 'firm_name', 'comment')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = AssetModelSerializer

    def get_queryset(self):
        queryset = AssetModel.objects.all()
        id = self.request.query_params.get('id', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    @transaction.atomic()
    def perform_create(self, serializer):
        current_time = int(time.time())
        obj = serializer.save(ctime=current_time)
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(Hosts.objects.filter(model_id__in=id_list)) > 0:
            raise APIValidateException('model already in use can not delete')
        assetmodels = AssetModel.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in assetmodels:
            self.changeLog(a.id, a.name, 'delete model: ' + a.name, uid=uid)
        assetmodels.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})


class ModelDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    设备型号详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   名称(必输)
    ● size                      ——   尺寸(必输)
    ● firm_name                 ——   厂商(必输)
    ● comment                   ——   备注
    ● ctime                     ——   创建时间(无需输入)

    批量删除:
    ● id[]                      ——   id列表
    """
    paginate_by = None
    queryset = AssetModel.objects.all()
    serializer_class = AssetModelSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if len(Hosts.objects.filter(model_id=id)):
            raise APIValidateException('model ' + instance.name + ' already in use can not delete')
        instance.delete()
        self.changeLog(id, instance.name, 'delete model: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)

class ConfList(CmdbListCreateAPIView):
    """
    设备配置列表/创建设备配置.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● search                    ——   机房名称(型号/厂商/备注)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   名称(必输)
    ● cpu                       ——   cpu
    ● disk                      ——   磁盘
    ● memory                    ——   内存
    ● raid                      ——   内存
    ● comment                   ——   备注
    ● ctime                     ——   创建时间(无需输入)

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = Conf.objects.all()

    search_fields = ('name', 'cpu', 'disk', 'memory', 'raid', 'comment')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = ConfSerializer

    def get_queryset(self):
        queryset = Conf.objects.all().order_by("-id")
        id = self.request.query_params.get('id', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    @transaction.atomic()
    def perform_create(self, serializer):
        current_time = int(time.time())
        obj = serializer.save(ctime=current_time)
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(Hosts.objects.filter(conf_id__in=id_list)) > 0:
            raise APIValidateException('model already in use can not delete')
        confs = Conf.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in confs:
            self.changeLog(a.id, a.name, 'delete conf: ' + a.name, uid=uid)
        confs.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})


class ConfDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    设备配置详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● name                      ——   名称(必输)
    ● cpu                       ——   cpu
    ● disk                      ——   磁盘
    ● memory                    ——   内存
    ● raid                      ——   内存
    ● comment                   ——   备注
    ● ctime                     ——   创建时间(无需输入)
    """
    paginate_by = None
    queryset = Conf.objects.all()
    serializer_class = ConfSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if len(Hosts.objects.filter(model_id=id)):
            raise APIValidateException('conf ' + instance.name + ' already in use can not delete')
        instance.delete()
        self.changeLog(instance.id, instance.name, 'delete conf: ' + instance.name)

    @transaction.atomic()
    def perform_update(self, serializer):
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.name, json_obj)


class NetworkList(CmdbListCreateAPIView):
    """
    网段列表/创建网段.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● room_id                   ——   机房id
    ● env                       ——   环境
    ● search                    ——   模糊查询(网络/网关/掩码)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● room_id                   ——   机房id(必输)
    ● room_name                 ——   机房名称
    ● room_cname                ——   机房中文名称
    ● env                       ——   环境
    ● network                   ——   网络
    ● mask                      ——   掩码
    ● maskint                   ——   掩码位数
    ● gateway                   ——   网关
    ● vlan                      ——   vlan
    ● total                     ——   总数量
    ● free                      ——   可用地址数量
    ● ctime                     ——   创建时间(无需输入)

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = Network.objects.all()

    filter_fields = ('room_id', 'env')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = NetworkSerializer

    def get_queryset(self):
        queryset = Network.objects.all().order_by("-id")
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
        room_dict = {}
        for r in Room.objects.all():
            room_dict[r.id] = r
        for h in serializer.data:
            t = h
            t['room_name'] = ''
            if room_dict.has_key(h['room_id']):
                t['room_name'] = room_dict[h['room_id']].name
            t['room_cname'] = ''
            if room_dict.has_key(h['room_id']):
                t['room_cname'] = room_dict[h['room_id']].cn_name
            t['total'] = IpAddress.objects.filter(network_id=h['id']).count()
            t['free'] = IpAddress.objects.filter(network_id=h['id'], state='free').count()
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    @transaction.atomic()
    def perform_create(self, serializer):
        network = self.request.data.get('network', '')
        maskint = self.request.data.get('maskint', '')
        gateway = self.request.data.get('gateway', '')
        if not check_ip(network):
            raise APIValidateException(u'network不是合法的ip地址')
        if not check_ip(gateway):
            raise APIValidateException(u'gateway不是合法的ip地址')
        if not str(network).endswith(".0"):
            raise APIValidateException(u'network必须以.0结尾')
        if not str(maskint).isdigit() or int(maskint) < 8 or int(maskint) > 32:
            raise APIValidateException(u'maskint必须为8到32之间的整数')
        current_time = int(time.time())
        obj = serializer.save(ctime=current_time)
        json_obj = json.dumps(model_to_dict(obj))
        ip_segment = obj.network + "/" + str(obj.maskint)
        iplist = IP(ip_segment)
        i = 0
        for ip in iplist:
            i += 1
            state = 'free'
            if str(ip).endswith(".0") or i == len(iplist) or str(ip) == str(gateway):
                state = 'reserve'
            IpAddress.objects.create(network_id=obj.id, ip=ip, ctime=current_time, state=state)
        self.changeLog(obj.id, obj.network, json_obj)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(IpAddress.objects.filter(network_id__in=id_list, state='used')) > 0:
            raise APIValidateException(u'网段正在使用,不能删除')
        networks = Network.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in networks:
            self.changeLog(a.id, a.network, 'delete network: ' + a.network, uid=uid)
        networks.delete()
        IpAddress.objects.filter(network_id__in=id_list).delete()
        return Response({"success": True, "msg": "succ!", "errors": []})


class NetworkDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    网段详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● room_id                   ——   机房id(必输)
    ● room_name                 ——   机房名称(无需输入)
    ● room_cname                ——   机房中文名称(无需输入)
    ● env                       ——   环境
    ● network                   ——   网络
    ● mask                      ——   掩码
    ● maskint                   ——   掩码位数
    ● gateway                   ——   网关
    ● vlan                      ——   vlan
    ● ctime                     ——   创建时间(无需输入)
    """
    paginate_by = None
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if len(IpAddress.objects.filter(network_id=id, state='used')):
            raise APIValidateException(u'该网段正在使用,不能删除')
        instance.delete()
        IpAddress.objects.filter(network_id=id).delete()
        self.changeLog(instance.id, instance.network, 'delete network: ' + instance.network)

    def put(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许put操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许patch操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS']


class IpAddressList(CmdbListCreateAPIView):
    """
    ip地址.

    查询参数：
    ● network_id                ——   网段id(必输)
    ● id                        ——   PK(查询多个用逗号隔开)
    ● ip                        ——   ip

    输入/输出参数：
    ● id                        ——   PK
    ● network_id                ——   网段id
    ● ip                        ——   ip
    ● state                     ——   状态(free, used, reserve)
    ● ctime                     ——   创建时间

    """
    paginate_by = None
    queryset = IpAddress.objects.all()

    filter_fields = ('network_id', 'ip')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = IpAddressSerializer

    def get_queryset(self):
        network_id = self.request.query_params.get('network_id', None)
        if not network_id:
            raise APIValidateException(u'network_id不能为空')
        queryset = IpAddress.objects.filter(network_id=network_id)
        id = self.request.query_params.get('id', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']
