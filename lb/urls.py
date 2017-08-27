# -*- coding: utf-8 -*-
from django.conf.urls import url
from lb import views

urlpatterns = [

    # 负载均衡
    url(r'^slb/$', views.SLBPageView.as_view()),
    url(r'^lblist/$', views.LBListView.as_view()),
    url(r'^locationlist/$', views.LocationListView.as_view()),
    url(r'^lbservice/$', views.ServiceLocationView.as_view()),
    url(r'^showconf/$', views.ShowConf.as_view()),

]
