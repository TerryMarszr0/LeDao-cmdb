# -*- coding: utf-8 -*-
from django.conf.urls import url
from asset import views_api

urlpatterns = [

    # 机房api
    url(r'^room/$', views_api.RoomList.as_view()),
    url(r'^room/(?P<pk>[0-9]+)/$', views_api.RoomDetail.as_view()),

    # 机柜api
    url(r'^rack/$', views_api.RackList.as_view()),
    url(r'^rack/(?P<pk>[0-9]+)/$', views_api.RackDetail.as_view()),

    # 设备型号api
    url(r'^model/$', views_api.ModelList.as_view()),
    url(r'^model/(?P<pk>[0-9]+)/$', views_api.ModelDetail.as_view()),

    # 设备配置api
    url(r'^conf/$', views_api.ConfList.as_view()),
    url(r'^conf/(?P<pk>[0-9]+)/$', views_api.ConfDetail.as_view()),

    # 网段管理api
    url(r'^network/$', views_api.NetworkList.as_view()),
    url(r'^network/(?P<pk>[0-9]+)/$', views_api.NetworkDetail.as_view()),
    url(r'^ipaddress/$', views_api.IpAddressList.as_view()),
]
