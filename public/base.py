# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.forms import model_to_dict
from django.views.generic import TemplateView
from django.http import *
from rest_framework import generics
from change.models import Change
import time, uuid
from rest_framework import permissions
from cmdb import configs
from urllib import quote
from rest_framework_jsonp.renderers import JSONPRenderer, JSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer

from cmdb.templatetags.mytags import register
from users.models import Menu, GroupMenu
from django.db.models import Q

class PublicView(TemplateView):
    userinfo = None

    def dispatch(self, request, *args, **kwargs):
        self.userinfo = request.user
        url = request.get_full_path()
        if not self.userinfo.username:
            login_url = "/home/login?redirect_url=" + url
            # callback_url = "http://" + self.request.get_host() + configs.CALLBACK_URL
            # login_url = configs.LOGIN_URL + "?redirect_url=" + quote(callback_url + "?redirect_url=" + quote(url))
            return HttpResponseRedirect(login_url)
        return super(PublicView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PublicView, self).get_context_data(**kwargs)
        context['user'] = self.userinfo
        context['menus'] = self.get_menu()
        context['ticket_url'] = configs.TICKET_URL
        context['system_name'] = u'乐道CMDB'
        context['system_version'] = configs.CMDB_VERSION
        return context
# ----------------------------------------------获取相应用户的菜单------------------------------------------------
    def get_menu(self):
        is_superuser = self.request.user.is_superuser
        is_staff = self.request.user.is_staff
        data = []
        all_menus = Menu.objects.all().order_by("-weight")

        if is_superuser != 1:
            ids = []
            current_user_set = self.request.user
            current_group_set = Group.objects.filter(Q(user=current_user_set))     # 获取当前用户所对应的所有组
            gids = []
            for group in current_group_set:
                gids.append(group.id)
            group_menu_list = GroupMenu.objects.filter(group_id__in=gids)
            for menu in group_menu_list:
                ids.append(menu.menu_id)
            ids = list(set(ids)) # id 去重
            all_menus = all_menus.filter(id__in=ids)

        for m in all_menus.filter(pid=0):
            m = model_to_dict(m)
            m['children'] = []
            m['has_children'] = False
            for me in all_menus.filter(pid=m['id']):
                m['children'].append(model_to_dict(me))
                m['has_children'] = True
            data.append(m)
        return data       # 输出一个 字典列表


# ------------------------------------------------------------------------------------------------------------

class CmdbBasePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method.lower() == 'get':
            return True
        return request.user.is_superuser or request.user.is_staff        # 返回是超级用户或者是职员

class CmdbListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = (CmdbBasePermission,)

    def changeLog(self, res_id, index, message, **kwargs):
        uid = str(uuid.uuid1())
        if kwargs.has_key('uid'):
            uid = str(kwargs['uid'])
        action = None
        if kwargs.has_key('action'):
            action = kwargs['action']
        resource = self.serializer_class.Meta.model._meta.db_table
        if kwargs.has_key('resource'):
            resource = kwargs['resource']
        http_method = self.request.method.lower()
        if not action:
            if http_method == 'get':
                action = 'search'
            elif http_method == 'post':
                action = 'create'
            elif http_method == 'put' or http_method == 'patch':
                action = 'update'
            elif http_method == 'delete':
                action = 'delete'
        Change.objects.create(username=self.request.user.username, resource=resource, res_id=res_id, uuid=uid,
                              action=action, index=index, message=message, change_time=int(time.time()), ctime=int(time.time()))


class CmdbRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (CmdbBasePermission,)

    def changeLog(self, res_id, index, message, **kwargs):       # changeLog 暂时不用管
        uid = str(uuid.uuid1())
        if kwargs.has_key('uid'):
            uid = str(kwargs['uid'])
        action = None
        if kwargs.has_key('action'):
            action = kwargs['action']
        resource = self.serializer_class.Meta.model._meta.db_table
        if kwargs.has_key('resource'):
            resource = kwargs['resource']
        http_method = self.request.method.lower()
        if not action:
            if http_method == 'get':
                action = 'search'
            elif http_method == 'post':
                action = 'create'
            elif http_method == 'put' or http_method == 'patch':
                action = 'update'
            elif http_method == 'delete':
                action = 'delete'
        Change.objects.create(username=self.request.user.username, resource=resource, res_id=res_id, uuid=uid,
                              action=action, index=index, message=message, change_time=int(time.time()), ctime=int(time.time()))
