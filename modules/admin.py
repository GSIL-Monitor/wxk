# encoding: utf-8

from __future__ import unicode_literals
import os.path

import flask_admin as admin
from flask import url_for
from flask_admin import helpers as admin_helpers
from flask_pymongo import PyMongo
from flask_principal import identity_loaded

import datetime

from .models import init_model, init_db
from .views import IndexView
from .views.quality import ReservedFaultView
from .views.notification import NoticeView
from .views.notification.notice import retrieve_unread_notifies
from .views.notification.announcement import AnnouncementView
# from .views.airmaterial import views as airmaterial_views
from .views.mxp.y5b import Y5BView
from .views.basic_data import views as basic_data_views
from .views.aircraft import AircraftInformationView
from .views.production import (RoutineWorkView, CompanyDayRecordView,
                               FaultReportsView, TroubleShootingView,
                               MaintenanceRecordView, ExamineRepairRecordView)
from .views.navigational import (FlightLogView, FlightlogStatisticsView,
                                 FormulaStatisticsView)
from .views.airmaterial import (
    AirmaterialCategoryView, PurchaseApplicationView, LendApplicationView,
    ReturnMaterialOrderView, StorageView, DisassembleOrderView,
    BorrowingInReturnView, PutOutStoreView, LoanReturnOrderView,
    LoanApplicationOrderView, AssembleApplicationView, AssembleView,
    RepairApplicationView, ManufacturerView, ScrapView, RepairReturnOrderView,
    AirMaterialStorageListView, SupplierView, RepairSupplierView,
    ExpireWarningView, StockWarningView, CheckWarningView
)
from .views.project_tech import (TechMaterialView, TrainingArchiveView,
                                 TrainigMaterialView, TrainingPlanView,
                                 AirworthinessView, EngineeringOrderView,
                                 RetainView)
from .views.configuration import ConfigurationView
from .views.warning_configuration.check_warning import CheckWaringConfigurationView
from .views.warning_configuration.stock_warning import StockWaringConfigurationView
from .views.warning_configuration.expire_warning import ExpireWaringConfigurationView
from .perms import _on_identity_loaded
from .views.admin import UserAdminView, RoleAdminView
from .views.unsubmit_flight_log import flight_log_notice

from . import __version__


MAINTAINANCE_MANAGEMENT = '机务维修管理'
SYSTEM_MANAGEMENT = '系统管理'
NAVIGATIONAL_MANAGEMENT = '航务管理'
Quality_MANAGEMENT = '质量管理'
AIRMATERIAL_MANAGEMENT = '航材管理'
AIRCRAFT_COL = 'aircraft_information'
FLIGHTLOG_COL = 'flight_log'


