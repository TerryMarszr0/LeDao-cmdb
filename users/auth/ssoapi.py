# -*- coding: utf-8 -*-

import json, requests
from cmdb import configs

# {"status":0,"msg":"登录成功","name":"陈绍东","phone":15921777942,"departmentId":860,"departmentName":"系统运维组","email":"chen.shaodong@puscene.com","employeNumber":"12088"}
def login_sso(userName, password):
    try:
        response = requests.post(configs.AUTH_URL, data=json.dumps({'userName': userName, 'password': password}), headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            return False, response.text
        userinfo = json.loads(response.text)
        if userinfo['data']['status'] != 0:
            return False, 'fail!'
        return True, userinfo['data']
    except Exception, ex:
        print str(ex)
        return False, str(ex)

def get_token(tokenKey):
    try:
        response = requests.get(configs.TOKEN_URL + tokenKey + '/', params={}, headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            return False, response.text
        userinfo = json.loads(response.text)
        return True, userinfo
    except Exception, ex:
        print str(ex)
        return False, str(ex)