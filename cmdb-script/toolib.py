#!/usr/bin/python
#-*- coding:utf-8 -*-
# ScriptName: toolib.py
# Create Date: 2017-05-05 13:08
# Modify Date: 2017-05-05 13:08
#***************************************************************#
import os, time

LOG_DIR = "/var/log/cmdb-script/"

class Logger(object):

    def __init__(self):
        print "in Logger"

    @classmethod
    def warning(cls, message):
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now=time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
        try:
            log_file = LOG_DIR+"/warning.log"
            file_object = open(log_file, 'a+')
            file_object.write(now + " " + str(message) + "\n")
            file_object.close()
        except Exception, e:
            return False
        return True
    
    @classmethod
    def action(cls, message):
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now=time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
        try:
            log_file = LOG_DIR+"/action.log"
            file_object = open(log_file, 'a+')
            file_object.write(now + " " + str(message) + "\n")
            file_object.close()
        except Exception, e:
            return False
        return True
