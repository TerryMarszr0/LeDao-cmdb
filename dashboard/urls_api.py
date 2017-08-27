# -*- coding: utf-8 -*-
from django.conf.urls import url
from dashboard import views_api

urlpatterns = [

    # 服务器管理 api
    url(r'^servers/$', views_api.ServersStatistics.as_view()),

]
