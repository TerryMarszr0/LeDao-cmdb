# -*- coding: utf-8 -*-
from public.base import PublicView
from host.models import Hosts, Image
from asset.models import Room, AssetModel, Conf
from lb.models import ServiceLB
from host.models import Hosts

from django.forms.models import model_to_dict

# Create your views here.


class SLBPageView(PublicView):
    template_name = 'lb/slb.html'

    def get_context_data(self, **kwargs):
        context = super(SLBPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看负载均衡'
        context['path1'] = u'负载均衡管理'
        context['path2'] = u'查看负载均衡'
        context['rooms'] = Room.objects.all()
        context['env'] = Hosts.HOST_ENV_CHOICES
        return context

class LBListView(PublicView):
    template_name = 'lb/lblist.html'

    def get_context_data(self , **kwargs):
        context = super(LBListView , self).get_context_data(**kwargs)
        context['header_title'] = u'查看负载均衡器'
        context['path1'] = u'负载均衡器管理'
        context['path2'] = u'查看负载均衡器'
        context['env'] = Hosts.HOST_ENV_CHOICES
        return context

class LocationListView(PublicView):
    template_name = 'lb/location.html'

    def get_context_data(self , **kwargs):
        context = super(LocationListView , self).get_context_data(**kwargs)
        context['header_title'] = u'查看location'
        context['path1'] = u'负载均衡器管理'
        context['path2'] = u'查看location'
        context['types'] = ServiceLB.UPSTREAM_TYPE_CHOICES
        return context



class ServiceLocationView(PublicView):
    template_name = 'lb/service_location.html'

    def get_context_data(self , **kwargs):
        service_id = self.request.GET.get('service_id', 0)
        context = super(ServiceLocationView , self).get_context_data(**kwargs)
        context['types'] = ServiceLB.UPSTREAM_TYPE_CHOICES
        context['env'] = Hosts.HOST_ENV_CHOICES
        context['service_id'] = service_id
        return context




class ShowConf(PublicView):
    template_name = 'lb/showconf.html'

    def get_context_data(self , **kwargs):
        context = super(ShowConf , self).get_context_data(**kwargs)
        context['header_title'] = u'查看负载均衡器'
        context['path1'] = u'负载均衡器管理'
        context['path2'] = u'查看负载均衡器'
        context['lb_id'] = self.request.GET.get("id")
        return context