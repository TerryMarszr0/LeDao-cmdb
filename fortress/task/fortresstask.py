# -*- coding: utf-8 -*-

from public.task.taskbase import Task
from fortress.libs.fortresslib import FortressOps, create_ssh_key, rsync_fortress
from cmdb.configs import logger
from fortress.models import ApplyTask
import time
from django.contrib.auth.models import User


class AddFortressUserTask(Task):

    def excute(self, **kwargs):
        username = kwargs.get('username', '')
        email = kwargs.get('email', '')
        users = User.objects.filter(username=username)
        if len(users) <= 0:
            return False, u'用户不存在'
        user = users[0]
        state, msg = FortressOps().addFortressUser(username, email)
        # 添加用户成功,则生成ssh免密密钥对
        if state:
            create_ssh_key(email, user.id, username)
        logger.info("task:" + msg)

        # 同步堡垒机数据
        rsync_fortress()
        return state, msg

class AddUserKeyTask(Task):

    def excute(self, **kwargs):
        ip = kwargs.get('ip', '')
        role = kwargs.get('role', '')
        username = kwargs.get('username', '')
        status, result = FortressOps().addUserKey(ip, role, username)

        # 同步堡垒机数据
        rsync_fortress()
        return status, result

class ApplyTaskAddUserKeyTask(Task):

    def excute(self, **kwargs):
        applytask_id = kwargs.get('applytask_id', 0)
        ApplyTask.objects.filter(id=applytask_id).update(state='running', run_time=int(time.time()))
        ip = kwargs.get('ip', '')
        role = kwargs.get('role', '')
        username = kwargs.get('username', '')
        status, result = FortressOps().addUserKey(ip, role, username)
        state = 'success'
        if not status:
            state = 'failure'
        ApplyTask.objects.filter(id=applytask_id).update(state=state, result=result, finish_time=int(time.time()))

        # 同步堡垒机数据
        rsync_fortress()
        return status, result

class DelUserKeyTask(Task):

    def excute(self, **kwargs):
        ip = kwargs.get('ip', '')
        role = kwargs.get('role', '')
        username = kwargs.get('username', '')

        # 同步堡垒机数据
        rsync_fortress()
        return FortressOps().delUserKey(ip, role, username)