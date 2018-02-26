# encoding: utf-8

from __future__ import unicode_literals

from flask_security import SQLAlchemyUserDatastore, Security

from .base import db
from .user import User
from .role import Role, BasicAction


class SupportUsernameDatastore(SQLAlchemyUserDatastore):

    def __init__(self, *args, **kwargs):
        super(SupportUsernameDatastore, self).__init__(*args, **kwargs)

    def get_user(self, identifier):
        user = super(SupportUsernameDatastore, self).get_user(identifier)
        if user is not None:
            return user
        return self.user_model.query.filter_by(username=identifier).first()


user_datastore = SupportUsernameDatastore(db, User, Role)


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
