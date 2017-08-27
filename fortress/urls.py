# -*- coding: utf-8 -*-
from django.conf.urls import url
from fortress import views

urlpatterns = [

    # 授权记录
    url(r'^authrecord/$', views.AuthRecordView.as_view()),

    # 我的授权主机
    url(r'^myauthrecord/$', views.MyAuthRecordView.as_view()),

    # 授权申请
    url(r'^myapply/$', views.MyApplyView.as_view()),

    # 授权申请详情
    url(r'^applydetail/$', views.ApplyDetailView.as_view()),

    # 授权审批
    url(r'^audit/$', views.AuditView.as_view()),

    # 授权审批
    url(r'^audit/applyrecord/$', views.ApplyRecordView.as_view()),
]
