# -*- coding: utf-8 -*-

import os, logging
logger = logging.getLogger('cmdb')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

########################## db ##########################
DB_NAME = "mwcmdb"
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
########################## db ##########################

########################## EMAIL ##########################
ENABLE = 1
EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 25
EMAIL_USER = "ops@puscene.com"
EMAIL_PASSWORD = "CM!34#j&i5b*"
EMAIL_TLS = False
EMAIL_SSL = False
########################## EMAIL ##########################

########################## resource pool ##########################

RESOURCE_POOL_ID = 1
FREE_SERVER_ID = 1
FREE_VM_ID = 2
FREE_ALIYUN_ID = 3
FREE_UNUSE = 4

########################## resource pool ##########################

########################## zabbix ##########################

ZABBIX_API_URL = "http://alizabbix.mwbyd.cn/api_jsonrpc.php"
ZABBIX_IDC_API_URL = "http://zabbix.mwbyd.cn/zabbix/api_jsonrpc.php"
ZABBIX_USER = "admin"
ZABBIX_PASSWORD = "admin"

########################## zabbix ##########################

########################## fortress host ##########################

FORTRESS_HOST = "10.0.20.24"

REMOTE_CMDB_DIR = "/opt/cmdb-script/"
########################## fortress host ##########################


########################## sso ##########################

AUTH_URL = "http://sso.mwbyd.cn/services/sso/login"

TOKEN_URL = "http://ssoops.mwbyd.cn/api/home/token/"

LOGIN_URL = "http://ssoops.mwbyd.cn/sso/login/"

CALLBACK_URL = "/home/ssologin/"

########################## sso ##########################

########################## auto ##########################

AUTO_DOMAIN = "http://auto.9now.net"

AUTO_TOKEN = "74a7e825-3234-45b6-8306-e5b61a9214ec-1"

########################## auto ##########################

########################## gitlab ##########################

GITLAB_TOKEN = "9yTv6xhN9VhdLjzoh3xm"

GITLAB_DOMAIN = "http://gitlab.mwbyd.cn:10080"

########################## gitlab ##########################

########################## 工单系统 ##########################

TICKET_URL = "http://test.ticket.mwbyd.cn"

########################## 工单系统 ##########################

REDIS_HOST = '127.0.0.1'

CMDB_TASK = "cmdb_task"

ZABBIX_TASK = "zabbix_task"

OPS_EMAIL = "chen.shaodong@puscene.com"

AES_KEY = "hKDJ$89UJ2zO)I*j"

DEBUG = True

CMDB_VERSION = "0.1.1"

RUN_ENV = 'test'
