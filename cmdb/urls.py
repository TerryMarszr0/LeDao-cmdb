"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework import routers
from django.contrib import admin
from rest_framework.authtoken import views
from home.views import index_view, LoginPageView, SkinConfigView
from home import views_api
from public.views_api import Redirect
admin.autodiscover()

router = routers.DefaultRouter()

urlpatterns = [

    ########################## api url config ##########################
    # url(r'/', include(router.urls)),

    url(r'^api/$', views_api.ApiDocument.as_view()),

    url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/admin/', include(admin.site.urls)),

    url(r'^api/tokenauth/', views_api.ObtainAuthToken.as_view()),

    url(r'^api/app/', include('app.urls_api')),

    url(r'^api/asset/', include('asset.urls_api')),

    url(r'^api/host/', include('host.urls_api')),

    url(r'^api/user/', include('users.urls_api')),

    url(r'^api/change/', include('change.urls_api')),

    url(r'^api/lb/', include('lb.urls_api')),

    url(r'^api/home/', include('home.urls_api')),

    url(r'^api/fortress/', include('fortress.urls_api')),

    url(r'^api/public/', include('public.urls_api')),

    url(r'^api/dashboard/', include('dashboard.urls_api')),

    url(r'^api/orange/redirect/', Redirect.as_view()),

    ########################## api url config ##########################


    ########################## site url config ##########################

    url(r'^$', index_view),

    url(r'^login/$', LoginPageView.as_view()),

    url(r'^home/', include('home.urls')),

    url(r'^app/', include('app.urls')),

    url(r'^host/', include('host.urls')),

    url(r'^asset/', include('asset.urls')),

    url(r'^skin_config/', SkinConfigView.as_view(), name='skin_config'),

    url(r'^user/', include('users.urls')),

    url(r'^change/', include('change.urls')),

    url(r'^lb/', include('lb.urls')),

    url(r'^fortress/', include('fortress.urls')),

    url(r'^public/', include('public.urls')),

    url(r'^dashboard/', include('dashboard.urls')),

    ########################## site url config ##########################
]