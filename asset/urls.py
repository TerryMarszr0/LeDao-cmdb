# -*- coding: utf-8 -*-
from django.conf.urls import url
from asset import views

urlpatterns = [

    # 设备型号
    url(r'^model/$', views.AssetModelPageView.as_view()),

    # 设备配置
    url(r'^conf/$', views.ConfPageView.as_view()),

    # 机房管理
    url(r'^room/$', views.RoomPageView.as_view(), name='room'),

    # 网段管理
    url(r'^network/$', views.NetworkPageView.as_view()),
    url(r'^ipaddress/$', views.IpAddressPageView.as_view()),

]
