# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from flask import request, jsonify
from flask_admin import expose
import json

from modules.models.airmaterial.supplier import Supplier
from util.fields.accessory_filed import AirmaterialFileuploadField
from modules.views.operations import normal_operation_formatter
from ..column_formatter import accessory_formatter
from wtforms.validators import DataRequired
from modules.views import CustomView


class _SupplierView(CustomView):
    # 供应商列表视图应显示的内容

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
        '/static/js/supplier_validation.js',
    ]

    column_list = [
        'name', 'businessScope', 'address', 'contactPerson', 'operations'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'name': '名称',
        'businessScope': '经营范围',
        'address': '地址',
        'contactPerson': '联系人',
        'phone': '电话',
        'email': '邮件',
        'fax': '传真',
        'fileResourceUrl': '附件',
        'operations': '操作'
    }
    column_details_list = [
        'name', 'address', 'contactPerson',
        'phone', 'email', 'fax', 'businessScope', 'fileResourceUrl',
    ]
    column_searchable_list = ('name', 'contactPerson')
    form_overrides = {
        'fileResourceUrl': partial(AirmaterialFileuploadField),
    }

    support_flow = None

    one_line_columns = ['businessScope', 'fileResourceUrl']

    column_formatters = {
        'operations': normal_operation_formatter,
        'fileResourceUrl': accessory_formatter('fileResourceUrl'),
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.name.validators = [DataRequired()]
        return super(_SupplierView, self).validate_form(form)

    # 从数据库里以名称查询供应厂商信息以json返回
    @expose('/get_supplier_data_from_name/', methods=['GET'])
    def get_supplier_data_from_name(self):
        try:
            name = request.args.get('name')
            if name:
                item = Supplier.query.filter(
                    Supplier.name == name).first()
                data = [item.contactPerson, item.phone, item.fax,
                        item.email]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')


SupplierView = partial(
    _SupplierView, Supplier, name='供应商'
)
