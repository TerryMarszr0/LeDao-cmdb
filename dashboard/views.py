# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from app.models import AppService, App
from public.base import PublicView


class ServersPageView(PublicView):
    template_name = 'dashboard/servers.html'

    def get_context_data(self, **kwargs):
        context = super(ServersPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'DashBoard'
        context['path1'] = u'服务器统计'
        context['path2'] = u'DashBoard'
        return context
# Create your views here.
