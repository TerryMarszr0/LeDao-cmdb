# -*- coding: utf-8 -*-
from public.base import PublicView
from fortress.models import AuthRecord, ApplyRecord

class AuthRecordView(PublicView):
    template_name = 'fortress/auth_record.html'

    def get_context_data(self, **kwargs):
        context = super(AuthRecordView, self).get_context_data(**kwargs)
        context['header_title'] = u'授权查询'
        context['path1'] = u'堡垒机管理'
        context['path2'] = u'授权查询'
        return context


class MyApplyView(PublicView):
    template_name = 'fortress/my_apply.html'

    def get_context_data(self, **kwargs):
        context = super(MyApplyView, self).get_context_data(**kwargs)
        context['header_title'] = u'我的申请记录'
        context['path1'] = u'堡垒机管理'
        context['path2'] = u'我的授权申请'
        context['roles'] = AuthRecord.ROLE_CHOICES
        context['states'] = ApplyRecord.STATE_CHOICES
        return context

class ApplyDetailView(PublicView):
    template_name = 'fortress/apply_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ApplyDetailView, self).get_context_data(**kwargs)
        context['apply_id'] = self.request.GET.get('apply_id', 0)
        return context

class AuditView(PublicView):
    template_name = 'fortress/audit.html'

    def get_context_data(self, **kwargs):
        context = super(AuditView, self).get_context_data(**kwargs)
        context['header_title'] = u'授权审批'
        context['path1'] = u'堡垒机管理'
        context['path2'] = u'授权审批'
        context['states'] = ApplyRecord.STATE_CHOICES
        return context

class ApplyRecordView(PublicView):
    template_name = 'fortress/apply_list.html'

    def get_context_data(self, **kwargs):
        context = super(ApplyRecordView, self).get_context_data(**kwargs)
        context['header_title'] = u'授权记录'
        context['path1'] = u'堡垒机管理'
        context['path2'] = u'授权记录'
        context['states'] = ApplyRecord.STATE_CHOICES
        return context

class MyAuthRecordView(PublicView):
    template_name = 'fortress/my_auth.html'

    def get_context_data(self, **kwargs):
        context = super(MyAuthRecordView, self).get_context_data(**kwargs)
        context['header_title'] = u'我的授权'
        context['path1'] = u'堡垒机管理'
        context['path2'] = u'我的授权'
        context['states'] = ApplyRecord.STATE_CHOICES
        context['username'] = self.request.user.username
        if not self.request.user.username:
            context['username'] = '-1'
        return context