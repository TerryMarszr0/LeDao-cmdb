# -*- coding: utf-8 -*-
from public.base import PublicView
from asset.models import Room
from host.models import Hosts

class AssetModelPageView(PublicView):
    template_name = 'asset/asset_model.html'


class ConfPageView(PublicView):
    template_name = 'asset/conf.html'

    def get_context_data(self, **kwargs):
        context = super(ConfPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看配置'
        context['path1'] = u'资产管理'
        context['path2'] = u'查看配置'
        return context

class RoomPageView(PublicView):
    template_name = 'asset/room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomPageView, self).get_context_data(**kwargs)
        context['state'] = Room.STATE
        context['header_title'] = u'查看机房'
        context['path1'] = u'资产管理'
        context['path2'] = u'查看机房'
        return context

class NetworkPageView(PublicView):
    template_name = 'asset/network.html'

    def get_context_data(self, **kwargs):
        context = super(NetworkPageView, self).get_context_data(**kwargs)
        context['state'] = Room.STATE
        context['header_title'] = u'查看网段'
        context['path1'] = u'资产管理'
        context['path2'] = u'查看网段'
        context['rooms'] = Room.objects.all()
        context['env'] = Hosts.HOST_ENV_CHOICES
        return context

class IpAddressPageView(PublicView):
    template_name = 'asset/ipaddress.html'

    def get_context_data(self, **kwargs):
        context = super(IpAddressPageView, self).get_context_data(**kwargs)
        context['network_id'] = self.request.GET.get('network_id')
        return context