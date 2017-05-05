#! /usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
import os
import datetime
import logging

from flask import request, render_template
from flask import Flask, jsonify

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

    # register_hooks(app)
    register_jinja(app)

    # register_babel(app)
    # register_routes(app)
    # register_logger(app)
    # register_login(app)
    register_admin(app)
    register_mail(app)

    return app


def register_hooks(app):
    """一些公共的用于处理特殊状态的请求返回页。"""

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("nonexist.html"), 404

    @app.errorhandler(503)
    def server_error(error):
        return render_template("servererror.html"), 503

    @app.errorhandler(405)
    @app.errorhandler(501)
    def user_unavailable(error):
        return render_template("userunabled.html")


def register_jinja(app):

    def uniform_datetime_to_day(value):
        if value is None:
            return 'N/A'
        return value.strftime('%m-%d')

    from util.jinja_filter import format_username, province, city, county
    app.jinja_env.filters['format_username'] = format_username
    app.jinja_env.filters['province'] = province
    app.jinja_env.filters['city'] = city
    app.jinja_env.filters['county'] = county
    app.jinja_env.filters['uniform_datetime_to_day'] = uniform_datetime_to_day


def register_babel(app):
    """Configure Babel for internationality."""
    from flask_babel import Babel

    babel = Babel(app)
    supported = app.config.get('BABEL_SUPPORTED_LOCALES',
                               ['en', 'zh'])
    default = app.config.get('BABEL_DEFAULT_LOCALE', 'en')

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(supported, default)


def register_logger(app):
    """Track the logger for prodution mode."""
    if app.debug:
        return
    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)


def register_cached_model(app):
    from util.broker import attach_model

    # 目前只处理了Tracker和Aircraft模型
    from tonghangyun_models import (Tracker, Aircraft, ServiceConfigModel,
                                    Airspace, MeteorologicalStation)
    from tonghangyun_common import GACompany

    attach_model(Tracker, Aircraft, ServiceConfigModel, Airspace,
                 MeteorologicalStation, GACompany)


def register_admin(app):
    from modules.admin import init_app
    db = init_app(app)
    app.db = db


def register_mail(app):
    from flask_mail import Mail
    Mail(app)
