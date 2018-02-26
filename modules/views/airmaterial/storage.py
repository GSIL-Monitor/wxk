# coding: utf-8

from __future__ import unicode_literals
import json
import re
from functools import partial
from copy import deepcopy

from flask_admin import expose
from flask import redirect, request, flash, jsonify
from flask_admin.form import FormOpts
from collections import OrderedDict
from flask_admin.babel import gettext
from wtforms import DateField
from flask_admin.helpers import get_redirect_target
from flask_weasyprint import HTML, render_pdf
from flask_admin.helpers import get_form_data

from modules.flows import StorageFlow
from modules.flows.operations import Edit, Finish, Create
from modules.views.operations import ActionNeedPermission
from wtforms.validators import DataRequired
from modules.views.custom import ActionViewCfg
from util.widgets import DateWidget
from modules.models.airmaterial.storage import Storage, StorageList
from modules.models.airmaterial import (
    PurchaseApplication, LendApplication, ReturnMaterialOrder, Supplier,
    DisassembleOrder, RepairReturnOrder, LoanReturnOrder, Manufacturer,
    AirmaterialCategory
)
from .inline_table import InlineTable
from modules.views import CustomView
from util.exception import BackendServiceError
from modules.models.airmaterial.storage_action import *
from airmaterial_fileds import *
from modules.views.column_formatter import accessory_formatter
from util.fields.accessory_filed import StorageOrOutPutMulitFileuploadField


