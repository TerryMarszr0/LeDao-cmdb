# -*- coding: utf-8 -*-

import json
import uuid

from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.forms.models import model_to_dict
from rest_framework import filters
from rest_framework import parsers, renderers
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from fortress.task.fortresstask import AddFortressUserTask
from public.base import CmdbListCreateAPIView, CmdbRetrieveUpdateDestroyAPIView
from public.base_exception import APIValidateException
from users.models import Menu, GroupMenu, DefaultGroup
from users.serializers import UserSerializer, MenuSerializer, GroupMenuSerializer, GroupSerializer
from app.models import ServicePrincipals, AppPrincipals



def add_user_default_password(crate_user, username, email, is_superuser, is_staff, group_list):
    user = User()
    user.username = username
    user.set_password('LeDao;123')
    user.email = email
    user.is_superuser = int(is_superuser)
    user.is_staff = int(is_staff)
    user.save()
    user.groups = Group.objects.filter(name__in=group_list)


    ########################################## 添加堡垒机用户任务 ##########################################
    # try:
    #     AddFortressUserTask().addTask(crate_user, username=username, email=email)
    # except:
    #     pass
    ########################################## 添加堡垒机用户任务 ##########################################
    return user

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method.lower() == 'get':
            return True
        return request.user.is_superuser

class UserList(CmdbListCreateAPIView):

    """
    用户列表.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● username                  ——   用户名
    ● email                     ——   邮箱
    ● is_superuser              ——   是否超级管理员
    ● is_staff                  ——   是否管理员
    ● search                    ——   搜索内容(username, email)

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● username                  ——   用户名(必输)
    ● email                     ——   邮箱(必输)
    ● is_superuser              ——   是否超级管理员(必输)
    ● is_staff                  ——   是否管理员(必输)
    ● last_login                ——   最后登录时间
    ● date_joined               ——   创建时间

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """

    permission_classes = (UserPermission,)

    paginate_by = None
    queryset = User.objects.all()

    filter_fields = ('username', 'email', 'is_superuser', 'is_staff', )
    search_fields = ('username', 'email', )
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = UserSerializer
    #todo ?????????
    def get_queryset(self):
        queryset = User.objects.all().order_by("-date_joined")
        id = self.request.query_params.get('id', None)
        if id:
            id_arr = id.split(",")
            queryset = queryset.filter(id__in=id_arr)
        return queryset

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        crate_user = request.user.username
        data = {'success': True, 'msg': u'新增成功'}
        username = request.data.get("username", '')
        email = request.data.get("email", '')
        is_superuser = request.data.get("is_superuser", 0)
        is_staff = request.data.get("is_staff", 0)
        group_list = request.data.getlist('group_list[]')  # 获取用户关联的组信息
        if not username:
            raise APIValidateException(u'username 不能为空')
        if not str(is_superuser).isdigit() or int(is_superuser) not in (0, 1):
            raise APIValidateException(u'is_superuser 只能为0或1')
        if not str(is_staff).isdigit() or int(is_staff) not in (0, 1):
            raise APIValidateException(u'is_staff 只能为0或1')
        if len(User.objects.filter(username=username)) > 0:
            raise APIValidateException(u'用户' + username + u'已存在')

        user = add_user_default_password(crate_user, username, email, is_superuser, is_staff, group_list)

        u = model_to_dict(user)
        u.pop('password')
        u.pop('groups')
        u.pop('user_permissions')
        u['date_joined'] = str(u['date_joined'])
        if u['last_login']:
            u['last_login'] = str(u['last_login'])
        self.changeLog(user.id, user.username, json.dumps(u))
        return Response(data)

    # 批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        id_list = request.data.getlist('id[]', [])
        id = request.data.get('id', '')
        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        if len(User.objects.filter(id__in=id_list, is_superuser=1)) > 0:
            raise APIValidateException(u'不能删除超级管理员')
        userlist = User.objects.filter(id__in=id_list)
        uid = str(uuid.uuid1())
        for a in userlist:
            self.changeLog(a.id, a.username, 'delete user: ' + a.username, uid=uid)
        userlist.delete()
        return Response({"success": True, "msg": "succ!", "errors": []})

    # 扩展列 user_group
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        results = []
        for d in serializer.data:
            d['group_list'] = []
            for group in Group.objects.filter(id__in=d['groups']):
                d['group_list'].append(group.name)

            d['default_group_list'] = []
            for default_group in DefaultGroup.objects.values("group_name"):
                d['default_group_list'].append(default_group['group_name'])
            results.append(d)

        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

