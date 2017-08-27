# -*- coding: utf-8 -*-
from django.conf.urls import url
from host import views

urlpatterns = [

    # 新增设备
    url(r'^addhost/$', views.AddHostPageView.as_view()),

    # 新增阿里云
    url(r'^addaliyun/$', views.AddAliyunPageView.as_view()),

    # 修改设备信息
    url(r'^edit/$', views.UpdateHostPageView.as_view()),

    # 设备详细信息
    url(r'^detail/$', views.DetailHostPageView.as_view()),

    # 操作系统管理
    url(r'^image/$', views.HostImagePageView.as_view()),

    # 主机查询
    url(r'^host/$', views.HostPageView.as_view()),

    # 资产组主机列表
    url(r'^$', views.AppHostPageView.as_view()),
]