class _StorageView(InlineTable, CustomView):

    list_template = 'storage/list.html'
    pdf_template = 'storage/pdf.html'

    # 入库首页列表视图应显示的内容
    column_list = [
        'number', 'date', 'instoreCategory', 'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '日期',
        'instoreCategory': '入库类别',
        'instorageDate': '入库日期',
        'remark': '备注',
        'statusName': '状态',
        'accessory': '附件',
        'name': '名称',
        'category': '类别',
        'quantity': '数量',
        'partNumber': '件号',
        'storehouse': '仓库',
        'shelf': '架位'
    }
    support_flow = partial(StorageFlow, 'storage flow')
    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'instorageDate': partial(DateField, widget=DateWidget()),
        'accessory': partial(StorageOrOutPutMulitFileuploadField),
    }

    one_line_columns = ['accessory']

    inline_model = StorageList
    inline_column = 'storage_id'
    column_export_list = [
        'category', 'partNumber', 'name', 'quantity', 'storehouse',
        'shelf']

    column_details_list = [
        'number', 'date', 'instoreCategory', 'instorageDate', 'remark', 'accessory',
    ]
    column_searchable_list = ('instoreCategory', 'number', 'statusName')

    can_extra = False

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
        '/static/js/upload_file.js',
        '/static/js/select_planeType.js',
        '/static/js/inline_table.js',
        '/static/js/numbro.js',
        '/static/js/languages.js',
        '/static/js/zh-CN.min.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/moment.min.js',
        '/static/js/pikaday.js',
        '/static/js/pikaday-zh.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/storage_validation.js',
    ]

    extra_css = [
        '/static/css/datepicker.css',
        '/static/css/bootstrap-datetimepicker.min.css',
        '/static/css/jquery-ui.css',
        '/static/css/pikaday.css',
        '/static/css/dateHeight.css',
    ]

    types_dict = {
        'CGSQ': [PurchaseApplication, 'purchase'],
        'JRSQ': [LendApplication, 'lendApplicationMaterials'],
        'TLD2': [ReturnMaterialOrder, 'returnMaterials'],
        'SXGH': [RepairReturnOrder, 'repairReturnMaterials'],
        'JCGH': [LoanReturnOrder, 'loanReturnMaterials'],
        'CJD2': [DisassembleOrder, 'disassembleMaterials'],
    }

    base_table_columns = [
        ('category', AM_CATEGORY),
        ('partNumber', AM_PARTNUMBER),
        ('serialNum', AM_SERIALNUM),
        ('name', AM_NAME),
        ('quantity', AM_QUANTITY),
        ('unitPrice', AM_UNITPRICE),
        ('unit', AM_UNIT),
        ('applicableModel', AM_APPLICABLEMODEL),
        ('storehouse', AM_STOREHOUSE),
        ('shelf', AM_SHELF),
        ('flyTime', AM_FLYTIME),
        ('engineTime', AM_ENGINETIME),
        ('flightTimes', AM_FLIGHTTIMES),
        ('effectiveDate', AM_EFFECTIVEDATE),
        ('lastCheckDate', AM_LASTCHECKDATE),
        ('nextCheckDate', AM_NEXTCHECKDATE),
        ('certificateNum', AM_CERTIFICATENUM),
        ('airworthinessTagNum', AM_AIRWORTHINESSTAGNUM),
        ('manufacturer', AM_MANUFACTURER),
        ('supplier', AM_SUPPLIER),
    ]

    base_d_r_table_columns = [
        ('category', AM_CATEGORY),
        ('partNumber', AM_PARTNUMBER),
        ('serialNum', AM_SERIALNUM),
        ('name', AM_NAME),
        ('quantity', AM_QUANTITY),
        ('unitPrice', AM_UNITPRICE),
        ('unit', AM_UNIT),
        ('applicableModel', AM_APPLICABLEMODEL),
        ('storehouse', AM_STOREHOUSE),
        ('shelf', AM_SHELF),
        ('flyTime', AM_FLYTIME),
        ('engineTime', AM_ENGINETIME),
        ('flightTimes', AM_FLIGHTTIMES),
        ('effectiveDate', AM_EFFECTIVEDATE),
        ('lastCheckDate', AM_LASTCHECKDATE),
        ('nextCheckDate', AM_NEXTCHECKDATE),
        ('certificateNum', AM_CERTIFICATENUM),
        ('disassembleDate', AM_DISASSEMBLEDATE),
        ('airworthinessTagNum', AM_AIRWORTHINESSTAGNUM),
        ('manufacturer', AM_MANUFACTURER),
        ('supplier', AM_SUPPLIER),
    ]

    # 采购申请入库单
    purchase_table_columns = OrderedDict(base_table_columns)
    # 退料入库单
    return_material_table_columns = deepcopy(base_table_columns)
    return_material_table_columns.extend([('checkInstruction', AM_CHECKINSTRUCTION)])
    return_material_table_columns = OrderedDict(return_material_table_columns)
    # 拆机入库
    disassemble_table_columns = deepcopy(base_d_r_table_columns)
    disassemble_table_columns.extend([('planeNum', AM_DISPLANENUM)])
    disassemble_table_columns = OrderedDict(disassemble_table_columns)
    # 送修归还入库
    repair_return_table_columns = deepcopy(base_d_r_table_columns)
    repair_return_table_columns.extend([('checkInstruction', AM_CHECKINSTRUCTION)])
    repair_return_table_columns = OrderedDict(repair_return_table_columns)
    # 借入入库
    lend_table_columns = purchase_table_columns
    # 借出归还入库
    loan_return_table_columns = purchase_table_columns
    # 先给一个默认值
    table_columns = purchase_table_columns
    inst_foreign_model = None

    form_excluded_columns = [
        'statusName', 'borrow', 'loanReturn', 'disassemble', 'returnMaterial',
        'purchaseApplication', 'repairReturnOrder', 'storageList'
    ]


    column_formatters = {
        'accessory': accessory_formatter('accessory'),
    }

    @property
    def form_widget_args(self):
        return {
            'instoreCategory': {
                'readonly': True,
            },
            'number': {
                'readonly': True
            },

        }

    def __init__(self, *args, **kwargs):

        self.relationField = 'storageList'
        self.f_key = 'storage_id'
        self.relationModel = StorageList

        super(_StorageView, self).__init__(*args, **kwargs)

    def init_table_columns(self, whichcolumns):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)
            table_columns[i]['need'] = False
        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = [
            '一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件']
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = True
        table_columns[1]['need'] = True
        table_columns[3]['need'] = True
        table_columns[3]['readOnly'] = True
        table_columns[4]['type'] = 'numeric'
        table_columns[4]['format'] = '0'
        table_columns[4]['need'] = True
        table_columns[5]['type'] = 'numeric'
        table_columns[5]['format'] = '0.00'
        table_columns[7]['editor'] = 'select'
        table_columns[7]['selectOptions'] = [self.plane_type]
        table_columns[7]['need'] = True
        table_columns[8]['need'] = True
        table_columns[9]['need'] = True
        table_columns[10]['validator'] = 'hhmm'
        table_columns[10]['format'] = '00:00'
        table_columns[11]['validator'] = 'hhmm'
        table_columns[11]['format'] = '00:00'
        table_columns[12]['type'] = 'numeric'
        table_columns[12]['format'] = '0'
        table_columns[13]['type'] = 'date'
        table_columns[13]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[13]['checkNeed'] = True
        table_columns[14]['type'] = 'date'
        table_columns[14]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[15]['type'] = 'date'
        table_columns[15]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[15]['checkNeed'] = True
        table_columns[19]['editor'] = 'select'
        table_columns[19]['selectOptions'] = [m.name for m in Supplier.query.all()]

        if whichcolumns in [disassembleStore, repairReturnStore]:
            table_columns[19]['editor'] = 'select'
            table_columns[19]['selectOptions'] = [m.name for m in Manufacturer.query.all()]
            table_columns[20]['editor'] = 'select'
            table_columns[20]['selectOptions'] = [m.name for m in Supplier.query.all()]
            table_columns[17]['type'] = 'date'
            table_columns[17]['dateFormat'] = 'YYYY-MM-DD'
            if whichcolumns == disassembleStore:
                table_columns[17]['need'] = True
        else:
            table_columns[18]['editor'] = 'select'
            table_columns[18]['selectOptions'] = [m.name for m in Manufacturer.query.all()]
        if whichcolumns in [repairReturnStore]:
            table_columns[21]['need'] = True
        if whichcolumns in [disassembleStore]:
            table_columns[21]['readOnly'] = True
        if whichcolumns in [retrunMaterialStore]:
            table_columns[20]['need'] = True
        if whichcolumns in [purchaseStore]:
            table_columns[10]['need'] = True
            table_columns[11]['need'] = True
            table_columns[12]['need'] = True

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/storage_table.js',
        })

        return json.dumps(table_columns)

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.instorageDate.validators = [DataRequired()]
            form.instoreCategory.validators = [DataRequired()]
        return super(_StorageView, self).validate_form(form)

    def on_model_change(self, form, model, is_created):
        category = {
            PurchaseSTORE: 'purchaseApplication',
            LendSTORE: 'borrow',
            LoanReturnSTORE: 'loanReturn',
            RepairReturnSTORE: 'repairReturnOrder',
            ReturnMaterialSTORE: 'returnMaterial',
            DisassembleSTORE: 'disassemble',
        }
        if is_created and model.instoreCategory in category.keys():
            setattr(model, category[model.instoreCategory], self.inst_foreign_model)
        super(_StorageView, self).on_model_change(form, model, is_created)

    def set_default(self, table, name, model, ao_id, columns, field, related):
        instore_isnt = getattr(self._create_form_class, 'instoreCategory')
        self.table_columns = table
        instore_isnt.kwargs['default'] = name
        inst_model = model.query.filter(model.id == ao_id).first()
        if not inst_model:
            return([], related)
        datas = []
        if not getattr(inst_model, field):
            return ([], related)

        for val in getattr(inst_model, field):
            data = []
            if val.category in ['一般航材', '时控件', '时寿件']:
                for i in range(0, val.quantity):
                    for k in columns:
                        # 对第8个机型添加默认值'Y5B(D)'
                        if len(data) == 7:
                            data.append(self.plane_type)
                            continue
                        if len(data) in [10, 11]:
                            try:
                                data.append(getattr(val, k))
                            except:
                                data.append('00:00')
                            continue
                        if not k:
                            data.append(k)
                            continue
                        if k == 'disassembleDate':
                            if getattr(inst_model, 'disassembleDate'):
                                data.append(inst_model.disassembleDate)
                            continue
                        if k == 'supplier':
                            if getattr(inst_model, 'supplier'):
                                data.append(inst_model.supplier)
                            continue
                        if k not in ['unit', 'quantity']:
                            data.append(getattr(val, k))
                            continue
                        if k == 'unit':
                            pn = getattr(val, 'partNumber')
                            ac = AirmaterialCategory.query.filter_by(
                                partNumber=pn).first()
                            if ac:
                                data.append(ac.unit)
                            else:
                                data.append(None)
                            continue
                        data.append(1)
                    datas.append(data)
                    data = []
                continue
            for k in columns:
                # 对第八个数据机型添加默认值'Y5B(D)'
                if len(data) == 7:
                    data.append(self.plane_type)
                    continue
                if len(data) in [10, 11]:
                    try:
                        data.append(getattr(val, k))
                    except:
                        data.append('00:00')
                    continue
                if not k:
                    data.append(k)
                    continue
                if k == 'disassembleDate':
                    if getattr(inst_model, 'disassembleDate'):
                        data.append(inst_model.disassembleDate)
                    continue
                if k == 'supplier':
                    if getattr(inst_model, 'supplier'):
                        data.append(inst_model.supplier)
                    continue
                if k != 'unit':
                    data.append(getattr(val, k))
                    continue
                pn = getattr(val, 'partNumber')
                ac = AirmaterialCategory.query.filter_by(
                    partNumber=pn).first()
                if ac:
                    data.append(ac.unit)
                else:
                    data.append(None)
            datas.append(data)
        datas = json.dumps(datas)
        self.inst_foreign_model = inst_model

        return (datas, related)

    def create_storge_list(self, model_name=None, ao_id=None):
        if not model_name and not ao_id:
            model_name = request.args.get('model', '')
            ao_id = request.args.get('id', '')
        table_datas = json.dumps([])
        if ao_id and model_name:
            if 'CGSQ' in model_name:
                columns = [
                    'category', 'partNumber', None, 'name', 'quantity',
                    'unitPrice', 'unit', None, None, None, 'flyTime', 0, 0, None, None,
                    None, None, None, 'manufacturer', 'supplier',
                ]
                return self.set_default(self.purchase_table_columns,
                                        PurchaseSTORE, PurchaseApplication,
                                        ao_id, columns, 'purchase',
                                        purchaseStore)

            if 'JRSQ' in model_name:
                columns = [
                    'category', 'partNumber', None, 'name', 'quantity', None,
                    'unit', None, None, None, 0, 0, 0,
                ]
                return self.set_default(self.lend_table_columns,
                                        LendSTORE, LendApplication,
                                        ao_id, columns,
                                        'lendApplicationMaterials',
                                        lendStore)

            if 'TLD' in model_name:
                columns = [
                    'category', 'partNumber', 'serialNum', 'name',
                    'quantity', None, 'unit', None, None, None, 0, 0, 0
                ]
                return self.set_default(self.return_material_table_columns,
                                        ReturnMaterialSTORE,
                                        ReturnMaterialOrder,
                                        ao_id, columns,
                                        'returnMaterials',
                                        retrunMaterialStore)

            if 'CJD' in model_name:

                columns = [
                    'category', 'partNumber', 'serialNum', 'name', 'quantity',
                    None, 'unit', None, None, None, 'flyTime', 'engineTime',
                    'flightTimes', 'effectiveDate', 'lastCheckDate', 'nextCheckDate',
                    None, 'disassembleDate', None, 'manufacturer', None, 'planeNum',
                ]
                return self.set_default(self.disassemble_table_columns,
                                        DisassembleSTORE,
                                        DisassembleOrder,
                                        ao_id, columns,
                                        'disassembleMaterials',
                                        disassembleStore)

            if 'SXGH' in model_name:
                columns = [
                    'category', 'partNumber', 'serialNum', 'name', 'quantity',
                    None, 'unit', None, None, None, 'flyTime', 'engineTime',
                    'flightTimes', None, 'lastCheckDate', None, None, None,
                    None, 'manufacturer'
                ]
                return self.set_default(self.repair_return_table_columns,
                                        RepairReturnSTORE,
                                        RepairReturnOrder,
                                        ao_id, columns,
                                        'repairReturnMaterials',
                                        repairReturnStore)

            if 'JCGH' in model_name:
                columns = [
                    'category', 'partNumber', 'serialNum', 'name', 'quantity',
                    None, 'unit', None, None, None, 'flyTime', 'engineTime',
                    'flightTimes', None, 'lastCheckDate', None, None, None,
                    'manufacturer'
                ]
                return self.set_default(self.loan_return_table_columns,
                                        LoanReturnSTORE,
                                        LoanReturnOrder,
                                        ao_id, columns,
                                        'loanReturnMaterials',
                                        loanReturnStore)
        # 如果不是通过别的申请创建 则返回空值
        return (table_datas, '')

    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        if request.method == 'GET':
            ret = self.create_storge_list()
            self._template_args.update({
                'table_columns': self.init_table_columns(ret[1]),
                'table_datas': ret[0],
            })
        else:
            request_str = request.headers['Referer']
            modelName = re.findall(r"model=(.+?)&", request_str)[0]
            action_id = None
            for val in request_str.split('&'):
                if 'id=' in val:
                    action_id = val.split('=')[1]
                    break
            # action_id = re.findall(r"&id=(.+?)", request_str)[0]
            self.create_storge_list(model_name=modelName, ao_id=action_id)
        # 处理加入入库按钮
        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_create:
            return redirect(return_url)
        form = self.create_form()
        model_name = request.args.get('model', '')
        if request.method == 'GET':
            self.get_accessory_from_before(form, model_name, self.types_dict)

        self.get_edit_details_view_colums(form.instoreCategory.data)
        if not hasattr(form, '_validated_ruleset') or not \
                form._validated_ruleset:
            self._validate_form_instance(
                ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            model = self.create_model(form)
            if model:
                flash(gettext('Record was successfully created.'), 'success')
                return redirect(self.get_save_return_url(
                    model, is_created=True))

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_create_rules)
        if self.create_modal and request.args.get('modal'):
            template = self.create_modal_template
        else:
            template = self.create_template

        perm = ActionNeedPermission('storage', Finish)
        refuse_op = ('入库', Finish) if perm.can() else None
        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        details_columns = self.get_column_names(
            self.review_details_columns or self.column_details_list, None)

        cfg = ActionViewCfg(
            '', 'fa-bell-o', None, ('保存', Create), ('入库', Finish))

        return self.render(
            template,
            action=self.get_url('.create_view', verb='creat'),
            details_columns=details_columns,
            get_value=self.get_list_value,
            return_url=return_url,
            cancel_url=return_url,
            action_name=cfg.action_name,
            icon_value=cfg.icon_value,
            form=form,
            agreed=cfg.agreed,
            refuse=refuse_op,
            form_opts=form_opts,
            one_line_columns=self.one_line_columns
        )

    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        ao_id = request.args.get('id', '')
        return_url = get_redirect_target() or self.get_url('.index_view')
        model = Storage.query.filter_by(id=ao_id).first()
        if not self.can_edit:
            return redirect(return_url)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)
        column = self.get_edit_details_view_colums(model.instoreCategory)
        self._template_args.update({
            'table_columns': self.init_table_columns(column),
            'table_datas': self.get_table_data_from_db(model),
        })
        model_id = model.id
        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not\
                form._validated_ruleset:
            self._validate_form_instance(
                ruleset=self._form_edit_rules, form=form)
        if self.validate_form(form):
            if self.update_model(form, model):
                if request.method == 'POST' and self.support_flow:
                    self._custom_action(model, request.form)
                flash(gettext('Record was successfully saved.'), 'success')
                return redirect(self.get_save_return_url(model,
                                                         is_created=False))

        perm = ActionNeedPermission('storage', Finish)
        refuse_op = ('入库', Finish) if perm.can() else None
        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        details_columns = self.get_column_names(
            self.review_details_columns or self.column_details_list, None)

        cfg = ActionViewCfg(
            '', 'fa-bell-o', None, ('保存', Edit), ('入库', Finish))

        return self.render(
            self.approve_edit_template,
            action=self.get_url('.approve_edit_view',
                                verb='edit', id=model_id),
            model=model,
            details_columns=details_columns,
            get_value=self.get_list_value,
            return_url=return_url,
            cancel_url=return_url,
            action_name=cfg.action_name,
            icon_value=cfg.icon_value,
            form=form,
            agreed=cfg.agreed,
            refuse=refuse_op,
            form_opts=form_opts,
            model_id=model_id,
            one_line_columns=self.one_line_columns
        )

    def get_edit_details_view_colums(self, instore_category):
        column = ''
        if instore_category == PurchaseSTORE:
            self.table_columns = self.purchase_table_columns
            column = purchaseStore
        elif instore_category == LendSTORE:
            self.table_columns = self.lend_table_columns
            column = lendStore
        elif instore_category == ReturnMaterialSTORE:
            self.table_columns = self.return_material_table_columns
            column = retrunMaterialStore
        elif instore_category == DisassembleSTORE:
            self.table_columns = self.disassemble_table_columns
            column = disassembleStore
        elif instore_category == RepairReturnSTORE:
            self.table_columns = self.repair_return_table_columns
            column = repairReturnStore
        elif instore_category == LoanReturnSTORE:
            self.table_columns = self.loan_return_table_columns
            column = loanReturnStore

        return column

    @expose('/details/')
    def details_view(self):
        ao_id = request.args.get('id', '')
        inst_model = Storage.query.filter_by(id=ao_id).first()
        if not inst_model or not ao_id:
            raise BackendServiceError('')
        column = self.get_edit_details_view_colums(inst_model.instoreCategory)
        self._template_args.update({
            'table_columns': self.get_readonly_table(column),
            'table_datas': self.get_table_data_from_db(inst_model),
            'extra_table_js': 'js/inline_table_details.js'
        })
        return super(_StorageView, self).details_view()

    def get_readonly_table(self, which_columns=None):
        table_columns = json.loads(self.init_table_columns(which_columns))
        for column in table_columns:
            column.update({'readOnly': True})
        return json.dumps(table_columns)

    @expose('/get_pn_from_types/', methods=['GET'])
    def get_pn_from_types(self):
        try:
            types = request.args.get('storage_type')
            if types:
                type_letter = types[:4]
                if type_letter in self.types_dict:
                    inst = self.types_dict[type_letter][0].query.filter_by(number=types).first()
                    materials = getattr(inst, self.types_dict[type_letter][1])
                    data = {}
                    for material in materials:
                        if material.category in data:
                            data[material.category].append(material.partNumber)
                        else:
                            data.update({material.category: [material.partNumber]})
                    data = json.dumps(data)
                    return jsonify(code=200, data=data, message='Ok')
                else:
                    raise Exception
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')

    @expose('get_pn_from_id', methods=['GET'])
    def get_pn_from_id(self):
        try:
            ids = request.args.get('id')
            if ids:
                cate_dict = {
                    LendSTORE: ['lendApplication', 'lendApplicationMaterials'],
                    LoanReturnSTORE: ['loanReturnOrder', 'loanReturnMaterials'],
                    DisassembleSTORE: ['disassembleOrder', 'disassembleMaterials'],
                    ReturnMaterialSTORE: ['returnMaterialOrder', 'returnMaterials'],
                    RepairReturnSTORE: ['repairReturnOrder', 'repairReturnMaterials'],
                    PurchaseSTORE: ['purchaseApplication', 'purchase'],
                }
                inst = Storage.query.filter_by(id=ids).first()
                cate = inst.instoreCategory
                application = getattr(inst, cate_dict[cate][0])
                materials = getattr(application, cate_dict[cate][1])
                data = {}
                for material in materials:
                    if material.category in data:
                        data[material.category].append(material.partNumber)
                    else:
                        data.update({material.category: [material.partNumber]})
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')

    @expose('/pdf/')
    def pdf_view(self):
        inst_id = request.args.get('id', '')
        inst = self.model.query.filter(self.model.id == inst_id).first()
        extra = {'name': inst.instoreCategory}
        return render_pdf(HTML(string=self._view_handler(self.pdf_template,
                                                         inst_id,
                                                         True,
                                                         **extra)))


StorageView = partial(
    _StorageView, Storage, name='入库'
)
