# -*- coding: utf-8 -*-
from django.conf.urls import url
from lb import views_api

urlpatterns = [

    # 负载均衡api
    url(r'^lb/$', views_api.LBList.as_view()),
    url(r'^lb/(?P<pk>[0-9]+)/$', views_api.LBDetail.as_view()),
    url(r'^servicelb/$', views_api.ServiceLBList.as_view()),
    url(r'^servicelb/(?P<pk>[0-9]+)/$', views_api.ServiceLBDetail.as_view()),

    url(r'^lbhosts/$', views_api.DomainLBHostList.as_view()),

    url(r'^nginxconf/(?P<service_name>.*)/$', views_api.NginxConf.as_view()),
    url(r'^changeServiceHostState/$', views_api.ChangeServiceHostState.as_view()),

    url(r'^pushNginxConfig/$', views_api.PushNginxConfig.as_view()),
]
