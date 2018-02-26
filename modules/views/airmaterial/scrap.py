# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from flask import request
from flask_admin import expose
from wtforms import DateField
from modules.flows import ScrapFlow
from wtforms.validators import DataRequired
from flask_security import current_user
from sqlalchemy import or_
from collections import OrderedDict

from util.widgets import DateWidget
from modules.models.airmaterial import Scrap, Manufacturer
from modules.models.role import Role, BasicAction
from modules.flows.states import SecApproved, Reviewed, Scrapped
from modules.models.airmaterial.scrap import ScrapMaterial
from modules.models.airmaterial import AirMaterialStorageList
from .out_storage_application_update_freezed_quantity import\
    UpdateStorageListFreezedQuantity
from airmaterial_fileds import *


class _ScrapView(UpdateStorageListFreezedQuantity):
    """报废单视图"""

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/bootstrap-select.min.js',
        '/static/js/jquery.multi-select.js',
        '/static/js/components-dropdowns.js',
        '/static/js/select_planeType.js',
        '/static/js/inline_table.js',
        '/static/js/numbro.js',
        '/static/js/languages.js',
        '/static/js/zh-CN.min.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/moment.min.js',
        '/static/js/pikaday.js',
        '/static/js/pikaday-zh.js',
        '/static/js/upload_file.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/scrap_validation.js',
    ]

    column_list = [
        'number', 'scrapCategory', 'applyPerson', 'applyDate', 'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'applyPerson': '申请人',
        'applyDate': '申请日期',
        'scrapCategory': '报废类型',
        'statusName': '状态',
        'applyReason': '申请原因',
        'partNumber': '件号',
        'serialNum': '序号',
        'name': '名称',
        'category': '类别',
        'quantity': '数量',

    }

    column_searchable_list = (
        'scrapCategory', 'number', 'statusName', 'applyPerson')
    # 查看页面显示的详情
    column_details_list = [
        'number', 'applyPerson', 'applyDate', 'scrapCategory',
        'applyReason'
    ]

    form_excluded_columns = ['statusName', 'scrapMaterial', 'putOutStore']

    support_flow = partial(ScrapFlow, 'scrap flow')

    form_overrides = {
        'applyDate': partial(DateField, widget=DateWidget()),
    }
    form_widget_args = {
        'number': {
            'readonly': True
        },
    }

    one_line_columns = ['applyReason']

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
        return super(_ScrapView, self).validate_form(form)

    def get_query(self):
        datas = super(_ScrapView, self).get_query()

        ids = [item.id for item in datas] if datas.count() else []
        role = Role.query.join(
            BasicAction, Role.id == BasicAction.role_id
        ).filter(BasicAction.view == True,
                 BasicAction.model == 'scrap')

        if not role.count():
            return datas

        for val in role:
            if val not in current_user.roles:
                continue
            datas = self.model.query.filter(
                or_(self.model.id.in_(ids),
                    self.model.auditStatus.in_([Reviewed, SecApproved, Scrapped])))

        return datas

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([('category', AM_CATEGORY),
                                          ('partNumber', AM_PARTNUMBER),
                                          ('serialNum', AM_SERIALNUM),
                                          ('name', AM_NAME),
                                          ('manufacturer', AM_MANUFACTURER),
                                          ('quantity', AM_QUANTITY),
                                          ('effectiveDate', AM_EFFECTIVEDATE),
                                          ('lastCheckDate', AM_LASTCHECKDATE),
                                          ('nextCheckDate', AM_NEXTCHECKDATE)])
        self.relationField = 'scrapMaterial'
        self.f_key = 'application_id'
        self.relationModel = ScrapMaterial

        super(_ScrapView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)

        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = [
            '一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件']
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['need'] = True
        table_columns[2]['editor'] = 'select'
        table_columns[2]['selectOptions'] = []
        table_columns[3]['readOnly'] = True
        table_columns[3]['need'] = True
        table_columns[4]['editor'] = 'select'
        table_columns[4]['selectOptions'] = [
            m.name for m in Manufacturer.query.all()]
        table_columns[5]['type'] = 'numeric'
        table_columns[5]['format'] = '0'
        table_columns[5]['need'] = True
        table_columns[6]['editor'] = 'select'
        table_columns[6]['selectOptions'] = []
        table_columns[6]['checkNeed'] = True
        table_columns[7]['type'] = 'date'
        table_columns[7]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[8]['editor'] = 'select'
        table_columns[8]['selectOptions'] = []
        table_columns[8]['checkNeed'] = True

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/scrap_table.js'
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):

        rowid = request.args.getlist('rowid')
        ao_id = request.args.get('id')
        cats = None
        table_datas = []
        if rowid:
            cats = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.id.in_(rowid)).all()
        elif ao_id:
            cats = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.id == ao_id).all()
        if cats:
            table_datas = [[
                cat.category, cat.partNumber, cat.serialNum,
                cat.name, cat.manufacturer,
                cat.quantity - cat.freezingQuantity, cat.effectiveDate,
                cat.lastCheckDate, cat.nextCheckDate
            ]for cat in cats]

        table_datas = json.dumps(table_datas)

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })

        return super(_ScrapView, self).create_view()

    def get_audit_form_class(self, model, verb):
        if verb == 'review' and model.scrapCategory == '一般':
            return self._action_view_cfg['review_only'].form
        return None


ScrapView = partial(
    _ScrapView, Scrap, name='报废单'
)
