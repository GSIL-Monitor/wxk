# coding: utf-8

from __future__ import unicode_literals

import os

DEBUG = False
TESTING = False
PROPAGATE_EXCEPTIONS = True
ADMIN_RAISE_ON_VIEW_EXCEPTION = False

STATIC_FOLDER = os.path.join(os.getcwd(), 'assets', 'static')

if 'SERVER_NAME' in os.environ:
    SERVER_NAME = os.environ['SERVER_NAME']

#: site
SITE_TITLE = u'徐州农用航空站通航信息化系统'
SITE_URL = '/'

COPYRIGHT_STR = '2016 - {} 技术开发: 海丰通航科技有限公司'

#: session
SESSION_COOKIE_NAME = '_s'
# SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

GRAVATAR_BASE_URL = 'http://www.gravatar.com/avatar/'
GRAVATAR_EXTRA = ''

# 与安全相关的配置
SECRET_KEY = 'tonghangyun-admin@1$$!%ser-key@100'
PASSWORD_SECRET = 'you##s%houldntkon@wnthis'

# 与存储服务相关的配置
# SQLALCHEMY_DATABASE_URI = '参见对应的环境变量设置'
SQLALCHEMY_ECHO = False

MONGO_HOST = '192.168.100.204'
MONGO_PORT = 30017

# 与认证安全相关的配置
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "tongrandomhangyun@!$__secret-password,%#!#%%!"

SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# 不准通过通航云管理平台的注册界面进行注册
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = True  # 由于脚本默认不激活
SECURITY_TRACKABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_EMAIL_SENDER = 'no-reply@tonghangyun.com.cn'

# 与邮件发送相关的配置
MAIL_SERVER = 'smtp.qiye.163.com'
MAIL_DEFAULT_SENDER = ('no-reply', 'no-reply@hfga.com.cn')
MAIL_USERNAME = 'no-reply@tonghangyun.com.cn'
MAIL_PASSWORD = 'BJ@hfga.com.cn33'

CACHE_TYPE = 'simple'

# 与维修客配置相关的信息
WXK_API_BASE = r'http://192.168.100.204'
PLATFORM_API_BASE = 'http://dev.hf-it.org/platform'
WXK_ACCESS_ROLE = 'wxk-platform-access'
# 真正部署的时候，与维修配置相关的用户名和密码最好使用环境变量
WXK_USERNAME = os.environ[
    'WXK_USERNAME'] if 'WXK_USERNAME' in os.environ else 'zhongrui'
WXK_PASSWORD = os.environ[
    'WXK_PASSWORD'] if 'WXK_PASSWORD' in os.environ else 'zhongrui123'
MONGO_DBNAME = os.environ[
    'WXK_MONGODB_NAME'] if 'WXK_MONGODB_NAME' in os.environ else 'zrth-storage'
SQLALCHEMY_DATABASE_URI = os.environ[
    'WXK_MYSQL_DB'] if 'WXK_MYSQL_DB' in os.environ else 'mysql://root:123@192.168.101.1/zrth_storage'
WXK_GROUP = os.environ[
    'WXK_GROUP'] if 'WXK_GROUP' in os.environ else 'zrth'

# 与REDIS相关的配置
REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_USER_DBID = 15        # 目前该实现需要一个特殊的DB来存放与用户缓存数据相关的内容
REDIS_PASSWORD = os.environ[
    'REDIS_PASSWORD'] if 'REDIS_PASSWORD' in os.environ else '%016q1w2e3root'

HOMEPAGE_MAX_COUNT = 8          # 首页各项显示的最多条数

PRINT_VERSION = True

# rebbitmq配置
MQ_HOST = 'rabbitmq'
MQ_USERNAME = 'admin'
MQ_PASSWORD = '123456'
MQ_VHOST = '/'
MQ_EXCHANGE = 'tonghangyun-cache-exchange'
MQ_TIMEOUT = 3
FILE_ROUTING_KEY = 'related-file'

# 机型配置
PLANE_TYPE = '运5B(D)'
