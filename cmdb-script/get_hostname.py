#!/usr/bin/python
#-*- coding:utf-8 -*-
# ScriptName: get_hostname.py
# Create Date: 2017-05-19 11:03
# Modify Date: 2017-05-19 11:03
#***************************************************************#
import os, sys, commands, json
import logging

logging.basicConfig(filename='/var/log/cmdb-script/cmdb_agent.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def getHostname(ip):
    command = 'ssh root@%s -o ConnectTimeout=10 "hostname"' % (ip)
    try:
        status, output = commands.getstatusoutput(command)
        return status, output.split("\n")[-1]
    except Exception, ex:
        logging.info(str(ex))
        return -1, str(ex)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        status, output = getHostname(sys.argv[1])
        if status != 0:
            print output
            exit(-1)
        print output
        exit(0)
    else:
        logging.info('params error')
        print 'params error'
        exit(-2)