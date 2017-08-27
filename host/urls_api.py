# -*- coding: utf-8 -*-
from django.conf.urls import url
from host import views_api

urlpatterns = [

    # 主机api
    url(r'^host/$', views_api.HostsList.as_view()),
    url(r'^host/(?P<pk>[0-9]+)/$', views_api.HostsDetail.as_view()),
    url(r'^servicehost/$', views_api.ServiceHostsList.as_view()),
    url(r'^upload/$', views_api.HostsUpload.as_view()),
    url(r'^syncaliyun/$', views_api.SyncAliyun.as_view()),
    url(r'^updatefromaliyun/$', views_api.UpdateFromAliyun.as_view()),

    url(r'^addaliyun/$', views_api.AddAliyunInstance.as_view()),

    # 修改主机状态api
    url(r'^changestate/$', views_api.ChangeHostState.as_view()),

    # 修改主机所属服务
    url(r'^changeservice/$', views_api.ChangeHostService.as_view()),

    # 主机挂载
    url(r'^mount/$', views_api.MountHostService.as_view()),

    # 修改主名api
    url(r'^changehostname/$', views_api.ChangeHostName.as_view()),

    # 查询/修改主密码api
    url(r'^password/$', views_api.HostPasswordApi.as_view()),

    # 系统镜像api
    url(r'^image/$', views_api.ImageList.as_view()),
    url(r'^image/(?P<pk>[0-9]+)/$', views_api.ImageDetail.as_view()),

    # 通过 ansible 读取主机信息并保存
    url(r'^info/$', views_api.HostInfoByAnsibleApi.as_view()),

]
