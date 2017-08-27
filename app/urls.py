# -*- coding: utf-8 -*-
from django.conf.urls import url
from app import views
from app.views import AppsPageView

urlpatterns = [

    # 业务线
    url(r'^group/$', views.GroupPageView.as_view()),

    # 应用管理
    url(r'^app/$', views.AppPageView.as_view(), name='app_app'),

    # 应用资源使用统计
    url(r'^app/stats/$', AppsPageView.as_view()),

    # 服务管理
    url(r'^service/$', views.AppServicePageView.as_view(), name='app_service'),

    # # 应用资源使用统计
    # url(r'^apps/$', views.AppsPageView.as_view()),

    # 服务资源使用统计
    url(r'^service/resource/$', views.ServiceReourcePageView.as_view()),

]
