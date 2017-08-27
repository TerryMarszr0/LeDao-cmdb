# -*- coding: utf-8 -*-
import time, uuid, json, re
from rest_framework import filters
from host.models import Hosts
from fortress.serializers import AuthRecordSerializer, ApplyRecordSerializer, ApplyTaskSerializer, SSHKeySerializer
from rest_framework.response import Response
from public.base_exception import APIValidateException
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView
from rest_framework import status
from fortress.models import AuthRecord, ApplyRecord, ApplyTask, SSHKey
from django.db import transaction
from django.forms.models import model_to_dict
from asset.models import Room
from fortress.task.fortresstask import AddUserKeyTask, ApplyTaskAddUserKeyTask, DelUserKeyTask
from django.db.models import Q
from rest_framework import permissions
from fortress.libs.fortresslib import FortressOps, create_ssh_key
from django.http import StreamingHttpResponse
from app.models import ServiceHost, AppService
from collections import defaultdict
from django.core.mail import send_mail
from django.contrib.auth.models import User
from cmdb import settings, configs

def format_authrecord(records):
    results = []
    hostids = []
    for r in records:
        hostids.append(r['host_id'])
    hostid_dict = {}
    for h in Hosts.objects.filter(id__in=hostids):
        hostid_dict[h.id] = h
    roomdict = {}
    for room in Room.objects.all():
        roomdict[room.id] = room
    for r in records:
        t = r
        t['ip'] = ''
        t['hostname'] = ''
        t['env'] = ''
        t['room_name'] = ''
        if hostid_dict.has_key(r['host_id']):
            host = hostid_dict[r['host_id']]
            t['ip'] = host.ip
            t['hostname'] = host.hostname
            t['env'] = host.env
            if roomdict.has_key(host.room_id):
                t['room_name'] = roomdict[host.room_id].name
        t['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t['ctime']))
        t['expiration_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t['expiration_time']))
        results.append(t)
    return results

class UserAuthRecordList(CmdbListCreateAPIView):
    """
    用户授权列表.

    查询参数：
    ● username                  ——   用户名(必输)

    输出参数：
    ● id                        ——   PK
    ● username                  ——   用户名
    ● host_id                   ——   主机id
    ● ip                        ——   ip
    ● role                      ——   权限
    ● cuser                     ——   创建用户
    ● ctime                     ——   创建时间
    ● expiration_time           ——   过期时间
    """
    paginate_by = None
    queryset = AuthRecord.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = AuthRecordSerializer

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    def get_queryset(self):
        queryset = AuthRecord.objects.filter(expiration_time__gt=int(time.time()))
        username = self.request.query_params.get('username', None)
        if not username:
            raise APIValidateException(u'username不能为空')
        queryset = queryset.filter(username=username)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        results = format_authrecord(serializer.data)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

class AuthRecordList(CmdbListCreateAPIView):
    """
    主机授权列表.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● username                  ——   用户名
    ● host_id                   ——   主机id
    ● search                    ——   查询字段(hostname, ip, username)

    输出参数：
    ● id                        ——   PK
    ● username                  ——   用户名
    ● host_id                   ——   主机id
    ● ip                        ——   ip
    ● role                      ——   权限
    ● cuser                     ——   创建用户(不用输入)
    ● ctime                     ——   创建时间(不用输入)
    ● expiration_time           ——   过期时间

    输入参数:
    ● ip[]                      ——   主机ip列表
    ● ip                        ——   主机ip多个ip用除点号之外任意符号隔开
    ● host_id[]                 ——   主机id列表
    ● host_id                   ——   主机id(多个id用逗号隔开)
    ● username[]                ——   用户名列表
    ● username                  ——   用户名(多个用户名用逗号隔开)
    ● day                       ——   授权天数
    ● role                      ——   角色

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = AuthRecord.objects.all()
    filter_fields = ('username', 'host_id')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = AuthRecordSerializer

    def _allowed_methods(self):
        return ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        cuser = request.user.username
        host_ids = request.data.getlist('host_id[]', [])
        host_id = request.data.get('host_id', '')
        ip_list = request.data.getlist('ip[]', [])
        ip = request.data.get('ip', '')
        username_list = request.data.getlist('username[]', [])
        username = request.data.get('username', '')
        role = request.data.get('role', '')
        day = request.data.get('day', '')
        role_list = []
        for r in AuthRecord.ROLE_CHOICES:
            role_list.append(r[0])
        if len(host_ids) <= 0 and not host_id and len(ip_list) <= 0 and not ip:
            raise APIValidateException(u'ip[], ip, host_id[], host_id不能同时为空')
        if len(username_list) <= 0 and not username:
            raise APIValidateException(u'username[]和username不能都为空')
        if not day:
            raise APIValidateException(u'day不能为空')
        if not str(day).isdigit():
            raise APIValidateException(u'day必须为整数')
        if role not in role_list:
            raise APIValidateException(u'role必须为' + " ".join(role_list) + u'中的一个')
        if host_id:
            host_ids += host_id.split(',')
        if ip:
            reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
            for _ip in reip.findall(ip):
                ip_list.append(_ip)
        if len(ip_list) > 0:
            for h in Hosts.objects.filter(ip__in=ip_list):
                host_ids.append(h.id)
        if username:
            username_list += username.split(',')
        username_list = list(set(username_list))
        if len(User.objects.filter(username__in=username_list)) < len(username_list):
            raise APIValidateException(u'用户不存在')
        host_ids = list(set(host_ids))
        hostlist = Hosts.objects.filter(id__in=host_ids)
        if len(hostlist) < len(host_ids):
            raise APIValidateException(u'主机不存在')
        host_dict = {}
        for h in hostlist:
            host_dict[str(h.id)] = h
        current_time = int(time.time())
        uid = str(uuid.uuid1())
        for h in host_ids:
            if not host_dict.has_key(str(h)):
                raise APIValidateException(u'id为' + str(h) + u'的主机不存在')

            for u in username_list:
                AuthRecord.objects.filter(username=u, host_id=h).delete()
                obj = AuthRecord.objects.create(ctime=current_time, expiration_time=int(time.time()) + int(day)*86400, role=role, username=u, cuser=cuser, host_id=h)
                obj_dict = model_to_dict(obj)
                json_obj = json.dumps(obj_dict)

                ########################################## 添加用户授权key任务 ##########################################
                try:
                    AddUserKeyTask().addTask(cuser, ip=host_dict[str(h)].ip, role=role, username=u)
                except Exception, ex:
                    configs.logger.error(str(ex))
                ########################################## 添加用户授权key任务 ##########################################

                self.changeLog(obj.id, obj.username, json_obj, uuid=uid)
        return Response({"success": True, "msg": "succ!"})

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        host = self.request.query_params.get('host', None)
        hosts = Hosts.objects.all()
        queryset = AuthRecord.objects.all().order_by("-id")
        if host:
            hosts = hosts.filter(Q(hostname__startswith=host) | Q(ip__startswith=host))
            hostids = []
            for h in hosts:
                hostids.append(h.id)
            queryset = queryset.filter(host_id__in=hostids)

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
        results = format_authrecord(serializer.data)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        cuser = request.user.username
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        records = AuthRecord.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        hostids = []
        for a in records:
            hostids.append(a.host_id)
        host_dict = {}
        for h in Hosts.objects.filter(id__in=hostids):
            host_dict[h.id] = h
        for a in records:
            ip = ''
            if host_dict.has_key(a.host_id):
                ip = host_dict[a.host_id].ip
            self.changeLog(a.id, str(a.username) , 'delete auth record: ' + a.username + " " + ip + " " + a.role, uid=uid)
            if host_dict.has_key(a.host_id):
                ######################################## 删除用户在机器上的ssh key ########################################
                try:
                    DelUserKeyTask().addTask(cuser, ip=ip, role=a.role, username=a.username)
                except:
                    pass
                ######################################## 删除用户在机器上的ssh key ########################################
        records.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})

class AuthRecordDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    主机详情页

    输出参数：
    ● id                        ——   PK
    ● username                  ——   用户名
    ● host_id                   ——   主机id
    ● role                      ——   权限
    ● cuser                     ——   创建用户(不用输入)
    ● ctime                     ——   创建时间(不用输入)
    ● expiration_time           ——   过期时间
    """
    paginate_by = None
    queryset = AuthRecord.objects.all()
    serializer_class = AuthRecordSerializer

    def _allowed_methods(self):
        return ['DELETE', 'HEAD', 'OPTIONS']

    def put(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许put操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许patch操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    @transaction.atomic()
    def perform_destroy(self, instance):
        cuser = self.request.user.username
        id = instance.id
        instance.delete()
        host = Hosts.objects.filter(id=instance.host_id)
        ip = ''
        if len(host) > 0:
            ip = host[0].ip
            ######################################## 删除用户在机器上的ssh key ########################################
            try:
                DelUserKeyTask().addTask(cuser, ip=ip, role=instance.role, username=instance.username)
            except:
                pass
            ######################################## 删除用户在机器上的ssh key ########################################
        self.changeLog(id, instance.username, 'delete auth record: ' + instance.username + " " + ip + " " + instance.role)


class ApplyRecordList(CmdbListCreateAPIView):
    """
    授权申请列表.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● apply_user                ——   申请人
    ● reviewer                  ——   审核人
    ● state                     ——   状态

    输出参数：
    ● id                        ——   PK
    ● apply_user                ——   申请人
    ● reviewer                  ——   审核人
    ● state                     ——   状态
    ● role                      ——   权限
    ● day                       ——   天数
    ● apply_time                ——   申请时间
    ● reason                    ——   申请原因
    ● audit_time                ——   审批时间
    ● reviewer_reason           ——   审批原因

    输入参数:
    ● role                      ——   权限(必输)
    ● day                       ——   天数(必输)
    ● reason                    ——   申请原因(必输)
    ● ip                        ——   ip列表,多个ip用换行或逗号隔开(选填,与ip[]不能同时为空)
    ● ip[]                      ——   ip列表(选填,与ip不能同时为空)

    """

    permission_classes = (permissions.AllowAny,)

    paginate_by = None
    queryset = ApplyRecord.objects.all()
    filter_fields = ('apply_user', 'reviewer', 'state')
    search_fields = ('reason', )
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ApplyRecordSerializer

    def _allowed_methods(self):
        return ['GET', 'POST', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        cuser = request.user.username
        ip_list = request.data.getlist('ip[]', [])
        ip = request.data.get('ip', '')
        reason = request.data.get('reason', '')
        role = request.data.get('role', '')
        day = request.data.get('day', '')
        role_list = []
        for r in AuthRecord.ROLE_CHOICES:
            role_list.append(r[0])
        if len(ip_list) <= 0 and not ip:
            raise APIValidateException(u'ip[]和ip不能同时为空')
        if not day:
            raise APIValidateException(u'day不能为空')
        if not str(day).isdigit():
            raise APIValidateException(u'day必须为整数')
        if role not in role_list:
            raise APIValidateException(u'role必须为' + " ".join(role_list) + u'中的一个')
        if not reason:
            raise APIValidateException(u'申请原因不能为空')
        if ip:
            reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
            for _ip in reip.findall(ip):
                ip_list.append(_ip)
        ip_list = list(set(ip_list))
        hostlist = Hosts.objects.filter(ip__in=ip_list)
        if len(hostlist) < len(ip_list):
            raise APIValidateException(u'主机不存在')
        host_dict = {}
        for h in hostlist:
            host_dict[str(h.id)] = h
        current_time = int(time.time())
        obj = ApplyRecord.objects.create(apply_user=cuser, reason=reason, apply_time=current_time, role=role, day=day, state='pending')
        uid = str(uuid.uuid1())
        for h in hostlist:
            ApplyTask.objects.create(apply_id=obj.id, host_id=h.id, role=role, day=day, state='pending')

        obj_dict = model_to_dict(obj)
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.apply_user, json_obj, uuid=uid)

        content = u'你有一份待审批授权申请,申请人为:' + cuser \
                      + u"<br/>审核地址为:" + 'http://cmdb.mwbyd.cn/fortress/audit/'
        send_mail(u'堡垒机授权申请', '', configs.EMAIL_USER, [configs.OPS_EMAIL], html_message=content)

        return Response({"success": True, "msg": "succ!"})

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        queryset = ApplyRecord.objects.all().order_by("-audit_time")
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
        for r in serializer.data:
            t = r
            if r['apply_time'] != None:
                t['apply_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['apply_time']))
            if r['audit_time'] != None:
                t['audit_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['audit_time']))
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    # @transaction.atomic()
    # def delete(self, request, *args, **kwargs):
    #     id_list = request.data.getlist('id[]', [])
    #     id = request.data.get('id', '')
    #     if id:
    #         id_list = id_list + id.split(",")
    #     if len(id_list) <= 0:
    #         raise APIValidateException(u'参数id[]和id不能都为空')
    #     records = ApplyRecord.objects.filter(id__in=id_list)
    #     uid = str(uuid.uuid1())
    #     for a in records:
    #         self.changeLog(a.id, str(a.apply_user) , 'delete apply record', uid=uid)
    #     records.delete()
    #     return Response({"success": True, "msg": "succ!", "errors": []})

class ApplyRecordDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    授权申请详情页

    输出参数：
    ● id                        ——   PK
    ● apply_user                ——   申请人
    ● reviewer                  ——   审核人
    ● state                     ——   状态
    ● role                      ——   权限
    ● day                       ——   天数
    ● apply_time                ——   申请时间
    ● reason                    ——   申请原因
    ● audit_time                ——   审批时间
    ● reviewer_reason           ——   审批原因
    """
    paginate_by = None
    queryset = ApplyRecord.objects.all()
    serializer_class = ApplyRecordSerializer

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    def delete(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许delete操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许put操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许patch操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


class ApplyTaskList(CmdbListCreateAPIView):
    """
    授权申请列表.

    查询参数：
    ● apply_id                  ——   申请人

    输出参数：
    ● id                        ——   PK
    ● apply_id                  ——   授权申请id
    ● host_id                   ——   主机id
    ● ip                        ——   主机ip
    ● state                     ——   状态
    ● role                      ——   权限
    ● day                       ——   天数
    ● result                    ——   任务执行结果
    ● run_time                  ——   执行时间
    ● finish_time               ——   完成时间

    """

    paginate_by = None
    queryset = ApplyTask.objects.all()
    filter_fields = ('apply_id', )
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ApplyTaskSerializer

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        queryset = ApplyTask.objects.all().order_by("-id")
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
        hostids = []
        for r in serializer.data:
            hostids.append(r['host_id'])
        host_dict = {}
        hids = []
        for h in Hosts.objects.filter(id__in=hostids):
            host_dict[str(h.id)] = h
            hids.append(h.id)
        service_dict = {}
        for s in AppService.objects.all():
            service_dict[s.id] = s
        host_service = defaultdict(list)
        for s in ServiceHost.objects.filter(host_id__in=hids):
            if service_dict.has_key(s.service_id):
                host_service[s.host_id].append(service_dict[s.service_id].name)
        for r in serializer.data:
            t = r
            t['service_name'] = []
            if host_service.has_key(int(r['host_id'])):
                t['service_name'] = host_service[int(r['host_id'])]
            t['ip'] = ''
            if host_dict.has_key(str(r['host_id'])):
                t['ip'] = host_dict[str(r['host_id'])].ip
            if r['run_time'] != None:
                t['run_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['run_time']))
            if r['finish_time'] != None:
                t['finish_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['finish_time']))
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

class MyApplyRecordList(CmdbListCreateAPIView):
    """
    我的授权申请列表.

    查询参数：
    ● state                     ——   状态

    输出参数：
    ● id                        ——   PK
    ● apply_user                ——   申请人
    ● reviewer                  ——   审核人
    ● state                     ——   状态
    ● role                      ——   权限
    ● day                       ——   天数
    ● apply_time                ——   申请时间
    ● reason                    ——   申请原因
    ● audit_time                ——   审批时间
    ● reviewer_reason           ——   审批原因

    """
    paginate_by = None
    queryset = ApplyRecord.objects.all()
    filter_fields = ('state', )
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ApplyRecordSerializer

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        username = self.request.user.username
        queryset = ApplyRecord.objects.filter(apply_user=username).order_by("-apply_time")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        results = []
        for r in serializer.data:
            t = r
            if r['apply_time'] != None:
                t['apply_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['apply_time']))
            if r['audit_time'] != None and r['audit_time'] > 0:
                t['audit_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['audit_time']))
            else:
                t['audit_time'] = None
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

class ChangeApplyState(CmdbListCreateAPIView):
    """
    修改申请状态.

    输入参数:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    ● state                     ——   状态(通过:finish,拒绝:refuse)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = ApplyRecord.objects.all()
    filter_fields = ('apply_user', 'reviewer', 'state')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ApplyRecordSerializer

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        cuser = request.user.username
        data = {'success': True, 'msg': u'操作成功'}
        state_list = []
        for s in ApplyRecord.STATE_CHOICES:
            state_list.append(s[0])
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        state = request.data.get("state", '')
        reviewer_reason = request.data.get("reviewer_reason", '')
        if len(id_list) <= 0 and not id:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if id:
            id_list += id.split(",")
        if state not in state_list:
            raise APIValidateException(u'state必须为 ' + " ".join(state_list) + u' 中的一个')
        apply_list = ApplyRecord.objects.filter(id__in=id_list)
        apply_dict = {}
        for a in apply_list:
            apply_dict[a.id] = a
            if a.state != 'pending':
                raise APIValidateException(u'该记录已经审批过,不能再次审批')
        apply_list.update(state=state, reviewer_reason=reviewer_reason, audit_time=int(time.time()), reviewer=cuser)
        uid = str(uuid.uuid1())
        for a in apply_list:
            obj = json.dumps(model_to_dict(a))
            self.changeLog(a.id, a.apply_user, obj, uid=uid)
        applytasks = ApplyTask.objects.filter(apply_id__in=id_list)
        if state == 'finish':
            applytasks.update(state='ready')
            hostids = []
            for t in applytasks:
                hostids.append(t.host_id)

            host_dict = {}
            for h in Hosts.objects.filter(id__in=hostids).exclude(state='deleted'):
                host_dict[h.id] = h

            # 添加授权记录
            for t in applytasks:
                if not host_dict.has_key(t.host_id):
                    continue
                apply = apply_dict[t.apply_id]
                AuthRecord.objects.filter(username=apply.apply_user, host_id=t.host_id).delete()
                AuthRecord.objects.create(username=apply.apply_user, host_id=t.host_id, role=t.role, cuser=cuser, ctime=int(time.time()), expiration_time=int(time.time()) + t.day*86400)
                try:
                    host = host_dict[t.host_id]
                    ApplyTaskAddUserKeyTask().addTask(cuser, applytask_id=t.id, username=apply.apply_user, role=t.role, ip=host.ip)
                except Exception, ex:
                    print str(ex)
                    pass
            for a in apply_list:
                content = u'<ul><li>你的授权申请已经审批通过, 请重新连接堡垒机, 或刷新堡垒机主机列表</li>'\
                          + u"<li>堡垒机地址为: fortress.mwbyd.cn</li>"\
                          + u"<li>你的堡垒机用户为:" + a.apply_user + '</li>'\
                          + u"<li>堡垒机使用方式见文档: http://wiki.mwbyd.cn/pages/viewpage.action?pageId=6334750</li>"\
                          + u"<li>如有问题请联系运维团队解决, 或发邮件到邮箱: group.yunwei@puscene.com</li></ul>"
                title = u'授权申请通过'
                users = User.objects.filter(username=a.apply_user)
                if len(users) > 0:
                    send_mail(title, '', settings.EMAIL_HOST_USER, [users[0].email], html_message=content)
        elif state == 'refuse':
            for a in apply_list:
                content = u'<ul><li>抱歉, 你的授权申请未通过</li>'\
                          + u"<li>如有疑问请咨询运维团队, 或发邮件到邮箱: group.yunwei@puscene.com</li></ul>"
                title = u'授权申请未通过'
                users = User.objects.filter(username=a.apply_user)
                if len(users) > 0:
                    send_mail(title, '', settings.EMAIL_HOST_USER, [users[0].email], html_message=content)
            applytasks.update(state='refuse')
        return Response(data)


class MySSHKey(CmdbListCreateAPIView):

    """
    我的SSH Key.

    输入/输出参数：
    ● username                  ——   用户名(无需输入)
    ● user_id                   ——   用户id(无需输入)
    ● ssh_key                   ——   SSH公钥(必输)
    """

    permission_classes = (permissions.AllowAny,)

    paginate_by = None
    queryset = SSHKey.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = SSHKeySerializer

    def get(self, request, *args, **kwargs):
        data = {}
        user_id = request.user.id
        if not user_id:
            return Response(data)
        userext = SSHKey.objects.filter(user_id=user_id)
        if len(userext) > 0:
            data['user_id'] = user_id
            data['user_name'] = request.user.username
            data['ssh_key'] = userext[0].ssh_key
            data['private_key'] = False
            if userext[0].private_key:
                data['private_key'] = True
        return Response(data)

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        data = {'success': True, 'msg': u'新增成功'}
        ssh_key = request.data.get("ssh_key", '')
        SSHKey.objects.filter(user_id=user_id).delete()
        u = SSHKey.objects.create(user_id=user_id, ssh_key=ssh_key, private_key='')
        u = model_to_dict(u)
        if ssh_key:
            status, output = FortressOps().addSSHKey(user.username, ssh_key)
            if not status:
                raise APIValidateException(output)
        self.changeLog(user.id, user.username, json.dumps(u))
        return Response(data)

class CreateMySSHKey(CmdbListCreateAPIView):

    """
    创建我的SSH Key.

    输入/输出参数：
    无
    """

    permission_classes = (permissions.AllowAny,)

    paginate_by = None
    queryset = SSHKey.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = SSHKeySerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user = request.user
        email = user.email
        user_id = user.id
        data = {'success': True, 'msg': u'新增成功'}
        status, result = create_ssh_key(email, user_id, user.username)
        if not status:
            raise APIValidateException(result)
        u = model_to_dict(result)
        self.changeLog(user.id, user.username, json.dumps(u))
        data['ssh_key'] = result.ssh_key
        return Response(data)

class DownloadSSHKey(CmdbListCreateAPIView):

    """
    获取我的SSH Key.

    输出参数：
    ● username                  ——   用户名(无需输入)
    ● user_id                   ——   用户id(无需输入)
    ● ssh_key                   ——   SSH Key(必输)
    """

    permission_classes = (permissions.AllowAny,)

    paginate_by = None
    queryset = SSHKey.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = SSHKeySerializer

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def get(self, request, *args, **kwargs):
        user = request.user
        user_id = user.id
        email = user.email
        ssh_key = SSHKey.objects.filter(user_id=user_id)
        if len(ssh_key) <= 0:
            status, ssh_key = create_ssh_key(email, user_id, user.username)
            if not status:
                raise APIValidateException(ssh_key)
        else:
            ssh_key = ssh_key[0]
        private_key = ssh_key.private_key
        response = StreamingHttpResponse(streaming_content=private_key)
        response['Content-Disposition'] = 'attachment;filename=' + 'id_rsa'
        return response

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)