# -*- coding: utf-8 -*-
from django.conf.urls import url
from app import views_api

urlpatterns = [

    # 应用api
    url(r'^app/$', views_api.AppList.as_view()),
    url(r'^app/(?P<pk>[0-9]+)/$', views_api.AppDetail.as_view()),

    # 业务线api
    url(r'^group/$', views_api.GroupList.as_view()),
    url(r'^group/(?P<pk>[0-9]+)/$', views_api.GroupDetail.as_view()),

    # 应用--负责人 api
    url(r'^app_principals/$', views_api.AppPrincipalsList.as_view()),
    url(r'^app_principals/(?P<pk>[0-9]+)/$', views_api.AppPrincipalsDetail.as_view()),

    # 应用api
    url(r'^service/$', views_api.AppServiceList.as_view()),
    url(r'^service/(?P<pk>[0-9]+)/$', views_api.AppServiceDetail.as_view()),
    url(r'^servicegroup/$', views_api.ServiceGroupList.as_view()),

    # 按ip扩容服务api
    url(r'^scaleoutbyip/$', views_api.ServiceScaleOutByIp.as_view()),

    # 自动扩容服务api
    url(r'^autoscaleout/$', views_api.ServiceAutoScaleOut.as_view()),

    # 按ip缩容服务api
    url(r'^reducebyip/$', views_api.ServiceReduceByIp.as_view()),

    # 应用资源使用统计 api
    url(r'^apps/(?P<pk>[0-9]+)/$', views_api.AppsStatistics.as_view()),

    # # 提供服务名以及该服务对应的服务器 ip 列表
    # url(r'^servicehostips/', views_api.ServiceHostIpsApi.as_view()),

    # # 保存来自于 Zabbix 中的服务资源信息
    # url(r'^serviceinformationsave/$', views_api.ServiceInformationSaveApi.as_view()),

    # 向前端提供来自 Zabbix 中的服务资源信息
    url(r'^serviceinformationshow/(?P<pk>[0-9]+)/$', views_api.ServiceInformationShowApi.as_view()),
]
