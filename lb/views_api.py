# -*- coding: utf-8 -*-
import time, re, json, redis, uuid, commands
from rest_framework import filters
from lb.models import LB, ServiceLB
from lb.serializers import LBSerializer, ServiceLBSerializer
from rest_framework.response import Response
from public.base_exception import APIValidateException
from asset.models import Room
from app.models import App, AppService, ServiceHost
from django.db import transaction
from django.forms.models import model_to_dict
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView
from host.models import Hosts
from django.http import HttpResponse
from host.lib.host_tools import HostValidate
from host.serializers import HostsSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from app.serializers import ServiceHostSerializer
from public.common.tools import check_ip
from cmdb import configs
from collections import defaultdict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class LBList(CmdbListCreateAPIView):
    """
    负载均衡列表/创建负载均衡.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● env                       ——   环境
    ● server_name               ——   服务名
    ● lb_service_id             ——   Nginx服务id
    ● search                    ——   模糊搜索(hostname, comment)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● lb_service_id             ——   Nginx服务id
    ● lb_service_name           ——   Nginx服务名称
    ● env                       ——   环境
    ● server_name               ——   域名
    ● port                      ——   端口
    ● sslport                   ——   ssl端口
    ● ssl_conf                  ——   ssl配置
    ● parameter                 ——   参数
    ● access_log                ——   访问日志
    ● error_log                 ——   错误日志
    ● comment                   ——   负载均衡描述
    ● ctime                     ——   创建时间
    ● cuser                     ——   创建用户

    批量删除参数:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = LB.objects.all()
    filter_fields = ('env', 'server_name', 'port', 'lb_service_id')
    search_fields = ('server_name', 'comment')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = LBSerializer

    def get_queryset(self):
        queryset = LB.objects.all()
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

        service_dict = {}
        for service in AppService.objects.filter(id__in=[h['lb_service_id'] for h in serializer.data]):
            service_dict[service.id] = service.name

        for h in serializer.data:
            t = h
            t['lb_service_name'] = service_dict.get(h['lb_service_id'], '')
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    @transaction.atomic()
    def perform_create(self, serializer):
        user = self.request.user.username
        current_time = int(time.time())
        obj = serializer.save(ctime=current_time, cuser=user)
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.server_name, json_obj)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(ServiceLB.objects.filter(lb_id__in=id_list)) > 0:
            raise APIValidateException(u'lb还有location配置,不能删除')
        lblist = LB.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in lblist:
            self.changeLog(a.id, a.server_name, 'delete lb: ' + a.server_name, uid=uid)
        lblist.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})


class LBDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    负载均衡详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● lb_service_id             ——   Nginx服务id
    ● lb_service_name           ——   Nginx服务名称
    ● env                       ——   环境
    ● server_name               ——   域名
    ● port                      ——   端口
    ● sslport                   ——   ssl端口
    ● ssl_conf                  ——   ssl配置
    ● parameter                 ——   参数
    ● comment                   ——   负载均衡描述
    ● ctime                     ——   创建时间
    ● cuser                     ——   创建用户
    """
    paginate_by = None
    queryset = LB.objects.all()
    serializer_class = LBSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        id = instance.id
        if len(ServiceLB.objects.filter(lb_id=id)) > 0:
            raise APIValidateException(u'还有location配置,不能删除')
        instance.delete()
        self.changeLog(instance.id, instance.server_name, 'delete lb: ' + instance.server_name)

    @transaction.atomic()
    def perform_update(self, serializer):
        obj = serializer.save()
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.server_name, json_obj)


