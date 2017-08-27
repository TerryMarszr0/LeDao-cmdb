# -*- coding: utf-8 -*-
from cmdb import configs
from cmdb.configs import logger
import requests, json

class AutoApi():

    def addProject(self, projectName, code, description):
        params = {}
        params['token'] = configs.AUTO_TOKEN
        params['code'] = code
        params['projectName'] = projectName
        if description:
            params['description'] = description
        try:
            response = requests.post(configs.AUTO_DOMAIN + '/gateway/project/addProject', data=json.dumps(params), headers={"Content-Type": "application/json"})
            data = json.loads(response.text)
            if data['statusCode'] == '200':
                return True, 'succ'
            logger.error(response.text)
            return False, data['msg']
        except Exception, ex:
            logger.error(str(ex))
            return False, str(ex)

    def updateProject(self, projectNameOld, projectName, code, description):
        params = {}
        params['token'] = configs.AUTO_TOKEN
        params['code'] = code
        params['projectName'] = projectName
        params['projectNameOld'] = projectNameOld
        if description:
            params['description'] = description
        try:
            response = requests.post(configs.AUTO_DOMAIN + '/gateway/project/updateProject', data=json.dumps(params), headers={"Content-Type": "application/json"})
            data = json.loads(response.text)
            if data['statusCode'] == '200':
                return True, 'succ'
            logger.error(response.text)
            return False, data['msg']
        except Exception, ex:
            logger.error(str(ex))
            return False, str(ex)

    def addTemplate(self, name, projectName, cmdbServiceName, cmdbServiceId, vcsRep, normalType, vcsType='git', review=0):
        params = {}
        params['token'] = configs.AUTO_TOKEN
        params['name'] = name
        params['projectName'] = projectName
        params['cmdbServiceName'] = cmdbServiceName
        params['cmdbServiceId'] = cmdbServiceId
        params['vcsRep'] = vcsRep
        params['vcsType'] = vcsType
        params['review'] = review
        if normalType:
            params['normalType'] = normalType
        try:
            response = requests.post(configs.AUTO_DOMAIN + '/gateway/template/addTemplate', data=json.dumps(params), headers={"Content-Type": "application/json"})
            data = json.loads(response.text)
            if data['statusCode'] == '200':
                return True, 'succ'
            logger.error(response.text)
            return False, data['msg']
        except Exception, ex:
            logger.error(str(ex))
            return False, str(ex)

    def updateTemplate(self, name, projectName, cmdbServiceName, cmdbServiceId, vcsRep, vcsType='git', review=0):
        params = {}
        params['token'] = configs.AUTO_TOKEN
        params['name'] = name
        params['projectName'] = projectName
        params['cmdbServiceName'] = cmdbServiceName
        params['cmdbServiceId'] = cmdbServiceId
        if vcsRep:
            params['vcsRep'] = vcsRep
        params['vcsType'] = vcsType
        params['review'] = review
        try:
            response = requests.post(configs.AUTO_DOMAIN + '/gateway/template/modifyTemplate', data=json.dumps(params), headers={"Content-Type": "application/json"})
            data = json.loads(response.text)
            if data['statusCode'] == '200':
                return True, 'succ'
            logger.error(response.text)
            return False, data['msg']
        except Exception, ex:
            logger.error(str(ex))
            return False, str(ex)

class GitLabApi():

    headers = {"PRIVATE-TOKEN": configs.GITLAB_TOKEN}
    params = {}

    def getProjects(self, page, per_page):
        self.params['page'] = page
        self.params['per_page'] = per_page
        try:
            response = requests.get(configs.GITLAB_DOMAIN + '/api/v3/projects', params=self.params, headers=self.headers)
            data = response.json()
            # data = json.loads(response.text)
            return True, data
        except Exception, ex:
            logger.error(str(ex))
            return False, str(ex)
