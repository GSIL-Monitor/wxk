# coding: utf-8

from __future__ import unicode_literals

import os

DEBUG = True
TESTING = False
VERIFY_EMAIL = True
VERIFY_USER = True
ADMIN_RAISE_ON_VIEW_EXCEPTION = False

STATIC_FOLDER = os.path.join(os.getcwd(), 'assets', 'static')

#: site
SITE_TITLE = '徐州农用航空站通航信息化系统'
SITE_URL = '/'

COPYRIGHT_STR = '2016 - {} 技术开发: 海丰通航科技有限公司'

#: session
SESSION_COOKIE_NAME = '_s'
# SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

# 这几与认证相关的配置非常重要，必须进行设置
SECRET_KEY = 'fuwu haifeng xitong $$@!# secret key'
PASSWORD_SECRET = 'password secret$!@#^!nnB'

GRAVATAR_BASE_URL = 'http://www.gravatar.com/avatar/'
GRAVATAR_EXTRA = ''


# 与存储服务相关的配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mahui@127.0.0.1:3306/localhost'
SQLALCHEMY_ECHO = False


MONGO_HOST = '192.168.100.204'
MONGO_PORT = 30017

# 与认证安全相关的配置
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

CACHE_TYPE = 'simple'

# 不准通过通航云管理平台的注册界面进行注册
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False   # 由于脚本默认不激活
SECURITY_TRACKABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_EMAIL_SENDER = 'no-reply@tonghangyun.com.cn'

# 与邮件发送相关的配置
MAIL_SERVER = '192.168.100.202'
MAIL_DEFAULT_SENDER = ('no-reply', 'no-reply@tonghangyun.com.cn')

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
WXK_GROUP = os.environ[
    'WXK_GROUP'] if 'WXK_GROUP' in os.environ else 'zrth'

# 与REDIS相关的配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_USER_DBID = 15                # 目前该实现需要一个特殊的DB来存放与用户缓存数据相关的内容
REDIS_PASSWORD = None

HOMEPAGE_MAX_COUNT = 6          # 首页各项显示的最多条数

PRINT_VERSION = True

# rebbitmq配置
MQ_HOST = '192.168.4.134'
MQ_USERNAME = 'guest'
MQ_PASSWORD = 'guest'
MQ_VHOST = '/'
MQ_EXCHANGE = 'tonghangyun-cache-exchange'
MQ_TIMEOUT = 3
FILE_ROUTING_KEY = 'related-file'

# 机型配置
PLANE_TYPE = '运5B(D)'