class ServiceLBList(CmdbListCreateAPIView):
    """
    负载均衡列表/创建负载均衡.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● lb_id                     ——   负载均衡器id
    ● service_id                ——   Upstream服务id
    ● server_name               ——   server_name
    ● search                    ——   模糊搜索(location_parameter, path)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● lb_id                     ——   负载均衡器id(无需输入)
    ● service_id                ——   Upstream服务id(必需)
    ● path                      ——   location路径(必需)
    ● proxy_path                ——   转发路径
    ● type                      ——   负载均衡算法(wrr,ip_hash)(必需)
    ● backend_port              ——   后端端口(必需)
    ● max_fails                 ——   max_fails(必需)
    ● fail_timeout              ——   fail_timeout(必需)
    ● location_parameter        ——   location参数
    ● lb                        ——   负载均衡器,参数如下(无需输入)

    以下为负载均衡器参数:
    ● id                        ——   PK(无需输入)
    ● lb_service_id             ——   Nginx服务id(必需)
    ● lb_service_name           ——   Nginx服务名称
    ● env                       ——   环境(必需)
    ● server_name               ——   域名(必需)
    ● port                      ——   端口(必需)
    ● sslport                   ——   ssl端口
    ● parameter                 ——   参数
    ● comment                   ——   描述
    ● ctime                     ——   创建时间(无需输入)
    ● cuser                     ——   创建用户(无需输入)

    批量删除参数:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = ServiceLB.objects.all()
    filter_fields = ('lb_id', 'service_id')
    search_fields = ('location_parameter', 'path')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ServiceLBSerializer

    def get_queryset(self):
        server_name = self.request.query_params.get('server_name', '')
        queryset = ServiceLB.objects.all()
        if server_name:
            lb_ids = [l.id for l in LB.objects.filter(server_name=server_name)]
            queryset = queryset.filter(lb_id__in=lb_ids)
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

        serviceids = [h['service_id'] for h in serializer.data]
        lblist = LB.objects.filter(id__in=[h['lb_id'] for h in serializer.data])
        for l in lblist:
            serviceids.append(l.lb_service_id)

        service_dict = {}
        for service in AppService.objects.filter(id__in=serviceids):
            service_dict[service.id] = service.name

        lbid_dict = {}
        for lb in lblist:
            tmp = model_to_dict(lb)
            tmp['lb_service_name'] = service_dict.get(tmp['lb_service_id'], str(tmp['lb_service_id']))
            lbid_dict[lb.id] = tmp

        for h in serializer.data:
            t = h
            t['service_name'] = service_dict.get(h['service_id'], '')
            t['lb'] = lbid_dict.get(h['lb_id'], {})
            results.append(t)
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

    @transaction.atomic()
    def create_servicelb(self, serializer):
        user = self.request.user.username
        lb_service_id = self.request.data.get('lb_service_id', 0)
        server_name = self.request.data.get('server_name', '')
        port = self.request.data.get('port', '')
        env = self.request.data.get('env', '')
        sslport = self.request.data.get('sslport', 0)
        service_id = self.request.data.get('service_id', '')
        if not sslport:
            sslport = 0
        parameter = self.request.data.get('parameter', '')
        if not lb_service_id:
            raise APIValidateException(u'lb_service_id不能为空')
        if not server_name:
            raise APIValidateException(u'server_name不能为空')
        if not port:
            raise APIValidateException(u'port不能为空')
        if not env:
            raise APIValidateException(u'env不能为空')
        if env not in [e[0] for e in Hosts.HOST_ENV_CHOICES]:
            raise APIValidateException(u'env不存在')
        if not service_id:
            raise APIValidateException(u'service_id不能为空')
        if len(AppService.objects.filter(id=service_id)) <= 0:
            raise APIValidateException(u'服务不存在')
        lb = LB.objects.filter(server_name=server_name, port=port, env=env)
        if len(lb) > 0:
            lb.update(sslport=sslport, parameter=parameter, lb_service_id=lb_service_id)
            lb = lb[0]
        else:
            lb = LB.objects.create(server_name=server_name, port=port, env=env, sslport=sslport, lb_service_id=lb_service_id,
                                   parameter=parameter, cuser=user, ctime=int(time.time()))
        obj = serializer.save(lb_id=lb.id)
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.path, json_obj)

    def perform_create(self, serializer):

        lb_service_id = self.request.data.get('lb_service_id', 0)
        env = self.request.data.get('env', '')
        appservice = AppService.objects.filter(id=lb_service_id)
        if len(appservice) <= 0:
            raise APIValidateException(u'Nginx集群服务不存在')
        try:
            self.create_servicelb(serializer)
        except Exception, ex:
            raise ex
        ########################### 推送配置文件 ###########################
        state, output = ssh_push_conf(appservice[0].name, env)
        if not state:
            raise APIValidateException(output)
        ########################### 推送配置文件 ###########################

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        servicelblist = ServiceLB.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in servicelblist:
            self.changeLog(a.id, a.path, 'delete location: ' + a.path, uid=uid)
        servicelblist.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})


class ServiceLBDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    负载均衡详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● lb_id                     ——   负载均衡器id(无需输入)
    ● service_id                ——   Upstream服务id(必需)
    ● path                      ——   location路径(必需)
    ● proxy_path                ——   转发路径
    ● type                      ——   负载均衡算法(wrr,ip_hash)(必需)
    ● backend_port              ——   后端端口(必需)
    ● max_fails                 ——   max_fails(必需)
    ● fail_timeout              ——   fail_timeout(必需)
    ● location_parameter        ——   location参数
    ● lb                        ——   负载均衡器,参数如下(无需输入)

    以下为负载均衡器参数:
    ● id                        ——   PK(无需输入)
    ● lb_service_id             ——   Nginx服务id(必需)
    ● lb_service_name           ——   Nginx服务名称
    ● env                       ——   环境(必需)
    ● server_name               ——   域名(必需)
    ● port                      ——   端口(必需)
    ● sslport                   ——   ssl端口
    ● parameter                 ——   参数
    ● comment                   ——   描述
    ● ctime                     ——   创建时间(无需输入)
    ● cuser                     ——   创建用户(无需输入)
    """
    paginate_by = None
    queryset = ServiceLB.objects.all()
    serializer_class = ServiceLBSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = serializer.data
        appservice = AppService.objects.filter(id=result['service_id'])
        result['service_name'] = ''
        if len(appservice) > 0:
            result['service_name'] = appservice[0].name
        lb = LB.objects.filter(id=result['lb_id'])
        result['lb'] = {}
        if len(lb) > 0:
           result['lb'] = model_to_dict(lb[0])
        return Response(result)

    @transaction.atomic()
    def perform_destroy(self, instance):
        instance.delete()
        self.changeLog(instance.id, instance.path, 'delete location: ' + instance.path)

    @transaction.atomic()
    def update_servicelb(self, serializer):
        user = self.request.user.username
        lb_service_id = self.request.data.get('lb_service_id', 0)
        server_name = self.request.data.get('server_name', '')
        port = self.request.data.get('port', '')
        env = self.request.data.get('env', '')
        sslport = self.request.data.get('sslport', 0)
        service_id = self.request.data.get('service_id', '')
        if not sslport:
            sslport = 0
        parameter = self.request.data.get('parameter', '')
        if not lb_service_id:
            raise APIValidateException(u'lb_service_id不能为空')
        if not server_name:
            raise APIValidateException(u'server_name不能为空')
        if not port:
            raise APIValidateException(u'port不能为空')
        if not env:
            raise APIValidateException(u'env不能为空')
        if env not in [e[0] for e in Hosts.HOST_ENV_CHOICES]:
            raise APIValidateException(u'env不存在')
        if not service_id:
            raise APIValidateException(u'service_id不能为空')
        if len(AppService.objects.filter(id=service_id)) <= 0:
            raise APIValidateException(u'服务不存在')
        lb = LB.objects.filter(server_name=server_name, port=port, env=env)
        if len(lb) > 0:
            lb.update(sslport=sslport, parameter=parameter)
            lb = lb[0]
        else:
            lb = LB.objects.create(server_name=server_name, port=port, env=env, sslport=sslport,
                                   parameter=parameter, cuser=user, ctime=int(time.time()))
        obj = serializer.save(lb_id=lb.id)
        json_obj = json.dumps(model_to_dict(obj))
        self.changeLog(obj.id, obj.path, json_obj)

    def perform_update(self, serializer):
        lb_service_id = self.request.data.get('lb_service_id', 0)
        env = self.request.data.get('env', '')
        appservice = AppService.objects.filter(id=lb_service_id)
        if len(appservice) <= 0:
            raise APIValidateException(u'Nginx集群服务不存在')
        try:
            self.update_servicelb(serializer)
        except Exception, ex:
            raise ex
        ########################### 推送配置文件 ###########################
        state, output = ssh_push_conf(appservice[0].name, env)
        if not state:
            raise APIValidateException(output)
        ########################### 推送配置文件 ###########################