def init_app(app):
    db = init_db(app)
    mongo = PyMongo(app)

    sec = init_model(app)
    app.__version__ = __version__

    admin_obj = admin.Admin(app, name=app.config['SITE_TITLE'],
                            translations_path=os.path.join(
                                app.root_path, 'translations'),
                            base_template='layout.html',
                            template_mode='bootstrap3',
                            index_view=IndexView(
                                name='首页',
                                menu_icon_type='fa',
                                menu_icon_value='fa-home'))

    # WUJG: 针对不同公司的实现，其权限或角色名可能会不同，通过下述机制可以针对不同的公司进行配置
    # 类级的权限配置，该优先级高于用户配置的内容，如果不需要，就无需设置
    # CustomView.view_accept_roles = role_management_dict
    # MongoCustomView.view_accept_roles = role_management_dict

    # Flask-Security 使用Flask-Admin的相关样式
    @sec.context_processor
    def security_context_processor():
        return dict(admin_base_template=admin_obj.base_template,
                    admin_view=admin_obj.index_view,
                    h=admin_helpers,
                    get_url=url_for)

    @sec.login_context_processor
    def security_login_processor():
        year = datetime.datetime.now().year
        return dict(copy_right=app.config['COPYRIGHT_STR'].format(year))

    # 需要处理一些额外的与操作相关的权限设置
    identity_loaded.connect_via(app)(_on_identity_loaded)

    # 机务维修管理配置
    maintain_list = [
        RoutineWorkView, TechMaterialView, TrainingArchiveView,
        TrainigMaterialView, TrainingPlanView, AirworthinessView,
        EngineeringOrderView, MaintenanceRecordView, FaultReportsView,
        TroubleShootingView, ExamineRepairRecordView, RetainView,
        ReservedFaultView,
    ]

    navigational_list = [
        FlightLogView, CompanyDayRecordView, FlightlogStatisticsView,
        FormulaStatisticsView,
    ]

    quality_list = []
    # 航材管理配置
    airmaterial_list = [
        AirmaterialCategoryView, PurchaseApplicationView,
        LendApplicationView, ReturnMaterialOrderView,
        StorageView, DisassembleOrderView,
        BorrowingInReturnView, PutOutStoreView,
        AssembleApplicationView, AssembleView,
        LoanReturnOrderView, LoanApplicationOrderView,
        RepairApplicationView, RepairReturnOrderView,
        ManufacturerView, ScrapView, AirMaterialStorageListView,
        SupplierView, RepairSupplierView, ExpireWarningView,
        StockWarningView, CheckWarningView

    ]

    with app.app_context():
        app.mongodb = mongo.db
        admin_obj.add_view(Y5BView(
            mongo.db, 'y5b', name='维修方案', category=MAINTAINANCE_MANAGEMENT))

    register_view_by_category(
        admin_obj, db.session, maintain_list, MAINTAINANCE_MANAGEMENT)
    register_view_by_category(
        admin_obj, db.session, navigational_list, NAVIGATIONAL_MANAGEMENT)
    register_view_by_category(
        admin_obj, db.session, quality_list, Quality_MANAGEMENT)
    register_view_by_category(
        admin_obj, db.session, airmaterial_list, AIRMATERIAL_MANAGEMENT)
    custom_category_style(admin_obj, MAINTAINANCE_MANAGEMENT, 'fa', 'fa-book')

    with app.app_context():
        admin_obj.add_view(AircraftInformationView(
            mongo.db, AIRCRAFT_COL, 'aircraft', name='机队管理',
            category=MAINTAINANCE_MANAGEMENT))

    # 系统管理配置
    admin_obj.add_view(UserAdminView(db.session, category=SYSTEM_MANAGEMENT))
    admin_obj.add_view(RoleAdminView(db.session, category=SYSTEM_MANAGEMENT))
    admin_obj.add_view(NoticeView(db.session, category=SYSTEM_MANAGEMENT))
    admin_obj.add_view(AnnouncementView(
        db.session, category=SYSTEM_MANAGEMENT))
    admin_obj.add_view(ConfigurationView(category=SYSTEM_MANAGEMENT))
    admin_obj.add_view(
        CheckWaringConfigurationView(category=SYSTEM_MANAGEMENT))
    admin_obj.add_view(
        StockWaringConfigurationView(category=SYSTEM_MANAGEMENT))
    admin_obj.add_view(
        ExpireWaringConfigurationView(category=SYSTEM_MANAGEMENT))
    register_view_by_category(
        admin_obj, db.session, basic_data_views, category=SYSTEM_MANAGEMENT)
    custom_category_style(admin_obj, SYSTEM_MANAGEMENT, 'fa', 'fa-cog')
    custom_category_style(admin_obj, NAVIGATIONAL_MANAGEMENT, 'fa', 'fa-plane')
    custom_category_style(admin_obj, Quality_MANAGEMENT, 'fa', 'fa-sliders')
    custom_category_style(admin_obj, AIRMATERIAL_MANAGEMENT, 'fa', 'fa-cog')

    retrieve_unread_notifies(app)
    flight_log_notice(app)

    return db


def register_view_by_category(admin_container, session, views, category):

    for view in views:
        admin_container.add_view(view(session, category=category))


def custom_category_style(admin_container, category, icon_type, icon_value):
    category_item = admin_container.get_category_menu_item(category)
    if category_item is not None:
        category_item.icon_type = icon_type
        category_item.icon_value = icon_value
