import os
import datetime

DEBUG = False
TESTING = False
PROPAGATE_EXCEPTIONS = True
ADMIN_RAISE_ON_VIEW_EXCEPTION = False

STATIC_FOLDER = os.path.join(os.getcwd(), 'assets', 'static')

if 'SERVER_NAME' in os.environ:
    SERVER_NAME = os.environ['SERVER_NAME']

#: site
SITE_TITLE = '机务维修管理系统'
SITE_URL = '/'

#: session
SESSION_COOKIE_NAME = '_s'
#SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

GRAVATAR_BASE_URL = 'http://www.gravatar.com/avatar/'
GRAVATAR_EXTRA = ''

# 与安全相关的配置
SECRET_KEY = 'tonghangyun-admin@1$$!%ser-key@100'
PASSWORD_SECRET = 'you##s%houldntkon@wnthis'

# 与存储服务相关的配置

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
SECURITY_SEND_REGISTER_EMAIL = True # 由于脚本默认不激活
SECURITY_TRACKABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_EMAIL_SENDER = 'no-reply@hfga.com.cn'

# 与邮件发送相关的配置
MAIL_SERVER = 'smtp.qiye.163.com'
MAIL_DEFAULT_SENDER = ('no-reply', 'no-reply@hfga.com.cn')
MAIL_USERNAME = 'no-reply@hfga.com.cn'
MAIL_PASSWORD = 'BJ@hfga.com.cn33'
