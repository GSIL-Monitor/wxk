# coding: utf-8

from __future__ import unicode_literals

from flask_admin import expose
from flask import request, redirect, jsonify, flash, url_for
from functools import partial
import json

from wtforms import SelectField
from modules.flows import AirmaterialRecordFlow
from wtforms.validators import DataRequired, NumberRange, ValidationError
from modules.models.airmaterial.airmaterial_category import AirmaterialCategory
from modules.views.airmaterial.multi_select import MultiSelectView
from modules.views.column_formatter import checkbox_formater
from modules.flows.operations import Create
from modules.perms import ActionNeedPermission
from modules.models.airmaterial import (
    LendApplication, PurchaseApplication, LendApplicationMaterial,
    PurchaseMaterial, ReturnMaterial, DisassembleMaterial,
    AirMaterialStorageList)
from util.validators.data_unique import DataUniqueRequired
from.airmaterial_record import AirmaterialRecord
from modules.models.base import db


class _AirmaterialCategoryView(MultiSelectView):

    list_template = 'airmaterial_category/list.html'
    create_template = 'unvalidate/create.html'
    approve_edit_template = 'unvalidate/approve_edit.html'

    # 航材类别首页列表视图应显示的内容
    column_list = [
        'checkbox', 'name', 'category', 'partNumber',
        'applicableModel', 'unit', 'minStock', 'statusName'
    ]

    # 对应内容的中文翻译
    column_labels = {
        'partNumber': '件号',
        'name': '名称',
        'category': '类别',
        'minStock': '最低库存',
        'unit': '单位',
        'applicableModel': '适用机型',
        'statusName': '状态',
        'checkbox': '复选',
        'isOrNotHaveEffectiveDate': '是否有有效期',
        'isOrNotHavePeriodCheck': '是否有定期检查',
    }
    # 查看页面显示的详情
    column_details_list = [
        'partNumber', 'name',
        'category', 'minStock',
        'unit', 'applicableModel',
        'isOrNotHaveEffectiveDate',
        'isOrNotHavePeriodCheck',
    ]

    column_searchable_list = ('category', 'partNumber', 'name', 'statusName')

    support_flow = partial(AirmaterialRecordFlow, 'basic flow')

    form_overrides = {
        'category': partial(SelectField, choices=[
            ('一般航材', '一般航材'),
            ('工装设备', '工装设备'),
            ('消耗品', '消耗品'),
            ('化工品', '化工品'),
            ('时控件', '时控件'),
            ('时寿件', '时寿件'),
        ]),
        'applicableModel': partial(SelectField, choices=[
            ('运5B(D)', '运5B(D)'),
        ])
    }

    column_formatters = {
        'checkbox': checkbox_formater()
    }

    type_url = {
        'purchase': 'purchaseapplication.create_view',
        'lend': 'lendapplication.create_view'
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.partNumber.validators = [
                DataRequired(),
                DataUniqueRequired(
                    AirmaterialCategory, 'partNumber', message='该件号已经存在！')]
            form.name.validators = [DataRequired()]
            form.category.validators = [DataRequired()]
            if form.minStock.data is not None:
                form.minStock.validators = [
                    NumberRange(min=0, message="最低库存不能小于0")]
        return super(_AirmaterialCategoryView, self).validate_form(form)

    @expose('/get_from_partNumber/', methods=['GET'])
    def get_from_partNumber(self):
        try:
            part_number = request.args.get('pn')
            if part_number:
                item = AirmaterialCategory.query.filter(
                    AirmaterialCategory.partNumber == part_number).first()
                data = json.dumps([item.category, item.partNumber,
                                   item.name, item.unit,
                                   item.isOrNotHaveEffectiveDate,
                                   item.isOrNotHavePeriodCheck])
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_pn_from_ca/', methods=['GET'])
    def get_pn_from_ca(self):
        try:
            ca = request.args.get('ca')
            if ca:
                items = AirmaterialCategory.query.filter(AirmaterialCategory.category == ca).all()
                data = [item.partNumber for item in items]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    def delete_model(self, model):
        """
        对于要删除的航材添加一部认证，如果再采购、
        借入、退料、拆机、入库相关航材中使用过航材类别，则不能够进行删除
        """
        materials = [PurchaseMaterial, LendApplicationMaterial,
                     ReturnMaterial, DisassembleMaterial,
                     AirMaterialStorageList]
        for material in materials:
            pn = material.query.filter(
                material.partNumber == model.partNumber).first()
            if pn:
                flash('该航材已经被使用，不能删除', 'error')
                return False
        return super(_AirmaterialCategoryView, self).delete_model(model)

    @expose('/record_view/', methods=['GET'])
    def record_view(self):
        key = request.args.get('id', '')
        record = AirmaterialRecord(self)
        return record.record_list(key)


AirmaterialCategoryView = partial(
    _AirmaterialCategoryView, AirmaterialCategory, name='航材类别'
)
