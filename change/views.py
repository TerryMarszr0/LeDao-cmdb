# -*- coding: utf-8 -*-
from public.base import PublicView
from change.models import Change

class ChangePageView(PublicView):
    template_name = 'change/change.html'

    def get_context_data(self, **kwargs):
        context = super(ChangePageView, self).get_context_data(**kwargs)
        context['actions'] = Change.ACTION
        return context

class ResChangePageView(PublicView):
    template_name = 'change/res_change.html'

    def get_context_data(self, **kwargs):
        context = super(ResChangePageView, self).get_context_data(**kwargs)
        context['resource'] = self.request.GET.get("resource", None)
        context['res_id'] = self.request.GET.get("res_id", 0)
        return context

