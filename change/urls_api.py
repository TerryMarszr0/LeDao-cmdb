# -*- coding: utf-8 -*-
from django.conf.urls import url
from change import views_api

urlpatterns = [

    # 变更记录api
    url(r'^change/$', views_api.ChangeList.as_view()),
    url(r'^change/(?P<pk>[0-9]+)/$', views_api.ChangeDetail.as_view()),

]
