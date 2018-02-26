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
def reset_database(username='admin', email='admin@hfga.com.cn', password='hfgahfga%'):
    # 如果是MySQL数据作为数据源，相应的数据库实例需要事先由运维初始化
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
        username=username,
        email=email,
        password=password,
        roles=[super_admin(db.session)]
    )
    db.session.commit()

    logging.info('Okay, it\'s DONE!')


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_airmaterial_category(clean, file=os.path.join(os.curdir, 'assets', 'airmaterial_category.csv')):
    from modules.models.airmaterial.airmaterial_category import AirmaterialCategory, read_datas
    from modules.models.util_csv import reset_datas

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        AirmaterialCategory, read_datas, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_storage_list(clean, file=os.path.join(os.curdir, 'assets', 'storage_list.csv')):
    from modules.models.airmaterial.storage_list import reset_datas, AirMaterialStorageList

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        AirMaterialStorageList, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_time_control_y5b(clean, file=os.path.join(os.curdir, 'assets', 'time_control_y5b.csv')):
    from modules.forms.y5b.time_control_unit import read_datas
    from modules.forms.util_csv import reset_datas

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        'time_control_unit_y5b', read_datas, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_scheduled_mx_check_y5b(clean, file=os.path.join(os.curdir, 'assets', 'schedule_mx_check_y5b.csv')):
    from modules.forms.y5b.scheduled_mx_check import read_datas
    from modules.forms.util_csv import reset_datas

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        'scheduled_mx_check_y5b', read_datas, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_flight_line_check_y5b(clean, file=os.path.join(os.curdir, 'assets', 'flight_line_check_y5b.csv')):
    from modules.forms.y5b.flight_line_check import read_datas
    from modules.forms.util_csv import reset_datas

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        'flight_line_check_y5b', read_datas, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_life_control_unit_y5b(clean, file=os.path.join(os.curdir, 'assets', 'life_control_y5b.csv')):
    from modules.forms.y5b.life_control_unit import read_datas
    from modules.forms.util_csv import reset_datas

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        'life_control_unit_y5b', read_datas, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_parking_check_y5b(clean, file=os.path.join(os.curdir, 'assets', 'parking_mx_check_y5b.csv')):
    from modules.forms.y5b.parking_check import read_datas
    from modules.forms.util_csv import reset_datas

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        'parking_mx_check_y5b', read_datas, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
@manager.option('--clean', help='Whether clean the datas before import new datas.')
def import_aircraft(clean, file=os.path.join(os.curdir, 'assets', 'aircraft.csv')):
    from modules.forms.aircraft.aircraft import read_datas
    from modules.forms.util_csv import reset_datas

    sys.stdout.write('Initialized %d data(s).\n' % reset_datas(file,
        'aircraft_information', read_datas, clean=clean))


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
def bind_mxp(clean, file=os.path.join(os.curdir, 'assets', 'aircraft.csv')):
    from modules.forms.aircraft.aircraft import bound_mxp

    sys.stdout.write('Initialized %d data(s).\n' % bound_mxp())


@manager.command
@manager.option('-f', '--file', help='The builtin airspace csv file name.')
def change_bind_information(clean, file=os.path.join(os.curdir, 'assets', 'bind_information.csv')):
    from modules.forms.aircraft.aircraft import (read_bind_information,
                                                 change_bind_information)

    sys.stdout.write('Initialized %d data(s).\n' % change_bind_information(file,
        'aircraft_information', read_datas=read_bind_information))


@manager.command
def init_translation():
    import subprocess, os.path

    if os.path.exists('./translations'):
        print('Nothing to be done, please using update_translation command.')
        return

    # 注意，这里的初始化有个相对路径，仅适用于WUJG的主机，好在该命令通常仅执行一次
    subprocess.check_call(
        ['pybabel', 'extract', '-F', 'babel.cfg', '-k', 'lazy_gettext', '-o', 'messages.pot',
         '.', '../../../flask-security'])
    subprocess.call(['pybabel', 'init', '-i', 'messages.pot', '-d', 'translations', '-l', 'zh'])

@manager.command
def update_translation():
    import subprocess

    subprocess.check_call(
        ['pybabel', 'extract', '-F', 'babel.cfg', '-k', 'lazy_gettext', '-o', 'messages.pot', '.'])
    subprocess.call(['pybabel', 'update', '-i', 'messages.pot', '-d', 'translations'])


@manager.command
def compile_translation():
    import subprocess

    subprocess.check_call(['pybabel', 'compile', '-d', 'translations'])


