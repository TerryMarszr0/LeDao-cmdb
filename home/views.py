# -*- coding: utf-8 -*-
import json, requests, time
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from public.base import PublicView
from cmdb import configs
from cmdb.configs import logger, CMDB_VERSION, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from public.common.mysqldb import DBOP
from public.redis.mq import RedisHealthCheck
from users.auth.ssoapi import login_sso, get_token
from users.models import DefaultGroup
from users.views_api import add_user_default_password
from django.contrib.auth.models import User
from urllib import unquote

def index_view(request):
    return HttpResponseRedirect('/host/')

class IndexPageView(PublicView):
    template_name = 'app/app.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'资产管理'
        context['path1'] = u'资产管理'
        context['path2'] = u'查看资产线'
        return context


class LoginPageView(TemplateView):
    template_name = 'home/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        return context

class SkinConfigView(TemplateView):
    template_name = 'skin_config.html'

    def get_context_data(self, **kwargs):
        context = super(SkinConfigView, self).get_context_data(**kwargs)
        return context

@csrf_exempt
def doLogin(request):

    data = {'success': False, 'msg': 'fail!'}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # username_list = username.split('@')
        # if len(username_list) == 1 and not str(username).isdigit():
        #     username += '@puscene.com'
        # status, userinfo = login_sso(username, password)
        # if not status:
        #     return HttpResponse(json.dumps(data), content_type='application/json')
        # email_arr = userinfo['email'].split('@')
        # users = User.objects.filter(username=email_arr[0])
        # if len(users) <= 0:
        #     # 默认的组关联到用户上
        #     default_group_list = []
        #     value_list = DefaultGroup.objects.values("group_name")
        #     for value in value_list:
        #         default_group_list.append(value['group_name'])
        #     user = add_user_default_password('auto', email_arr[0], userinfo['email'], 0, 0, default_group_list)
        # else:
        #     user = users[0]
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            data['success'] = True
            data['msg'] = 'succ!'
    else:
        data['msg'] = 'request method must be POST'
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@csrf_exempt
def sso_login(request):
    tokenKey = request.GET.get('tokenKey', '')
    redirect_url = request.GET.get('redirect_url', '/')
    status, userinfo = get_token(tokenKey)
    if status:
        email_arr = userinfo['email'].split('@')
        users = User.objects.filter(username=email_arr[0])
        if len(users) <= 0:
            # 默认的组关联到用户上
            default_group_list = []
            value_list = DefaultGroup.objects.values("group_name")
            for value in value_list:
                default_group_list.append(value['group_name'])
            user = add_user_default_password('auto', email_arr[0], userinfo['email'], 0, 0, default_group_list)
        else:
            user = users[0]
        if user and user.is_active:
            auth.login(request, user)
    return HttpResponseRedirect(unquote(redirect_url))


@csrf_exempt
def healthCheck(request):
    data = {'success': False, 'msg': 'fail!'}
    if request.method == 'GET':
        data['version'] = CMDB_VERSION
        # 测试数据库状态
        db_op = DBOP(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)
        data['db_state'] = 'health' if db_op.dbhealthcheck("show tables;") else 'exception'
        # 测试redis状态
        data['redis_state'] = 'health' if RedisHealthCheck().state else 'exception'
        data['success'] = True
        data['msg'] = 'succ!'
    else:
        data['msg'] = 'request method must be GET'
    return HttpResponse(json.dumps(data), content_type='application/json')
