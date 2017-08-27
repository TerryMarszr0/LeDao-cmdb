# -*- coding: utf-8 -*-
from django.conf.urls import url
from home import views

urlpatterns = [

    url(r'^$', views.IndexPageView.as_view(), name='index'),

    url(r'^login', views.LoginPageView.as_view(), name='login'),

    url(r'^dologin', views.doLogin, name='dologin'),

    url(r'^ssologin/$', views.sso_login),

    url(r'^logout', views.logout, name='logout'),

    url(r'^logout', views.logout),

    url(r'^healthcheck', views.healthCheck, name='healthcheck'),

]
