# -*- coding: utf-8 -*-
from django.conf.urls import url
from dashboard import views

urlpatterns = [

    # 服务器统计
    url(r'^servers/$', views.ServersPageView.as_view()),

]
