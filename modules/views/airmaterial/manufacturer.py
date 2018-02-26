# coding: utf-8

from __future__ import unicode_literals

from flask_admin import expose
from flask import request, redirect
from functools import partial

from wtforms import SelectField
from modules.flows import BasicFlow
from wtforms.validators import DataRequired
from modules.models.airmaterial import Manufacturer
from modules.views import CustomView
from modules.views.column_formatter import checkbox_formater
from modules.views.operations import normal_operation_formatter
from util.fields.accessory_filed import AirmaterialFileuploadField
from modules.views.column_formatter import accessory_formatter


class _ManufacturerView(CustomView):
    """生产厂商"""

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
        '/static/js/upload_file.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/manufacturer_validation.js',
    ]

    column_list = [
        'name', 'address', 'contact', 'phone', 'operation'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'name': '名称',
        'businessScope': '经营范围',
        'address': '地址',
        'contact': '联系人',
        'phone': '电话',
        'email': '邮件',
        'fax': '传真',
        'operation': '操作',
        'fileResourceUrl': '附件',
    }
    # 查看页面显示的详情
    column_details_list = [
        'name', 'businessScope', 'address', 'contact', 'phone',
        'email', 'fax', 'fileResourceUrl',
    ]

    form_overrides = {
        'fileResourceUrl': partial(AirmaterialFileuploadField),
    }

    column_searchable_list = ('name', 'contact')

    support_flow = None

    one_line_columns = ['fileResourceUrl']

    column_formatters = {
        'operation': normal_operation_formatter,
        'fileResourceUrl': accessory_formatter('fileResourceUrl'),
    }


ManufacturerView = partial(
    _ManufacturerView, Manufacturer, name='生产厂商'
)
