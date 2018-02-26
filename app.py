#! /usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
import os
import datetime
import logging
import time

from flask import render_template, Flask, session, url_for, g
from pymongo.errors import ServerSelectionTimeoutError, NetworkTimeout

from util.exception import BackendServiceError, TokenNeedRefreshError, QiNiuServiceError

app = Flask(
    __name__,
    template_folder='templates',
)


def create_app(config=None):
    """
    创建应用程序唯一的实例

    :params config: dict实例或使用绝对路径标识的python文件，用于配置整个Flask进程
    """

    if 'THY_SETTINGS' in os.environ:
        val = os.environ['THY_SETTINGS']
        config_file = 'etc/local.py'
        if 'prod' == val:
            config_file = 'etc/prod.py'
        elif 'stage' == val:
            config_file = 'etc/stage.py'
        elif 'dev' == val:
            config_file = 'etc/dev.py'

        app.config.from_pyfile(config_file)

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    # 必须包含有静态数据的配置信息
    app.static_folder = app.config.get('STATIC_FOLDER')
    app.config.update({'SITE_TIME': datetime.datetime.now()})
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

    register_hooks(app)
    register_jinja(app)
    register_cache(app)
    register_proxy(app)

    # register_routes(app)
    # register_logger(app)
    # register_login(app)
    register_admin(app)
    register_mail(app)
    register_babel(app)

    return app


def register_hooks(app):
    """一些公共的用于处理特殊状态的请求返回页。"""
    @app.errorhandler(400)
    @app.errorhandler(403)
    def bad_request(error):
        return render_template(
            "forbbiden.html",
            admin_view={
                'category': '出错了',
                'name': app.config.get('SITE_TITLE'),
                'admin': {'name': app.config.get('SITE_TITLE')},
            },
            get_url=url_for,
        ), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template(
            "not_found.html",
            admin_view={
                'category': '出错了',
                'name': app.config.get('SITE_TITLE'),
                'admin': {'name': app.config.get('SITE_TITLE')},
            },
            get_url=url_for,
        ), 404

    @app.errorhandler(BackendServiceError)
    @app.errorhandler(TokenNeedRefreshError)
    @app.errorhandler(ServerSelectionTimeoutError)
    @app.errorhandler(NetworkTimeout)
    @app.errorhandler(QiNiuServiceError)
    @app.errorhandler(503)
    @app.errorhandler(501)
    @app.errorhandler(500)
    @app.errorhandler(405)
    def server_error(error):

        if isinstance(error, (ServerSelectionTimeoutError, NetworkTimeout)):
            app.logger.warning('Mongo service is not available.')

        if isinstance(error, BackendServiceError):
            app.logger.warning('The weixiuke restfull api is not available.')

        if isinstance(error, QiNiuServiceError):
            app.logger.warning('The qiniu service has some wrong')

        refresh = False
        if isinstance(error, TokenNeedRefreshError):
            refresh = True

        return render_template(
            "service_unavailable.html",
            admin_view={
                'category': '出错了',
                'name': app.config.get('SITE_TITLE'),
                'admin': {'name': app.config.get('SITE_TITLE')},
            },
            get_url=url_for,
            refresh=refresh,
        ), 503


def register_jinja(app):

    def uniform_datetime_to_day(value):
        if value is None:
            return 'N/A'
        return value.strftime('%m-%d')

    def uniform_datetime_to_str(value, format):
        if value is None:
            return 'N/A'
        value = time.localtime(value)
        value = time.strftime(format, value)
        return value

    from util.jinja_filter import format_username, province, city, county
    app.jinja_env.filters['format_username'] = format_username
    app.jinja_env.filters['province'] = province
    app.jinja_env.filters['city'] = city
    app.jinja_env.filters['county'] = county
    app.jinja_env.filters['uniform_datetime_to_day'] = uniform_datetime_to_day
    app.jinja_env.filters[
        'uniform_datetime_to_str'] = uniform_datetime_to_str


def register_babel(app):
    """Configure Babel for internationality."""
    from flask_babelex import Babel, Domain

    babel = Babel(app, default_locale='zh')
    # 使用本地的domain，因为flask_security等库没有默认提供中文的支持
    local_domain = Domain(domain='security')
    security = app.extensions['security']
    security.i18n_domain = local_domain

    @babel.localeselector
    def get_locale():
        session['lang'] = 'zh'
        return session.get('lang', 'zh')


def register_logger(app):
    """Track the logger for prodution mode."""
    if app.debug:
        return
    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


def register_cache(app):
    from modules.cache import cache

    cache.init_app(app)


def register_admin(app):
    from modules.admin import init_app
    db = init_app(app)
    app.db = db

    if app.config.get('PRINT_VERSION', False):
        @app.before_request
        def inject_version():
            g.__version__ = app.__version__


def register_mail(app):
    from flask_mail import Mail
    Mail(app)


def register_proxy(app):
    from modules.proxy import proxy

    # 方便其他模块使用
    app.redis_cache = proxy.init_app(app)
