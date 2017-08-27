# -*- coding: utf-8 -*-

import os, logging
logger = logging.getLogger('cmdb')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

########################## db ##########################
DB_NAME = "ledao_cmdb"
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
########################## db ##########################

########################## EMAIL ##########################
ENABLE = 1
EMAIL_HOST = "smtp.exmail.163.com"
EMAIL_PORT = 25
EMAIL_USER = "ledao@163.com"
EMAIL_PASSWORD = ""
EMAIL_TLS = False
EMAIL_SSL = False
########################## EMAIL ##########################

########################## resource pool ##########################

RESOURCE_POOL_ID = 1
FREE_SERVER_ID = 1
FREE_VM_ID = 2

########################## resource pool ##########################


########################## zabbix ##########################

ZABBIX_API_URL = "http://zabbix/api_jsonrpc.php"
ZABBIX_IDC_API_URL = "http://idczabbix/zabbix/api_jsonrpc.php"
ZABBIX_USER = "admin"
ZABBIX_PASSWORD = "admin"

########################## zabbix ##########################

########################## fortress host ##########################

FORTRESS_HOST = "127.0.0.1"

REMOTE_CMDB_DIR = "/opt/cmdb-script/"
########################## fortress host ##########################


########################## sso ##########################

AUTH_URL = "http://sso.ledao.cn/services/sso/login"

TOKEN_URL = "http://ssoops.ledao.cn/api/home/token/"

LOGIN_URL = "http://ssoops.ledao.cn/sso/login/"

CALLBACK_URL = "/home/ssologin/"

########################## sso ##########################

########################## auto ##########################

AUTO_DOMAIN = "http://auto.9now.net"

AUTO_TOKEN = "74a7e825-3234-45b6-8306-e5b61a9214ec-1"

########################## auto ##########################

########################## gitlab ##########################

GITLAB_TOKEN = ""

GITLAB_DOMAIN = "http://127.0.0.1"

########################## gitlab ##########################


########################## 工单系统 ##########################

TICKET_URL = "http://test.ticket.ledao.cn"

########################## 工单系统 ##########################

REDIS_HOST = '127.0.0.1'

CMDB_TASK = "cmdb_task"

ZABBIX_TASK = "zabbix_task"

OPS_EMAIL = "chen.shaodong@ledao.com"

AES_KEY = "h3DJ&o9UJ2zO^(oh"

DEBUG = True

CMDB_VERSION = "0.1.1"

RUN_ENV = 'dev'

