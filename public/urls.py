# -*- coding: utf-8 -*-
from django.conf.urls import url
from public import views

urlpatterns = [

    # 异步任务
    url(r'^task/$', views.TaskPageView.as_view()),

]
