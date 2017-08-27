# -*- coding: utf-8 -*-
import json
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from rest_framework import filters

from users.serializers import UserSerializer
from public.base_exception import APIValidateException
from django.contrib.auth.models import User
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView
from django.db import transaction
from rest_framework import status
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from users.auth.ssoapi import login_sso
from django.contrib import auth


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):

        username = request.data.get('username', '')
        password = request.data.get('password', '')
        username_list = username.split('@')
        if len(username_list) == 1:
            username += '@puscene.com'
        status, userinfo = login_sso(username, password)
        username = username.split('@')[0]
        if not status:
            user = auth.authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise APIValidateException(u'用户名或密码错误')
        else:
            users = User.objects.filter(username=username)
            if len(users) <= 0:
                raise APIValidateException(u'用户不存在')
            user = users[0]
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class ApiDocument(CmdbListCreateAPIView):

    """
    api使用手册.

    用户认证：
    ● 认证方式                   ——   在http请求的head中加入Authorization,格式为Authorization: Token your token
    ● 调用实例                   ——   curl -X GET http://cmdb.mwbyd.cn/api/host/host/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
    ● 获取Token                 ——   登录CMDB->点击头像下方用户名->点击下拉窗口中API Token. 或者使用/api/tokenauth/ api获取token,例如: curl -X POST http://cmdb.mwbyd.cn/api/tokenauth/ -d'username=xx&password=xxx'
    ● API权限                   ——   所有用户(包括未认证的)都有GET权限,管理员和超级管理员有POST,PUT,PATCH,DELETE权限

    Http Method：
    ● GET                       ——   查询数据
    ● POST                      ——   新增数据
    ● PUT                       ——   修改数据(必须传所有字段值,未传字段将被更新成空)
    ● PATCH                     ——   修改数据(只需传入需要更新的字段即可,未传入字段保持原值)
    ● DELETE                    ——   删除数据

    Http Status Codes:
    ● 200                       ——   OK(查询或修改成功)
    ● 201                       ——   创建成功

    ● 400                       ——   数据校验错误(比如必输参数没传等)
    ● 401                       ——   未认证(用户未登录或者Token校验失败)
    ● 403                       ——   没有权限
    ● 405                       ——   Http Method不允许

    ● 5XX                       ——   服务器端错误

    分页api的全局查询条件:
    ● limit                     ——   查询条数
    ● offset                    ——   起始位置

    对象传递例子:
    ● id[]                      ——   后面带有[]的参数表示是数组，其数据传递的实例为:id[]=1&id[]=2&id[]=3&id[]=5

    Content-Type:
    ● Content-Type设置为:application/x-www-form-urlencoded

    """

    paginate_by = None
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic()
    def get(self, request, *args, **kwargs):
        return Response({"detail": u'api使用手册'})

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['GET', 'HEAD', 'OPTIONS']