class UserDetail(CmdbRetrieveUpdateDestroyAPIView):
    """
    用户详情页

    输入/输出参数：
    ● id                        ——   PK(无需输入)
    ● username                  ——   用户名
    ● email                     ——   邮箱
    ● is_superuser              ——   是否超级管理员
    ● is_staff                  ——   是否管理员
    ● last_login                ——   最后登录时间
    ● date_joined               ——   创建时间
    """

    permission_classes = (UserPermission,)

    paginate_by = None
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic()
    def perform_destroy(self, instance):
        if instance.is_superuser == 1:
            raise APIValidateException(u'不能删除超级管理员')
        id = self.kwargs.get('pk', '')
        user = User.objects.get(id=id)
        user.groups = []

        #删除应用和服务中绑定的用户信息
        old_name = user.username
        AppPrincipals.objects.filter(user_name=old_name).delete()   #应用
        ServicePrincipals.objects.filter(user_name=old_name).delete()   #服务

        instance.delete()
        self.changeLog(instance.id, instance.username, 'delete user: ' + instance.username)

    @transaction.atomic()
    def perform_update(self, serializer):
        id = self.kwargs.get('pk', '')
        user = User.objects.get(id=id)

        #更新应用和服务中绑定的用户信息
        old_name = user.username
        new_name = self.request.data.get('username')
        if old_name != new_name:
            AppPrincipals.objects.filter(user_name=old_name).update(user_name=new_name)  #应用
            ServicePrincipals.objects.filter(user_name=old_name).update(user_name=new_name)  #服务

        obj = serializer.save()

        user = User.objects.get(id=obj.id)
        group_names = self.request.data.getlist('group_list[]')      # 获取用户关联的组信息
        user.groups = Group.objects.filter(name__in=group_names)     # 更新用户对应的组


        u = model_to_dict(obj)
        u.pop('password')
        u.pop('groups')
        u.pop('user_permissions')
        u['date_joined'] = str(u['date_joined'])
        if u['last_login']:
            u['last_login'] = str(u['last_login'])
        json_obj = json.dumps(u)
        self.changeLog(obj.id, obj.username, json_obj)

class UserToken(APIView):

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.username:
            return Response({'detail': u'用户未认证'}, status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key})

class UpdateUserToken(APIView):

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        if not request.user.username:
            return Response({'detail': u'用户未认证'}, status.HTTP_401_UNAUTHORIZED)
        Token.objects.filter(user_id=request.user.id).delete()
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key})

class ChangeUserPwd(CmdbListCreateAPIView):

    """
    用户修改密码.

    输入参数：
    ● old_password              ——   旧密码(必输)
    ● password                  ——   新密码(必输)

    """

    permission_classes = (UserPermission,)

    paginate_by = None
    queryset = User.objects.all()

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        raise APIValidateException(u'不允许get操作', status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    def _allowed_methods(self):
        return ['PATCH', 'HEAD', 'OPTIONS']

    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        data = {'success': True, 'msg': u'新增成功'}
        username = request.user.username
        password = request.data.get('password')
        old_password = request.data.get('old_password')

        if not password:
            raise APIValidateException(u'password 不能为空')
        user = auth.authenticate(username=username, password=old_password)
        if not user:
            raise APIValidateException(u'旧密码不正确')
        user.set_password(password)
        user.save()
        self.changeLog(user.id, user.username, 'change password')
        return Response(data)

class MenuList(CmdbListCreateAPIView):

    queryset = Menu.objects.all()   # 查出所有 menu 的值

    search_fields = ('name', 'path')   # 模糊查询的字段
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = MenuSerializer  # 业务线的序列化

    @transaction.atomic()          # 发生异常则回滚，保证操作的一致性和完整性
    def perform_create(self, serializer):     # 增添

        obj = serializer.save()
        obj_dict = model_to_dict(obj)
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.name, json_obj)  # 写日志

    #批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):  # args 相当是一个集合，kwargs 相当是一个字典
        id_list = request.data.getlist('id[]', [])  # 获取 id 列表
        id = request.data.get('id', '')  # 获取 id

        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        menus = Menu.objects.filter(id__in=id_list)  # 过滤出 id 在 id_list 的 menu
        uid = str(uuid.uuid1())  # 生成唯一的 id

        group_names = []
        for a in menus:
            group_names.append(a.name)
            self.changeLog(a.id, a.name, 'delete menu: ' + a.name, uid=uid)

        menus.delete()  # 删除相应的 menus
        return Response({"success": True, "msg": "succ!", "errors": []})  # 该函数返回 Response 对象

    def get_queryset(self):
        queryset = Menu.objects.all().order_by("-id")
        return queryset

