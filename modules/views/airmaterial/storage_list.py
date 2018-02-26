# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from copy import deepcopy
import json
from flask_admin import expose
from flask import redirect, request, flash, jsonify
from flask_admin.form import FormOpts
from collections import OrderedDict
from flask_admin.babel import gettext
from wtforms import SelectField, DateField
from flask_admin.helpers import get_form_data
from flask_admin.contrib.sqla import form
from flask_admin.helpers import get_redirect_target
from sqlalchemy import and_

from modules.models.airmaterial import (AirMaterialStorageList,
                                        LoanApplicationOrder,
                                        AssembleApplication, Scrap,
                                        RepairApplication, BorrowingInReturnModel)
from modules.views.airmaterial.multi_select import MultiSelectView
from modules.perms import ActionNeedPermission
from modules.flows.operations import Create
from modules.views.column_formatter import checkbox_formater


class _AirMaterialStorageListView(MultiSelectView):

    list_template = 'storage_list/list.html'

    support_flow = False
    use_inheritance_operation = False
    can_export = True

    column_labels = {
        'category': '类型',
        'partNumber': '件号',
        'serialNum': '序号',
        'name': '名称',
        'quantity': '数量',
        'freezingQuantity': '冻结数量',
        'unit': '单位',
        'flyTime': '飞行小时',
        'engineTime': '发动机小时',
        'flightTimes': '起落架次',
        'applicableModel': '适用机型',
        'storehouse': '仓库',
        'minStock': '最低库存',
        'shelf': '架位',
        'effectiveDate': '库存有效日期',
        'certificateNum': '证书编号',
        'airworthinessTagNum': '适航标签号',
        'lastCheckDate': '上次检查日期',
        'nextCheckDate': '下次检查日期',
        'manufacturer': '生产厂商',
        'supplier': '供应商',
        'statusName': '状态值',
        'checkbox': '复选'
    }

    column_list = [
        'checkbox', 'category', 'partNumber', 'serialNum', 'name', 'quantity',
        'freezingQuantity', 'unit', 'flyTime', 'engineTime', 'flightTimes',
        'applicableModel',
        'storehouse', 'shelf', 'minStock', 'effectiveDate', 'certificateNum',
        'airworthinessTagNum', 'lastCheckDate', 'nextCheckDate',
        'manufacturer', 'supplier', 'statusName'
    ]

    column_formatters = {
        'checkbox': checkbox_formater(check_storage=True)
    }

    column_export_exclude_list = ['checkbox', 'statusName']

    type_url = {
        'loan': 'loanapplicationorder.create_view',
        'assembleapplication': 'assembleapplication.create_view',
        'scrap': 'scrap.create_view',
        'repair': 'repairapplication.create_view',
        'borrowing_return': 'borrowinginreturnmodel.create_view'
    }

    column_searchable_list = ('name', 'partNumber', 'category', 'serialNum',
                              'storehouse', 'statusName', 'shelf',
                              'certificateNum', 'airworthinessTagNum',
                              'manufacturer', 'supplier')

    @expose('/get_unique_serialnum/', methods=['GET'])
    def get_unique_serialnum(self):
        try:
            pn = request.args.get('pn')
            sn = request.args.get('sn')
            if pn:
                items = AirMaterialStorageList.query.filter(
                    and_(AirMaterialStorageList.partNumber == pn,
                         AirMaterialStorageList.serialNum == sn)).first()
                if items:
                    data = False
                else:
                    data = True
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_from_list_sn/', methods=['GET'])
    def get_from_list_sn(self):
        try:
            pn = request.args.get('pn')
            sn = request.args.get('sn')
            if sn and pn:
                if sn == 'null' or sn == '':
                    sn = None
                item = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == pn,
                    AirMaterialStorageList.serialNum == sn).first()
                data = json.dumps([item.category, item.partNumber,
                                   item.serialNum, item.name,
                                   item.manufacturer, item.quantity,
                                   item.flyTime, item.engineTime,
                                   item.flightTimes, item.lastCheckDate,
                                   item.nextCheckDate, item.unit,
                                   item.effectiveDate])
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_pn_from_list_ca/', methods=['GET'])
    def get_pn_from_list_ca(self):
        try:
            ca = request.args.get('ca')
            if ca:
                items = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.category == ca).all()
                data = []
                for item in items:
                    if item.quantity > item.freezingQuantity:
                        data.append(item.partNumber)

                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_sn_form_list_pn/', methods=['GET'])
    def get_sn_form_list_pn(self):
        try:
            pn = request.args.get('pn')
            act = request.args.get('act')
            if pn and act:
                items = AirMaterialStorageList.query.filter(
                        AirMaterialStorageList.partNumber == pn).all()
                if act == 'out':
                    data = [
                        item.serialNum for item in items
                        if item.quantity > item.freezingQuantity]
                elif act == 'in':
                    data = [item.serialNum for item in items]
                data = [item if item else '' for item in set(data)]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_max_quantity_from_list/', methods=['GET'])
    def get_max_quantity_from_list(self):
        try:
            ca = request.args.get('ca')
            pn = request.args.get('pn')
            sn = request.args.get('sn')
            if ca and pn:
                # 为空的sn转换为None
                if sn == 'null' or sn == '':
                    sn = None
                query = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == pn,
                    AirMaterialStorageList.serialNum == sn)
                item = query.first()
                max_quantity = item.quantity - item.freezingQuantity
                if max_quantity <= 0:
                    raise Exception('Bad Argument')
                return jsonify(code=200, data=max_quantity, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_date_from_list/', methods=['GET'])
    def get_date_from_list(self):
        try:
            A_M_slist = AirMaterialStorageList
            args_dict = request.args.to_dict()
            for key in args_dict.keys():
                if args_dict[key] == 'null' or args_dict[key] == '':
                    args_dict[key] = None
            if args_dict.get('pn') and args_dict.get('act'):
                if args_dict.get('act') == 'effect':
                    items = A_M_slist.query.filter(
                        A_M_slist.partNumber == args_dict.get('pn'),
                        A_M_slist.serialNum == args_dict.get('sn'))
                    if args_dict.get('nc'):
                        items = items.filter(
                            A_M_slist.nextCheckDate == args_dict.get('nc'))
                    data = [item.effectiveDate for item in items.all()]
                if args_dict.get('act') == 'nextcheck':
                    items = A_M_slist.query.filter(
                        A_M_slist.partNumber == args_dict.get('pn'),
                        A_M_slist.serialNum == args_dict.get('sn'))
                    if args_dict.get('ed'):
                        items = items.filter(
                            A_M_slist.effectiveDate == args_dict.get('ed'))
                    data = [item.nextCheckDate for item in items.all()]
                data.append(None)
                data = [item if item else '' for item in set(data)]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')


AirMaterialStorageListView = partial(
    _AirMaterialStorageListView, AirMaterialStorageList, name='库存列表')
