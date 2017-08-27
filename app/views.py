# -*- coding: utf-8 -*-

from app.models import AppService, App
from asset.models import Room
from public.base import PublicView


# class AppPermissionPageView(PublicView):
#     template_name = 'app/app_permission.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         result = super(AppPermissionPageView, self).dispatch(request, *args, **kwargs)
#         return result
#
#     def get_context_data(self, **kwargs):
#         context = super(AppPermissionPageView, self).get_context_data(**kwargs)
#         app_id = self.request.GET.get("app_id", 0)
#         context['app_id'] = app_id
#         return context


class GroupPageView(PublicView):
    template_name = 'app/group.html'

    def get_context_data(self, **kwargs):
        context = super(GroupPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看业务线'
        context['path1'] = u'应用管理'
        context['path2'] = u'查看业务线'
        return context

class AppPageView(PublicView):
    template_name = 'app/app.html'

    def get_context_data(self, **kwargs):
        context = super(AppPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看应用'
        context['path1'] = u'应用管理'
        context['path2'] = u'查看应用'
        context['group'] = self.request.GET.get('group', '')
        return context

class AppServicePageView(PublicView):
    template_name = 'app/app_service.html'

    def get_context_data(self, **kwargs):
        context = super(AppServicePageView, self).get_context_data(**kwargs)
        context['state'] = Room.STATE
        context['header_title'] = u'查看服务'
        context['path1'] = u'应用管理'
        context['path2'] = u'查看服务'
        context['lines'] = App.objects.all()
        context['types'] = AppService.TYPE
        app_id = self.request.GET.get("app_id", '')
        context['app_id'] = app_id
        context['state'] = AppService.STATE
        return context

# 应用资源统计
class AppsPageView(PublicView):
    template_name = 'app/apps.html'

    def get_context_data(self, **kwargs):
        context = super(AppsPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看应用'
        context['path1'] = u'服务管理'
        context['path2'] = u'查看应用'
        app_id = self.request.GET.get("id", '')
        context['app_name'] = u"应用名称：" + App.objects.get(id=app_id).name
        return context

# 服务资源统计
class ServiceReourcePageView(PublicView):
    template_name = 'app/service_source.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceReourcePageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看服务'
        context['path1'] = u'服务管理'
        context['path2'] = u'查看服务'
        service_id = self.request.GET.get("id", '')
        context['service_name'] = u"服务名称：" + AppService.objects.get(id=service_id).name
        return context



