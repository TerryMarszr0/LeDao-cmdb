# -*- coding: utf-8 -*-
from django.conf.urls import url

from home import views_api

urlpatterns = [

    # api使用手册
    url(r'^apidoc/$', views_api.ApiDocument.as_view()),

]
