# -*- coding: utf-8 -*-
import time, json, sys
from public.models import AsyncTask
from cmdb.configs import logger
from public.redis.mq import Q
from django.forms.models import model_to_dict
from cmdb import configs

class Task():

    queue_key = configs.CMDB_TASK

    def excute(self, **kwargs):
        return True, 'succ!'

    def addTask(self, crate_user, **kwargs):
        task = AsyncTask.objects.create(task=str(self.__class__), params=json.dumps(kwargs), state='ready', ctime=int(time.time()), cuser=crate_user)
        q = Q(self.queue_key)
        q.push(json.dumps(model_to_dict(task)))

    def run(self, task_id=0, **kwargs):
        AsyncTask.objects.filter(id=task_id).update(start_time=int(time.time()), state='running')
        try:
            res, data = self.excute(**kwargs)
            state = 'failure'
            if res:
               state = 'success'
            AsyncTask.objects.filter(id=task_id).update(state=state, result=data, finish_time=int(time.time()))
        except Exception, ex:
            AsyncTask.objects.filter(id=task_id).update(state='failure', result=str(ex))
            logger.error("task " + str(task_id) + ":" + str(ex))