@manager.command
@manager.option('--category', help='Which data need to be cleared.')
def clear_database(category):
    # 如果是MySQL数据作为数据源，相应的数据库实例需要事先由运维初始化
    import logging

    from modules.models.base import db

    colls = db.engine.table_names()
    conn = db.engine.connect()

    role_datas = ['user', 'role', 'roles_users', 'basic_action', 'alembic_version']
    basic_datas = ['airport', 'fly_nature', 'formula', 'pesticide', 'pilot', 'sub_formula']
    if int(category) == 1:
        role_datas.extend(basic_datas)

    if int(category) in [0, 1]:
        logging.info('Sir, we are going to delete all exist datas without users and roles')

        conn.execute("SET FOREIGN_KEY_CHECKS=0")
        for name in colls:
            if name in role_datas:
                continue

            conn.execute("delete from %s" % name)
        conn.execute("SET FOREIGN_KEY_CHECKS=1")
        logging.info('Okay, it\'s DONE!')

    if int(category) == 2:
        role_datas.extend(basic_datas)
        logging.warn('Sir, we are going to delete all exist datas without basic datas')
        conn.execute("SET FOREIGN_KEY_CHECKS=0")
        for name in colls:
            if name in role_datas:
                continue
            conn.execute("drop table %s" % name)
        conn.execute("SET FOREIGN_KEY_CHECKS=1")
        logging.warn('Okay, it\'s DONE!')

    if int(category) == 3:
        air_colls = [
            'airmaterial_category', 'airmaterial_list', 'assemble',
            'assemble_application_list', 'assemble_application',
            'borrowing_in_return', 'borrowing_in_return_material',
            'disassemble_order', 'disassemble_material', 'lend_application',
            'lend_application_material', 'loan_material', 'loan_application',
            'loan_return_order', 'loan_return_material', 'manufacturer',
            'purchase_material', 'purchase_application', 'put_out_store',
            'put_out_store_material', 'repair_application', 'repair_material',
            'repair_return_order', 'repair_return_material', 'repair_supplier',
            'return_material_order', 'return_material', 'scrap',
            'scrap_material', 'storage_list', 'put_storage',
            'air_material_storage_list', 'supplier']

        air_colls_versions = [
            'airmaterial_category_version', 'assemble_version',
            'assemble_application_version',
            'borrowing_in_return_version',
            'disassemble_order_version', 'lend_application_version',
            'loan_application_version',
            'loan_return_order_version', 'manufacturer_version',
            'purchase_application_version', 'put_out_store_version',
            'repair_application_version', 'repair_return_order_version',
            'repair_supplier_version',
            'return_material_order_version', 'scrap_version',
            'put_storage_version',
            'air_material_storage_list_version', 'supplier_version']

        air_colls.extend(air_colls_versions)

        logging.warn('Sir, we are going to delete all exist datas about air datas')
        conn.execute("SET FOREIGN_KEY_CHECKS=0")
        for name in air_colls:

            conn.execute("delete from %s" % name)
        conn.execute("SET FOREIGN_KEY_CHECKS=1")
        logging.warn('Okay, it\'s DONE!')


@manager.command
@manager.option('--delete', help='Whether delete the all role user.')
def add_all_role_user(delete, username='hfga', email='hfga@hfga.com.cn', password="hfga%"):
    # 如果是MySQL数据作为数据源，相应的数据库实例需要事先由运维初始化
    import logging

    from modules.models.base import db
    from modules.models.role import BasicAction, Role
    from modules.views.perms import models
    from modules.models import user_datastore
    from modules.roles import AllAction
    from modules.models.user import User
    if delete == 'true':
        tmp_actions = BasicAction.query.join(Role, BasicAction.role_id == Role.id).filter(Role.name == AllAction)
        role = db.session.query(Role).filter_by(name=AllAction).first()
        user = db.session.query(User).filter_by(username=username).first()
        for item in tmp_actions.all():
            db.session.delete(item)
        datas = []
        for item in models:
            action = {}
            for val in item[2]:
                action[val] = True
            basic_action = BasicAction(**action)
            basic_action.review_approve = basic_action.review_refuse = basic_action.review
            basic_action.approved = basic_action.approve_refuse = basic_action.approve
            basic_action.submit_review = basic_action.review_again = basic_action.submit
            basic_action.second_approve_refuse = basic_action.second_approved
            basic_action.role = role
            basic_action.model = item[0]
            db.session.add(basic_action)
            datas.append(basic_action)
        user.role = [role]
        db.session.commit()
        return

    role = Role(name=AllAction, description='全权角色')
    db.session.add(role)

    datas = []
    for item in models:
        action = {}
        for val in item[2]:
            action[val] = True
        basic_action = BasicAction(**action)
        basic_action.review_approve = basic_action.review_refuse = basic_action.review
        basic_action.approved = basic_action.approve_refuse = basic_action.approve
        basic_action.submit_review = basic_action.review_again = basic_action.submit
        basic_action.second_approve_refuse = basic_action.second_approved
        basic_action.role = role
        basic_action.model = item[0]
        db.session.add(basic_action)
        datas.append(basic_action)

    # 创建一个默认的管理员
    user_datastore.create_user(
        username=username,
        email=email,
        password=password,
        roles=[role]
    )
    db.session.commit()

    logging.info('Okay, it\'s DONE!')


if __name__ == '__main__':
    manager.run()
