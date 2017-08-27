# -*- coding: utf-8 -*-
from django.conf.urls import url
from users import views_api

urlpatterns = [

    # 用户api
    url(r'^user/$', views_api.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views_api.UserDetail.as_view()),

    # 菜单api
    url(r'^menu/$', views_api.MenuList.as_view()),
    url(r'^menu/(?P<pk>[0-9]+)/$', views_api.MenuDetail.as_view()),

    # 组-菜单api
    url(r'^group_menu/$', views_api.GroupMenuList.as_view()),
    url(r'^group/$', views_api.GroupList.as_view()),
    url(r'^group_menu/(?P<pk>[0-9]+)/$', views_api.GroupMenuDetail.as_view()),
    url(r'^group/(?P<pk>[0-9]+)/$', views_api.GroupDetail.as_view()),

    # 用户token
    url(r'^token/$', views_api.UserToken.as_view()),

    # 获取新的用户token
    url(r'^newtoken/$', views_api.UpdateUserToken.as_view()),

    # 修改密码
    url(r'^changepwd/$', views_api.ChangeUserPwd.as_view()),
]
