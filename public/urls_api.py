# -*- coding: utf-8 -*-
from django.conf.urls import url
from public import views_api

urlpatterns = [

    # 异步任务
    url(r'^task/$', views_api.TaskList.as_view()),

    # 重做异步任务
    url(r'^redotask/$', views_api.RedoTask.as_view()),

    # 全局搜索
    url(r'^quicksearch/$', views_api.QuickSearchList.as_view()),

    # git仓库地址
    url(r'^gitrepo/$', views_api.GitList.as_view()),


]
