#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import json

# url = "http://cmdb.mwbyd.cn/api/lb/changeServiceHostState/"
# token = "ea9d9d56cdcf6641189f7d41b0ff23425f0e51a3"
url = "http://test.cmdb.mwbyd.cn/api/lb/changeServiceHostState/"
token = "d233e72a509e466fe2068af8e5371d89d5a68d5d"

def change_state(service_name, ip, state):
    params = {"service_name": service_name, 'ip': ip,  "state": state}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Token %s' % token}
    response = requests.patch(url, data=params, headers=headers)
    if response.status_code not in (200, 201):
        return False, response.text
    return True, 'succ!'


if __name__ == "__main__":
    service_name = sys.argv[1]
    ip = sys.argv[2]
    state = sys.argv[3]
    status, data = change_state(service_name, ip, state)
    if not status:
        print data
        exit(500)
    print "MW_SUCCESS"