#!/usr/bin/python
#-*- coding:utf-8 -*-
# ScriptName: change_hostname.py
# Create Date: 2017-05-10 12:51
# Modify Date: 2017-05-10 12:51
#***************************************************************#
import os, sys, datetime, commands, json

from toolib import *

def changHostname(hn,ip):
    _HN=hn
    _IP=ip

    Logger.action("%s change_hostname:%s" % (_IP, _HN))
    command = 'ssh -o ConnectTimeout=30 %s "hostname %s"'  % (_IP,_HN)
    tmp=commands.getstatusoutput(command)
    if tmp[0]==0:
        command_ck = 'ssh -o ConnectTimeout=30 %s "cat /etc/sysconfig/network | grep "HOSTNAME=" || sed -i \'1 aHOSTNAME=xxx\'  /etc/sysconfig/network"' % _IP
        commands.getstatusoutput(command_ck)
        command = 'ssh -o ConnectTimeout=30 %s "sed -i \'s/HOSTNAME=.*/HOSTNAME=%s/\' /etc/sysconfig/network"'  %(_IP,_HN)
        tmp1 = commands.getstatusoutput(command)
        if tmp1[0]==0:
            command = 'ssh -o ConnectTimeout=30 %s "sed -i \'s/\\(.*\\)%s.*/%s %s/\' /etc/hosts"'  %(_IP,_IP,_IP,_HN)
            tmp3=commands.getstatusoutput(command)
            command_centos7='ssh -o ConnectTimeout=30 %s "if cat /etc/redhat-release | grep \'release 7\';then hostnamectl set-hostname %s;fi"' % (_IP,_HN)
            commands.getstatusoutput(command_centos7)
            if tmp3[0]==0:
                Logger.action("%s change_hostname success" % _IP)
                result={"success": True, "msg": "change ok"}
                print json.dumps(result)
                command_zabbix='ssh -o ConnectTimeout=30 %s "/etc/init.d/zabbix_agentd restart"'   % _IP
                commands.getstatusoutput(command_zabbix)
                commands_rsyslog='ssh -o ConnectTimeout=30 %s "if cat /etc/redhat-release | grep \'release 7\';then systemctl restart  rsyslog;else service rsyslog restart;fi"'   % _IP
                commands.getstatusoutput(commands_rsyslog)
            else:
                Logger.action("%s change_hostname failed" % _IP)
                result={"success": False, "msg": "change hosts failed"}
                print json.dumps(result),
        else:
            Logger.action("%s change_hostname network failed" % _IP)
            result={"success": False, "msg": "change network failed"}
            print json.dumps(result),
    else:
        Logger.action("%s change_hostname ssh failed" % _IP)
        result={"success": False,"msg": "ssh  failed"}
        print json.dumps(result),

if __name__ == '__main__':
    if len(sys.argv) == 3:
        changHostname(sys.argv[1],sys.argv[2])
    else:
        Logger.action("%s change_hostname params not match 3" % _IP)
        result={"success": False}
        print json.dumps(result)
