# encoding: utf-8

from __future__ import unicode_literals

import flask_admin as admin
from flask import url_for
from flask_admin import helpers as admin_helpers
from flask_pymongo import PyMongo
from flask_principal import identity_loaded

from .models import init_model, init_db
from .views import IndexView
from .views.project_tech import views as tech_category_views
from .views.production import views as production_views
from .views.quality import views as quality_views
from .views.notification import NoticeView
from .views.notification.notice import retrieve_unread_notifies
from .views.airmaterial import views as airmaterial_views
from .views.mxp import init_mxp_view
from .views.admin import UserAdminView, RoleAdminView
from .views.aircraft import AircraftInformationView
from .perms import _on_identity_loaded


PROJECT_TECH_CATEGORY = '工程技术'
PRODUCTION_MANAGEMENT = '生产管理'
QUALITY_MANAGEMENT = '质量管理'
NOTIFICATION_MANAGEMENT = '通知管理'
AIRMATERIAL_MANAGEMENT = '航材管理'
MAINTAINANCE_MANAGEMENT = '维修方案管理'
MAINTAIN = '维修视图'
AIRCRAFT_COL = 'aircraft_information'


def init_app(app):
    db = init_db(app)
    mongo = PyMongo(app)

    sec = init_model(app)

    admin_obj = admin.Admin(
        app, name='中瑞通航机务维修管理系统',
        base_template='layout.html',
        template_mode='bootstrap3',
        index_view=IndexView(
            name='控制面板',
            menu_icon_type='fa', menu_icon_value='fa-home'))

    # Flask-Security 使用Flask-Admin的相关样式
    @sec.context_processor
    def security_context_processor():
        return dict(admin_base_template=admin_obj.base_template,
                    admin_view=admin_obj.index_view,
                    h=admin_helpers,
                    get_url=url_for)

    # 需要处理一些额外的与操作相关的权限设置
    identity_loaded.connect_via(app)(_on_identity_loaded)

    # TODO: 修改小图标，具体请查看font-awsome
    # 工程技术模块的配置
    register_view_by_category(
        admin_obj, db.session,
        tech_category_views, PROJECT_TECH_CATEGORY)
    custom_category_style(
        admin_obj, PROJECT_TECH_CATEGORY,
        'fa', 'fa-file-text-o')

    # 机队管理模块配置
    with app.app_context():
        admin_obj.add_view(AircraftInformationView(
            mongo.db, AIRCRAFT_COL, 'aircraft', '机队管理',
            menu_icon_type='fa', menu_icon_value='fa-plane'))

    # 生产管理模块的配置
    register_view_by_category(
        admin_obj, db.session,
        production_views, PRODUCTION_MANAGEMENT)
    custom_category_style(
        admin_obj, PRODUCTION_MANAGEMENT,
        'fa', 'fa-paper-plane')

    # 质量管理模块的配置
    register_view_by_category(
        admin_obj, db.session,
        quality_views, QUALITY_MANAGEMENT)
    custom_category_style(
        admin_obj, QUALITY_MANAGEMENT,
        'fa', 'fa-paper-plane')

    # 航材管理模块的配置
    register_view_by_category(
        admin_obj, db.session,
        airmaterial_views, AIRMATERIAL_MANAGEMENT)
    custom_category_style(
        admin_obj, AIRMATERIAL_MANAGEMENT,
        'fa', 'fa-gears')

    # 维修管理模块配置
    with app.app_context():
        init_mxp_view(admin_obj, mongo.db, category=MAINTAINANCE_MANAGEMENT)
        custom_category_style(admin_obj,
                               MAINTAINANCE_MANAGEMENT, 'fa', 'fa-book')
        app.mongodb = mongo.db

    # 通知管理模块的配置
    admin_obj.add_view(
        NoticeView(db.session, menu_icon_type='fa', menu_icon_value='fa-bullhorn'))

    # 下面的两个视图是独立的，通常也只有超级管理员可以看到
    admin_obj.add_view(UserAdminView(db.session))
    admin_obj.add_view(RoleAdminView(db.session))

    retrieve_unread_notifies(app)

    return db


def register_view_by_category(admin_container, session, views, category):
    for view in views:
        admin_container.add_view(view(session, category=category))


def custom_category_style(admin_container, category, icon_type, icon_value):
    category_item = admin_container.get_category_menu_item(category)
    category_item.icon_type = icon_type
    category_item.icon_value = icon_value
