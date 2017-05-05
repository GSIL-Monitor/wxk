# coding: utf-8

from __future__ import unicode_literals
import os, os.path, sys

from flask_script import Manager, Server

from app import create_app


settings = os.path.abspath('./etc/settings.py')
if not os.path.exists(settings):
    settings = os.path.abspath('./etc/dev.py')

if 'THY_SETTINGS' not in os.environ and os.path.exists(settings):
    os.environ['THY_SETTINGS'] = settings

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('runserver', Server(port=5000, host='0.0.0.0'))


@manager.command
def live(port=5000):
    from livereload import Server
    server = Server(manager.create_app())
    server.serve(port)


@manager.command
def init_local_dev():
    # 主要是为了方便本地测试，进而初始化
    import logging

    from modules.models.base import db
    from modules.models import user_datastore
    from modules.roles import init_builtin_roles, super_admin

    logging.info('Sir, we are going to drop all exist datas....')
    db.drop_all()

    logging.info('Yes, the whole data are going to to re-formatting!!')
    db.create_all()

    # 初始化默认权限
    roles = init_builtin_roles()

    db.session.add_all(roles)

    # 创建一个默认的管理员
    user_datastore.create_user(
        email='admin@hfga.com.cn',
        password='hfgahfga%',
        roles=[super_admin(db.session)]
    )
    db.session.commit()

    logging.info('Okay, it\'s DONE!')


if __name__ == '__main__':
    manager.run()
