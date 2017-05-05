import os
import datetime

DEBUG = True
TESTING = False
VERIFY_EMAIL = True
VERIFY_USER = True
ADMIN_RAISE_ON_VIEW_EXCEPTION = False

STATIC_FOLDER = os.path.join(os.getcwd(), 'assets', 'static')

#: site
SITE_TITLE = '机务维修管理系统'
SITE_URL = '/'

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
SQLALCHEMY_DATABASE_URI = 'sqlite:///sample_db.sqlite'
SQLALCHEMY_ECHO = True

MONGO_HOST = '192.168.100.204'
MONGO_PORT = 30017
MONGO_DBNAME = 'zrth-storage'

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

# 不准通过通航云管理平台的注册界面进行注册
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False   # 由于脚本默认不激活
SECURITY_TRACKABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_EMAIL_SENDER = 'no-reply@tonghangyun.com.cn'

# 与邮件发送相关的配置
MAIL_SERVER = '192.168.100.202'
MAIL_DEFAULT_SENDER = ('no-reply', 'no-reply@tonghangyun.com.cn')


API_BASEURL = r'http://192.168.100.204'
API_AUTH_URL = r'http://dev.hf-it.org/platform/auth'
API_AUTH_USER = {"login": "zhongrui", "password": "zhongrui123"}
API_CONTENT_TPYE = 'application/json'
