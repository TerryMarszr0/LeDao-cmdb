# -*- coding: utf-8 -*-
from django.conf.urls import url
from users import views

urlpatterns = [

    # 用户管理
    url(r'^user/$', views.UserPageView.as_view()),

    # 菜单管理
    url(r'^menu/$', views.MenuPageView.as_view()),

    # 角色-菜单管理
    url(r'^group_menu/$', views.GroupMenuPageView.as_view()),

    # 我的个人信息
    url(r'^myinfo/$', views.MyInfoPageView.as_view()),

]
