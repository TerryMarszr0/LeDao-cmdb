# -*- coding: utf-8 -*-
from django.conf.urls import url
from fortress import views_api

urlpatterns = [

    # 用户授权主机列表
    url(r'^userhost/$', views_api.UserAuthRecordList.as_view()),

    # 授权列表
    url(r'^authrecord/$', views_api.AuthRecordList.as_view()),
    url(r'^authrecord/(?P<pk>[0-9]+)/$', views_api.AuthRecordDetail.as_view()),

    # 授权申请列表
    url(r'^applyrecord/$', views_api.ApplyRecordList.as_view()),
    url(r'^applyrecord/(?P<pk>[0-9]+)/$', views_api.ApplyRecordDetail.as_view()),

    # 我的授权申请列表
    url(r'^myapply/$', views_api.MyApplyRecordList.as_view()),

    # 授权申请详情列表
    url(r'^applytask/$', views_api.ApplyTaskList.as_view()),

    # 修改授权申请状态
    url(r'^changeapplystate/$', views_api.ChangeApplyState.as_view()),

    # 我的ssh key
    url(r'^mysshkey/$', views_api.MySSHKey.as_view()),

    # 我的ssh key
    url(r'^downloadkey/$', views_api.DownloadSSHKey.as_view()),

    # 创建ssh key
    url(r'^createmykey/$', views_api.CreateMySSHKey.as_view()),
]
