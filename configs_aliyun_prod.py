# -*- coding: utf-8 -*-

import os, logging
logger = logging.getLogger('cmdb')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

########################## db ##########################
DB_NAME = "mwcmdb"
DB_USER = "mwcmdb"
DB_PASSWORD = "mw$%GTs89d"
DB_HOST = "10.1.28.179"
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
ZABBIX_USER = "zabbixapi"
ZABBIX_PASSWORD = "RJ45^8#fe@pnd"

########################## zabbix ##########################

########################## fortress host ##########################

FORTRESS_HOST = "10.1.20.97"

REMOTE_CMDB_DIR = "/opt/cmdb-script/"
########################## fortress host ##########################


########################## sso ##########################

AUTH_URL = "http://sso.mwbyd.cn/services/sso/login"

TOKEN_URL = "http://ssoops.mwbyd.cn/api/home/token/"

LOGIN_URL = "http://ssoops.mwbyd.cn/sso/login/"

CALLBACK_URL = "/home/ssologin/"

########################## sso ##########################

########################## auto ##########################

AUTO_DOMAIN = "http://auto.mwbyd.cn"

AUTO_TOKEN = "3066c0ad-75aa-4934-a7e4-7a32e6392748-b7"

########################## auto ##########################

########################## gitlab ##########################

GITLAB_TOKEN = "9yTv6xhN9VhdLjzoh3xm"

GITLAB_DOMAIN = "http://gitlab.mwbyd.cn:10080"

########################## gitlab ##########################

########################## 工单系统 ##########################

TICKET_URL = "http://ticket.mwbyd.cn"

########################## 工单系统 ##########################

REDIS_HOST = '10.1.20.91'

CMDB_TASK = "cmdb_task"

ZABBIX_TASK = "zabbix_task"

OPS_EMAIL = "group.yunwei@puscene.com"

AES_KEY = "KJ8&*(ji09%^&3zn"

DEBUG = False

CMDB_VERSION = "0.1.1"

RUN_ENV = 'prod'
