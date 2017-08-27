# -*- coding: utf-8 -*-
from public.base import PublicView
from public.models import AsyncTask

# Create your views here.

class TaskPageView(PublicView):
    template_name = 'public/task.html'

    def get_context_data(self, **kwargs):
        context = super(TaskPageView, self).get_context_data(**kwargs)
        context['header_title'] = u'查看异步任务'
        context['path1'] = u'任务管理'
        context['path2'] = u'异步任务'
        context['state'] = AsyncTask.TASK_STATE
        return context
