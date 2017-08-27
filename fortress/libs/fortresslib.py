# -*- coding: utf-8 -*-

from cmdb import configs
from cmdb.configs import logger
import os, json, commands, time
from hashlib import md5
from django.core.mail import send_mail
from paramiko.rsakey import RSAKey
import StringIO
from fortress.models import SSHKey


class FortressOps():

    def addFortressUser(self, username, email):
        m = md5()
        m.update(username + str(time.time()))
        password = m.hexdigest()[0:20]
        command = 'ssh root@%s -o ConnectTimeout=2 "/bin/sh %s/fortress/create.sh %s %s"' % (configs.FORTRESS_HOST, configs.REMOTE_CMDB_DIR, username, password)
        logger.info(command)
        try:
            status, output = commands.getstatusoutput(command)
            if status != 0:
                logger.error(output)
                return False, output
            logger.info(output)
            content = u'已为你开通堡垒机账号<br/>用户名为:' + username + u'<br/>密码为:' + password + u"<br/>堡垒机使用方式见:http://wiki.mwbyd.cn/pages/viewpage.action?pageId=6334750<br/>" \
                      + u"如有疑问请联系陈绍东,邮箱:chen.shaodong@puscene.com,手机号:15921777942"
            send_mail(u'堡垒机开通通知', '', configs.EMAIL_USER, [email], html_message=content)
            return True, output
        except Exception, e:
            logger.error(str(e))
            return False, str(e)

    def addUserKey(self, ip, role, username):
        command = 'ssh root@%s -o ConnectTimeout=2 "/usr/bin/python %s/auth.ssh_key.py add %s %s %s"' % (configs.FORTRESS_HOST, configs.REMOTE_CMDB_DIR, ip, role, username)
        logger.info(command)
        try:
            status, output = commands.getstatusoutput(command)
            if status != 0:
                logger.error(output)
                return False, output
            logger.info(output)
            result_dict = json.loads(output)[0]
            if result_dict['success'] == "true":
                return True, result_dict['msg']
            return False, result_dict['msg']
        except Exception, e:
            logger.error("add user key:" + str(e))
            return False, str(e)

    def delUserKey(self, ip, role, username):
        command = 'ssh root@%s -o ConnectTimeout=2 "/usr/bin/python %s/auth.ssh_key.py del %s %s %s"' % (configs.FORTRESS_HOST, configs.REMOTE_CMDB_DIR, ip, role, username)
        logger.info(command)
        try:
            status, output = commands.getstatusoutput(command)
            if status != 0:
                logger.error(output)
                return False, output
            logger.info(output)
            result_dict = json.loads(output)[0]
            if result_dict['success'] == "true":
                return True, result_dict['msg']
            return False, result_dict['msg']
        except Exception, e:
            logger.error("add user key:" + str(e))
            return False, str(e)

    def getGoogleKey(self, username):
        command = 'ssh root@%s -o ConnectTimeout=2 "head -n 1 /home/%s/.google_authenticator"' % (configs.FORTRESS_HOST, username)
        try:
            status, output = commands.getstatusoutput(command)
            if status != 0:
                logger.error(output)
                return False, output
            return True, output
        except Exception, e:
            logger.error(str(e))
            return False, str(e)

    def addSSHKey(self, username, ssh_key):
        command = 'ssh root@%s -o ConnectTimeout=2 "echo %s > /home/%s/.ssh/authorized_keys"' % (configs.FORTRESS_HOST, ssh_key, username)
        try:
            status, output = commands.getstatusoutput(command)
            if status != 0:
                logger.error(output)
                return False, output
            return True, output
        except Exception, e:
            logger.error(str(e))
            return False, str(e)


def gen_keys(emial, key=""):
    """
    生成公钥 私钥
    """
    output = StringIO.StringIO()
    sbuffer = StringIO.StringIO()
    key_content = {}
    if not key:
        try:
            key = RSAKey.generate(2048)
            key.write_private_key(output)
            private_key = output.getvalue()
        except Exception, ex:
            return False, str(ex)
    else:
        private_key = key
        output.write(key)
        try:
            key = RSAKey.from_private_key(output)
        except Exception, e:
            return False, str(e)

    for data in [key.get_name(),
                 " ",
                 key.get_base64(),
                 " %s@%s" % ("magicstack", os.uname()[1])]:
        sbuffer.write(data)
    public_key = sbuffer.getvalue()
    public_key_arr = public_key.split(" ")
    public_key_arr[-1] = emial
    key_content['public_key'] = " ".join(public_key_arr)
    key_content['private_key'] = private_key
    return True, key_content

def create_ssh_key(email, user_id, username):
    status, result = gen_keys(email)
    if not status:
        return False, result
    ssh_key = result['public_key']
    private_key = result['private_key']
    SSHKey.objects.filter(user_id=user_id).delete()
    u = SSHKey.objects.create(user_id=user_id, ssh_key=ssh_key, private_key=private_key)
    status, output = FortressOps().addSSHKey(username, ssh_key)
    if not status:
        return False, output
    return True, u

def rsync_fortress():
    command = 'ssh root@%s -o ConnectTimeout=5 "python /opt/cmdb-script/rsync_backup.py"' % (configs.FORTRESS_HOST, )
    try:
        status, output = commands.getstatusoutput(command)
        if status != 0:
            logger.error(output)
            return False, output
        logger.info(output)
        return True, output
    except Exception, e:
        logger.error(str(e))
        return False, str(e)