class NginxConf(CmdbRetrieveUpdateDestroyAPIView):
    """
    Nginx配置文件详情页

    输出参数：
    ● filename                  ——   负载均衡配置文件名
    ● service_ips               ——   nginx服务组ip列表,如:['1.1.1.1', '2.2.2.2']
    ● service_id                ——   nginx集群服务id
    ● env                       ——   环境
    ● nginx_conf                ——   nginx配置文件内容
    """
    paginate_by = None
    queryset = LB.objects.all()
    serializer_class = LBSerializer

    def put(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许put操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许patch操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许delete操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    def get(self, request, *args, **kwargs):
        env = request.GET.get('env', '')
        service_name = kwargs.get("service_name", '')
        appservice = AppService.objects.filter(name=service_name)
        if len(appservice) <= 0:
            raise APIValidateException(u'服务' + service_name + u'不存在')
        appservice = appservice[0]
        if appservice.type != 'nginx':
            raise APIValidateException(service_name + u'的服务类型不是nginx')
        if not env:
            raise APIValidateException(u'env不能为空')
        if env not in [e[0] for e in Hosts.HOST_ENV_CHOICES]:
            raise APIValidateException(u'env不能为:' + env)
        lblist = LB.objects.filter(lb_service_id=appservice.id, env=env)
        lb_ids = [lb.id for lb in lblist]
        servicelblist = ServiceLB.objects.filter(lb_id__in=lb_ids)
        serviceids = [s.service_id for s in servicelblist]

        # 服务名称
        sid_name = {}
        for s in AppService.objects.filter(id__in=serviceids):
           sid_name[s.id] = s.name

        # 服务端口,server name下的location
        service_port = {}
        server_locations = defaultdict(list)
        for s in servicelblist:
            service_port[sid_name.get(s.service_id, '')] = s.backend_port
            server_locations[s.lb_id].append(s)

        # 服务中online的主机
        onlinehostids = []
        host_sids = defaultdict(list)
        for h in ServiceHost.objects.filter(service_id__in=serviceids, state='Up'):
            onlinehostids.append(h.host_id)
            host_sids[h.host_id].append(h.service_id)

        # 服务在线主机列表
        s_ips = defaultdict(list)
        for h in Hosts.objects.filter(id__in=onlinehostids, env=env):
            for sid in host_sids.get(h.id, []):
                s_ips[sid_name.get(sid, '')].append(h.ip)

        conf = ""

        # 生成upstream配置文件
        upstreams = ""
        for service, ips in s_ips.items():
            servers = ""
            backend_port = service_port.get(service, 0)
            if not backend_port:
                raise APIValidateException(u'服务 ' + service + u" backend端口配置错误")
            for ip in ips:
                servers += "\tserver %s:%s weight=100;\n" % (ip, backend_port)
            upstream = "upstream %s.%s {\n%s}\n" % (service, env, servers)
            upstreams += upstream

        # 如果upstream为空则不生成后续配置文件
        if not upstreams:
            return HttpResponse(conf, content_type='application/json')
        conf += upstreams

        # 生成server配置文件
        servers = ''
        for lb in lblist:
            locations = ''
            parameter = lb.parameter
            if not parameter:
                parameter = ''
            parameter = parameter.replace("\r", '')
            parameter = parameter.replace("\t", '')
            parameter_list = parameter.split("\n")
            p_arr = []
            for p in parameter_list:
                p_arr.append(p.strip())
            parameter = "\n\t".join(p_arr)
            for l in server_locations.get(lb.id, []):
                location_parameter = l.location_parameter
                if not location_parameter:
                    location_parameter = ""
                location_parameter = location_parameter.replace("\r", '')
                location_parameter = location_parameter.replace("\t", '')
                location_parameter_list = location_parameter.split("\n")
                arr = []
                for lp in location_parameter_list:
                    arr.append(lp.strip())
                location_parameter = "\n\t\t".join(arr)
                location = "\n\tlocation %s {\n\t\t%s\n\n\t\tproxy_pass http://%s.%s%s;\n\n\t}\n" % (l.path, location_parameter, sid_name[l.service_id], env, l.proxy_path)
                locations += location
            if lb.sslport != 0:
                server = "\nserver {\n\tserver_name  %s;\n\tlisten       %s;\n\tlisten       %s ssl;\n\t\n\t%s\n\t%s\n}\n" % \
                         (lb.server_name, lb.port, lb.sslport, parameter, locations)
            else:
                server = "\nserver {\n\tserver_name  %s;\n\tlisten       %s;\n\t\n\t%s\n\t%s\n}\n" % \
                         (lb.server_name, lb.port, parameter, locations)
            servers += server
        conf += servers
        return HttpResponse(conf, content_type='application/json')

class ChangeServiceHostState(CmdbListCreateAPIView):
    """
    修改服务主机upstream状态.

    输入/输出参数：
    ● service_name              ——   服务名称(必输)
    ● state                     ——   状态(online, offline)
    ● ip[]                      ——   ip列表
    ● ip                        ——   ip(多个ip用逗号隔开)
    注: 参数id和id[]不能都为空
    """
    paginate_by = None
    queryset = ServiceHost.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ServiceHostSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']

    def patch(self, request, *args, **kwargs):
        ip_list = request.data.getlist('ip[]', [])
        ip = request.data.get('ip', '')
        state = request.data.get('state', '')
        serviceName = request.data.get('service_name', '')
        if len(ip_list) <= 0 and not ip:
            raise APIValidateException(u'参数ip[]和ip不能都为空')
        if not serviceName:
            raise APIValidateException(u'参数service_name不能为空')
        if not state:
            raise APIValidateException(u'参数state不能为空')
        state_list = [s[0] for s in ServiceHost.STATE]
        if state not in state_list:
            raise APIValidateException(u'参数state必须为 ' + ",".join(state_list) + u" 中的一个")
        reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        for _ip in reip.findall(ip):
            ip_list.append(_ip)
        if len(ip_list) <= 0:
            raise APIValidateException(u'传入的ip不合法')
        for ip in ip_list:
            if not(check_ip(ip)):
                raise APIValidateException(u'传入的ip不合法')
        appservice = AppService.objects.filter(name=serviceName, state='online')
        if len(appservice) <= 0:
            raise APIValidateException(u'服务%s不存在或已被禁用' % serviceName)
        service_id = appservice[0].id
        hostlist = Hosts.objects.filter(ip__in=ip_list)
        hostids = [h.id for h in hostlist]
        env_list = [h.env for h in hostlist]
        env_list = list(set(env_list))
        if len(env_list) == 0:
            raise APIValidateException(u'找不到ip对应的环境')
        if len(env_list) > 1:
            raise APIValidateException(u'传入的ip必须属于同一个环境')
        ServiceHost.objects.filter(service_id=service_id, host_id__in=hostids).update(state=state)

        ########################### 推送配置文件 ###########################
        lbids = [s.lb_id for s in ServiceLB.objects.filter(service_id=service_id)]
        lbserviceids = [lb.lb_service_id for lb in LB.objects.filter(id__in=list(set(lbids)), env=env_list[0])]
        for sv in AppService.objects.filter(id__in=list(set(lbserviceids))):
            status, output = ssh_push_conf(sv.name, env_list[0])
            if not status:
                raise APIValidateException(output)

        ########################### 推送配置文件 ###########################

        return Response({'success': True, 'msg': 'succ!'})

class PushNginxConfig(CmdbListCreateAPIView):
    """
    推送nginx配置文件.

    输入/输出参数：
    ● service_name              ——   服务名称(必输)
    ● env                       ——   环境

    """
    paginate_by = None
    queryset = ServiceHost.objects.all()
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = ServiceHostSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许put操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许patch操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许delete操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['POST', 'HEAD', 'OPTIONS']

    def post(self, request, *args, **kwargs):
        service_name = request.data.get('service_name', '')
        env = request.data.get('env', '')
        if not service_name:
            raise APIValidateException(u'参数service_name不能为空')
        if not env:
            raise APIValidateException(u'参数env不能为空')
        env_list = [s[0] for s in Hosts.HOST_ENV_CHOICES]
        if env not in env_list:
            raise APIValidateException(u'参数env必须为 ' + ",".join(env_list) + u" 中的一个")
        services = AppService.objects.filter(name=service_name)
        if len(services) <= 0:
            raise APIValidateException(u'服务不存在')
        service = services[0]
        if service.type != 'nginx':
            raise APIValidateException(u'该服务不不是Nginx集群')
        ########################### 推送配置文件 ###########################
        status, output = ssh_push_conf(service_name, env)
        if not status:
            raise APIValidateException(output)
        ########################### 推送配置文件 ###########################
        return Response({'success': True, 'msg': 'succ!'})

def ssh_push_conf(service_name, env):
    cmd = 'ssh root@%s "cd /opt/cmdb-script/ && python push_nginx_conf.py %s %s %s"' % (configs.FORTRESS_HOST, configs.RUN_ENV, service_name, env)
    configs.logger.info(cmd)
    state, output = commands.getstatusoutput(cmd)
    if state != 0:
        configs.logger.error(output)
        return False, output
    return True, output

class DomainLBHostList(CmdbListCreateAPIView):
    """
    服务主机列表.

    查询参数：
    ● domain                    ——   域名(必输)
    ● env                       ——   环境(必输)(prod-生产环境, stg-预发环境, uat-集成测试环境, test-测试环境, dev-开发环境)
    ● room_id                   ——   机房id
    ● state                     ——   状态(free、online、offline、unuse)

    输入/输出参数：
    ● id                        ——   PK
    ● instance_id               ——   实例id
    ● sn                        ——   序列号
    ● type                      ——   主机类型(server, vm, net, aliyun, storage)
    ● attribute                 ——   属性(ECS, RDS, SLB, server, xen, switch, xenparent, dockerparent, docker, route, firewall, storage)
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
    filter_fields = ('room_id', 'state', 'env')
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = HostsSerializer

    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许post操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']

    def get_queryset(self):
        queryset = Hosts.objects.all()
        domain = self.request.query_params.get('domain', None)
        env = self.request.query_params.get('env', None)
        if not domain:
            raise APIValidateException(u'domain不能为空')
        if not env:
            raise APIValidateException(u'env不能为空')
        lb = LB.objects.filter(server_name=domain, lbenv=env)
        if len(lb) <= 0:
            raise APIValidateException(u'域名' + domain + " " + env + u"环境" + u'配置不存在')
        lb = lb[0]
        service = AppService.objects.filter(id=lb.service_id)
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

