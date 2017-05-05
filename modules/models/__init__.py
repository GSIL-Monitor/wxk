# encoding: utf-8

from __future__ import unicode_literals

from flask_security import SQLAlchemyUserDatastore, Security

from .base import db
from .user import User
from .role import Role, BasicAction


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def init_db(app):

    db.init_app(app)

    return db


def init_model(app, hook=None):
    "初始化管理端的相关存储模型定义。"

    security = Security(app, user_datastore)

#    if hook and isinstance(hook, Iterable):
#        for item in hook:
#            item()

    return security
