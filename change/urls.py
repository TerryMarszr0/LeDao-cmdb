# -*- coding: utf-8 -*-
from django.conf.urls import url
from change import views

urlpatterns = [

    # 变更查询列表
    url(r'^change/', views.ChangePageView.as_view()),

    # 资源变更列表
    url(r'^reschange/', views.ResChangePageView.as_view()),

]