class MenuDetail(CmdbRetrieveUpdateDestroyAPIView):

    paginate_by = None
    queryset = Menu.objects.all()            # 查询所有数据
    serializer_class = MenuSerializer        # 序列菜单对象

    @transaction.atomic()                    # 菜单的删除操作
    def perform_destroy(self, instance):

        id = instance.id
        instance.delete()                    # 执行删除操作
        self.changeLog(id, instance.name, 'delete menu: ' + instance.name)

    @transaction.atomic()                              # 菜单的更新操作
    def perform_update(self, serializer):

        id = self.kwargs.get('pk', '')                 # 获取id ，默认值为 ''
        menu = Menu.objects.filter(id=id)              # 过滤出相应 id 的菜单名
        if len(menu) <= 0:                             # 没有相应菜单名
            raise APIValidateException(u'没有相应的信息')    # 抛异常

        pid = self.request.data.get('pid')             # 如果传过来的值是 '' 则自动的附 0
        if pid=='':
            obj = serializer.save(pid=0)
        else:
            obj = serializer.save()

        obj_dict = model_to_dict(obj)                  # 写日志
        json_obj = json.dumps(obj_dict)
        self.changeLog(obj.id, obj.name, json_obj)

class GroupList(CmdbListCreateAPIView):
    """
    角色列表.

    查询参数：
    ● id                        ——   PK(查询多个用逗号隔开)
    ● name                      ——   组名
    ● search                    ——   搜索内容(name)

    输入参数：
    ● id                        ——   ID(不用输入)
    ● name                      ——   组名称(必输)
    ● menu_id[]                 ——   菜单列表(必输)

    输出参数：
    ● id                        ——   ID
    ● name                      ——   组名称
    ● menu_ids                  ——   菜单列表

    批量删除:
    ● id[]                      ——   id列表
    ● id                        ——   id(多个id用逗号隔开)
    注: 参数id和id[]不能都为空
    """

    queryset = Group.objects.all()   # 查出所有 menu 的值
    filter_fields = ('name',)
    search_fields = ('name',)   # 模糊查询的字段
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = GroupSerializer  # 业务线的序列化

    @transaction.atomic()  # 发生异常则回滚，保证操作的一致性和完整性
    def perform_create(self, serializer):  # 增添
        obj = serializer.save()
        #默认组要向DefaultGroup中添加
        is_default = self.request.data.get('is_default','0')
        if int(is_default) > 0:
            DefaultGroup.objects.create(group_name=obj.name)

        menu_list = self.request.data.get('menu_id[]', '')
        menu_ids = [int(x) for x in menu_list.split(',')]
        for menu_id in menu_ids:  # 向 auth_group_menu 表中添加数据
            GroupMenu.objects.create(group_id=obj.id, menu_id=menu_id)

    def get_queryset(self):
        queryset = Group.objects.all().order_by("-id")
        return queryset

    def list(self, request, *args, **kwargs):  # 扩展列 menu_ids
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        results = []
        for d in serializer.data:
            t = d
            t['menu_ids'] = []
            for gu in GroupMenu.objects.filter(group_id=d['id']):
                t['menu_ids'].append(gu.menu_id)

            is_default = len(DefaultGroup.objects.filter(group_name=d['name']))
            t['is_default'] = str(is_default)
            results.append(t)

        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)

class GroupDetail(CmdbRetrieveUpdateDestroyAPIView):

    queryset = Group.objects.all()            # 查询所有数据
    serializer_class = GroupSerializer        # 序列菜单对象

    @transaction.atomic()                    # 菜单的删除操作
    def perform_destroy(self, instance):
        id = self.kwargs.get('pk', '')       # 获取要删除的 id
        group = Group.objects.get(id=id)     # 删除相应的组
        group.delete()
        # 如果这个组是默认组，在 DefaultGroup 中要删除相应的组
        default_group = DefaultGroup.objects.filter(group_name=group.name)
        if len(default_group) > 0:
            default_group.delete()

        group_menus = GroupMenu.objects.filter(group_id=id)  # 删除 auth_group_menu 表中相应的组
        group_menus.delete()

    @transaction.atomic()  # 菜单的更新操作
    def perform_update(self, serializer):
        id = self.kwargs.get('pk', '')  # 获取id ，默认值为 ''
        obj = serializer.save()         # 先更改 auth_group 表中的

        # 默认组要向DefaultGroup中添加
        is_default = self.request.data.get('is_default', '0')
        if int(is_default) == 0:
            default_group = DefaultGroup.objects.filter(group_name=obj.name)
            if len(default_group) > 0:
                default_group.delete()
        else:
            default_group = DefaultGroup.objects.filter(group_name=obj.name)
            if len(default_group) == 0:
                DefaultGroup.objects.create(group_name=obj.name)

        menu_list = self.request.data.get("menu_id[]",'')
        menus =  [ int( x ) for x in menu_list.split(",") ]      # 将字符串转换为整形数组
        group_menus = GroupMenu.objects.filter(group_id=id)
        group_menus.delete()              # 将旧的删除
        for menu_id in menus:
            GroupMenu.objects.create(group_id=id,menu_id=menu_id)      # 循环将新数据插入

class GroupMenuList(CmdbListCreateAPIView):      # 有问题，为什么在 Group 中创建就会出现

    queryset = GroupMenu.objects.all()   # 查出所有 menu 的值

    search_fields = ('group_id')   # 模糊查询的字段
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    serializer_class = GroupMenuSerializer  # 业务线的序列化

    #批量删除
    @transaction.atomic()
    def delete(self, request, *args, **kwargs):  # args 相当是一个集合，kwargs 相当是一个字典
        id_list = request.data.getlist('id[]', [])  # 获取 id 列表
        id = request.data.get('id', '')  # 获取 id

        if id:
            id_list = id_list + id.split(",")
        if len(id_list) <= 0:
            raise APIValidateException(u'参数id[]和id不能都为空')
        groups = Group.objects.filter(id__in=id_list)     # 过滤出 id 在 id_list 的 menu

        group_name_list = []
        for group in groups:       # 删除相应组对应的菜单
            group_name_list.append(group.name)
            menus = GroupMenu.objects.filter(group_id=group.id)
            menus.delete()

        groups.delete()  # 删除相应的 groups
        # 删除 DefaultGroup 表中相应的组名
        default_groups = DefaultGroup.objects.filter(group_name__in=group_name_list)
        if len(default_groups) > 0:
            default_groups.delete()

        uid = str(uuid.uuid1())  # 生成唯一的 id
        return Response({"success": True, "msg": "succ!", "errors": []})  # 该函数返回 Response 对象

class GroupMenuDetail(CmdbRetrieveUpdateDestroyAPIView):

    queryset = GroupMenu.objects.all()            # 查询所有数据
    serializer_class = GroupMenuSerializer        # 序列菜单对象

    @transaction.atomic()                              # 菜单的更新操作
    def perform_update(self, serializer):

        id = self.kwargs.get('pk', '')                 # 获取id ，默认值为 ''
        group_menu = GroupMenu.objects.filter(id=id)              # 过滤出相应 id 的菜单名
        if len(group_menu) <= 0:                             # 没有相应菜单名
            raise APIValidateException(u'没有相应的信息')    # 抛异常

        obj = serializer.save()

        # obj_dict = model_to_dict(obj)                  # 写日志
        # json_obj = json.dumps(obj_dict)
        # self.changeLog(obj.id, obj.menu_id, json_ob

































