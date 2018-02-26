# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from copy import deepcopy
import time

import json
import re
from flask_admin import expose
from flask import redirect, request, flash
from collections import OrderedDict
from flask_admin.contrib.sqla import form
from flask_admin.form import FormOpts
from flask_admin.babel import gettext
from wtforms import SelectField, DateField
from flask_admin.helpers import get_form_data
from flask_admin.helpers import get_redirect_target
from flask_weasyprint import HTML, render_pdf

from modules.flows import PutOutStoreFlow
from modules.flows.operations import Edit, Finish, Create
from modules.views.operations import ActionNeedPermission
from wtforms.validators import DataRequired
from modules.views.custom import ActionViewCfg
from util.widgets import DateWidget
from modules.models.airmaterial.put_out_store import PutOutStoreModel
from modules.models.airmaterial import (
    LoanApplicationOrder, BorrowingInReturnModel, AssembleApplication,
    RepairApplication, Scrap, PutOutStoreMaterial, Supplier, Manufacturer
)
from modules.views import CustomView
from .with_inline_table import WithInlineTableView
from util.exception import BackendServiceError
from modules.models.airmaterial.storage_action import *
from airmaterial_fileds import *
from modules.views.column_formatter import accessory_formatter
from util.fields.accessory_filed import StorageOrOutPutMulitFileuploadField


class _PutOutStoreView(WithInlineTableView):
    # 出库列表视图应显示的内容
    list_template = 'out_storage/list.html'
    column_list = [
        'number', 'date', 'outStoreCategory', 'statusName',
    ]
    pdf_template = 'storage/pdf.html'

    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'outDate': '出库日期',
        'date': '日期',
        'outStoreCategory': '出库类别',
        'loanCategory': '借出类型',
        'borrowCompany': '借用单位',
        'statusName': '状态',
        'remark': '备注',
        'accessory': '附件',
        'companyAddr': '单位地址',
        'contactPerson': '联系人',
        'telephone': '电话',
        'fax': '传真',
        'mailbox': '邮箱',
        'name': '名称',
        'category': '类别',
        'quantity': '数量',
        'partNumber': '件号',

    }
    column_searchable_list = ('outStoreCategory', 'number', 'statusName')

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
        '/static/js/inline_table.js',
        '/static/js/numbro.js',
        '/static/js/languages.js',
        '/static/js/zh-CN.min.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/moment.min.js',
        '/static/js/pikaday.js',
        '/static/js/pikaday-zh.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/put_out_validate.js',
    ]

    extra_css = [
        '/static/css/datepicker.css',
        '/static/css/bootstrap-datetimepicker.min.css',
        '/static/css/jquery-ui.css',
        '/static/css/pikaday.css',
    ]
    can_extra = False

    one_line_columns = ['accessory']

    inline_model = PutOutStoreMaterial
    inline_column = 'putOutStorage_id'
    column_export_list = [
        'category', 'partNumber', 'name', 'quantity']

    support_flow = partial(PutOutStoreFlow, 'put out store flow')
    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'outDate': partial(DateField, widget=DateWidget()),
        'loanCategory': partial(SelectField, choices=[
            ('一般', '一般'),
            ('重要', '重要'),
        ]),
        'accessory': partial(StorageOrOutPutMulitFileuploadField),
    }

    column_formatters = {
        'accessory': accessory_formatter('accessory'),
    }

    column_details_list = [
        'number', 'outDate', 'date', 'outStoreCategory',
        'loanCategory', 'borrowCompany', 'companyAddr',
        'contactPerson', 'telephone', 'fax',
        'mailbox', 'remark', 'accessory'
    ]

    base_table_columns = [
        ('category', AM_CATEGORY), ('partNumber', AM_PARTNUMBER), ('serialNum', AM_SERIALNUM),
        ('name', AM_NAME), ('quantity', AM_QUANTITY),
    ]

    types_dict = {
        'JCSQ': [LoanApplicationOrder],
        'JRGH': [BorrowingInReturnModel],
        'ZJSQ': [AssembleApplication],
        'BFSQ': [Scrap],
        'SXSQ': [RepairApplication],
    }

    # 下面五项为五种出库类型的表体内容
    # 借出出库
    loan_table_columns = deepcopy(base_table_columns)
    loan_table_columns.extend([
        ('manufacturer', AM_MANUFACTURER), ('supplier', AM_SUPPLIER), ('effectiveDate', AM_EFFECTIVEDATE),
        ('lastCheckDate', AM_LASTCHECKDATE), ('nextCheckDate', AM_NEXTCHECKDATE),
        ('flyTime', AM_FLYTIME), ('engineTime', AM_ENGINETIME), ('flightTimes', AM_FLIGHTTIMES),
        ('unit', AM_UNIT),
    ])
    loan_table_columns = OrderedDict(loan_table_columns)
    # 借入归还出库
    borrow_return_table_columns = deepcopy(base_table_columns)
    borrow_return_table_columns.extend([
        ('manufacturer', AM_MANUFACTURER), ('supplier', AM_SUPPLIER), ('effectiveDate', AM_EFFECTIVEDATE),
        ('flyTime', AM_FLYTIME), ('engineTime', AM_ENGINETIME), ('flightTimes', AM_FLIGHTTIMES),
        ('lastCheckDate', AM_LASTCHECKDATE), ('nextCheckDate', AM_NEXTCHECKDATE),
    ])
    borrow_return_table_columns = OrderedDict(borrow_return_table_columns)
    # 装机出库
    assemble_table_columns = deepcopy(base_table_columns)
    assemble_table_columns.extend([
        ('manufacturer', AM_MANUFACTURER), ('supplier', AM_SUPPLIER), ('effectiveDate', AM_EFFECTIVEDATE),
        ('lastCheckDate', AM_LASTCHECKDATE), ('nextCheckDate', AM_NEXTCHECKDATE),
        ('flyTime', AM_FLYTIME), ('engineTime', AM_ENGINETIME), ('flightTimes', AM_FLIGHTTIMES),
        ('planeNum', AM_PLANENUM)
    ])
    assemble_table_columns = OrderedDict(assemble_table_columns)
    # 送修出库
    repair_table_columns = deepcopy(base_table_columns)
    repair_table_columns.extend([
        ('manufacturer', AM_MANUFACTURER), ('supplier', AM_SUPPLIER), ('effectiveDate', AM_EFFECTIVEDATE),
        ('flyTime', AM_FLYTIME), ('engineTime', AM_ENGINETIME), ('flightTimes', AM_FLIGHTTIMES),
        ('lastCheckDate', AM_LASTCHECKDATE), ('nextCheckDate', AM_NEXTCHECKDATE),
        ('planeNum', AM_PLANENUM), ('repairCompany', AM_REPAIRCOMPANY)
    ])
    repair_table_columns = OrderedDict(repair_table_columns)
    # 报废出库
    scrap_table_columns = deepcopy(base_table_columns)
    scrap_table_columns.extend([
        ('scrapReason', AM_SCRAPREASON), ('effectiveDate', AM_EFFECTIVEDATE),
        ('nextCheckDate', AM_NEXTCHECKDATE)
    ])
    scrap_table_columns = OrderedDict(scrap_table_columns)
    # 先给一个默认值
    table_columns = loan_table_columns
    inst_foreign_model = None
    # 下面表头所要剔除的内容
    common_exclude_list = [
        'loanCategory', 'borrowCompany', 'companyAddr',
        'contactPerson', 'telephone', 'fax', 'mailbox',
    ]

    form_excluded_columns = [
        'statusName', 'borrowingInReturn', 'loanApplication',
        'assembleApplication', 'scrap', 'repairApplication',
        'putOutStoreMaterials',
    ]

    @property
    def form_widget_args(self):
        return {
            'number': {
                'readonly': True,
            },
            'outStoreCategory': {
                'readonly': True,
            }

        }

    def __init__(self, *args, **kwargs):
        # 深拷贝一个详情，用于后续需要剔除字段的详情视图
        self.relationField = 'putOutStoreMaterials'
        self.f_key = 'putOutStorage_id'
        self.relationModel = PutOutStoreMaterial

        super(_PutOutStoreView, self).__init__(*args, **kwargs)
        self.tmp_columns = deepcopy(self.column_details_list)
        self.tmp_review_columns = deepcopy(self.review_details_columns)

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
        table_columns[0]['readOnly'] = True
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['readOnly'] = True
        table_columns[1]['need'] = True
        table_columns[2]['editor'] = 'select'
        table_columns[2]['selectOptions'] = []
        table_columns[2]['readOnly'] = True
        table_columns[3]['readOnly'] = True
        table_columns[3]['need'] = True
        table_columns[4]['type'] = 'numeric'
        table_columns[4]['format'] = '0'
        table_columns[4]['need'] = True

        if whichcolumns == borrowReturnOutStore:
            table_columns[5]['editor'] = 'select'
            table_columns[5]['selectOptions'] = self.get_manufacturer()
            table_columns[6]['editor'] = 'select'
            table_columns[6]['selectOptions'] = self.get_supplier()
            table_columns[7]['readOnly'] = True
            table_columns[7]['checkneed'] = True
            table_columns[8]['validator'] = 'hhmm'
            table_columns[9]['validator'] = 'hhmm'
            table_columns[10]['type'] = 'numeric'
            table_columns[10]['format'] = '0'
            table_columns[11]['type'] = 'date'
            table_columns[11]['dateFormat'] = 'YYYY-MM-DD'
            table_columns[12]['readOnly'] = True
            table_columns[12]['checkNeed'] = True
        if whichcolumns in [loanOutstore]:
            table_columns[5]['editor'] = 'select'
            table_columns[5]['selectOptions'] = self.get_manufacturer()
            table_columns[6]['editor'] = 'select'
            table_columns[6]['selectOptions'] = self.get_supplier()
            table_columns[7]['readOnly'] = True
            table_columns[7]['checkNeed'] = True
            table_columns[8]['type'] = 'date'
            table_columns[8]['dateFormat'] = 'YYYY-MM-DD'
            table_columns[9]['readOnly'] = True
            table_columns[9]['checkNeed'] = True
            table_columns[10]['validator'] = 'hhmm'
            table_columns[11]['validator'] = 'hhmm'
            table_columns[12]['type'] = 'numeric'
            table_columns[12]['format'] = '0'
        if whichcolumns in [assembleOutStore]:
            table_columns[5]['editor'] = 'select'
            table_columns[5]['selectOptions'] = self.get_manufacturer()
            table_columns[6]['editor'] = 'select'
            table_columns[6]['selectOptions'] = self.get_supplier()
            table_columns[7]['readOnly'] = True
            table_columns[7]['checkNeed'] = True
            table_columns[8]['type'] = 'date'
            table_columns[8]['dateFormat'] = 'YYYY-MM-DD'
            table_columns[9]['readOnly'] = True
            table_columns[9]['checkNeed'] = True
            table_columns[10]['validator'] = 'hhmm'
            table_columns[11]['validator'] = 'hhmm'
            table_columns[12]['type'] = 'numeric'
            table_columns[12]['format'] = '0'
            table_columns[13]['editor'] = 'select'
            table_columns[13]['selectOptions'] = self.get_aircraft()
            table_columns[13]['need'] = True
        if whichcolumns in [repairOutStore]:
            table_columns[5]['editor'] = 'select'
            table_columns[5]['selectOptions'] = self.get_manufacturer()
            table_columns[6]['editor'] = 'select'
            table_columns[6]['selectOptions'] = self.get_supplier()
            table_columns[7]['readOnly'] = True
            table_columns[7]['checkneed'] = True
            table_columns[8]['validator'] = 'hhmm'
            table_columns[9]['validator'] = 'hhmm'
            table_columns[10]['type'] = 'numeric'
            table_columns[10]['format'] = '0'
            table_columns[11]['type'] = 'date'
            table_columns[11]['dateFormat'] = 'YYYY-MM-DD'
            table_columns[12]['readOnly'] = True
            table_columns[12]['checkNeed'] = True
            table_columns[12]['need'] = False
            table_columns[13]['editor'] = 'select'
            table_columns[13]['selectOptions'] = self.get_aircraft()
            table_columns[14]['editor'] = 'select'
            table_columns[14]['selectOptions'] = self.get_repair_supplier()

        if whichcolumns == scrapOutStore:
            table_columns[6]['readOnly'] = True
            table_columns[7]['readOnly'] = True

        self._template_args.update({
            'inline_table': True,
            'can_add_line': False,
            'can_del_line': True,
            'extra_table_js': 'js/put_out_store_table.js',
        })

        return json.dumps(table_columns)

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.outStoreCategory.validators = [DataRequired()]
            form.outDate.validators = [DataRequired()]
        return super(_PutOutStoreView, self).validate_form(form)

    def on_model_change(self, form, model, is_created):
        category = {
            LoanOutSTORE: 'loanApplication',
            BorrowReturnOutSTORE: 'borrowingInReturn',
            AssembleOutSTORE: 'assembleApplication',
            ScrapOutSTORE: 'scrap',
            RepairOutSTORE: 'repairApplication',
        }
        if is_created and model.outStoreCategory in category.keys():
            setattr(model, category[
                model.outStoreCategory], self.inst_foreign_model)
        super(_PutOutStoreView, self).on_model_change(form, model, is_created)

    def create_form(self, obj=None):
        ret = None
        model_name = request.args.get('model', '')
        if request.method == 'GET':
            ao_id = request.args.get('id', '')
            ret = self.creat_detail_view(ao_id=ao_id, create=True,
                                         storage_model=model_name)
        else:
            request_str = request.headers['Referer']
            modelName = re.findall(r"model=(.+?)&", request_str)[0]
            action_id = None
            for val in request_str.split('&'):
                if 'id=' in val:
                    action_id = val.split('=')[1]
                    break
            # action_id = ac_id if ''request_str.split('&id=')[1]
            ret = self.creat_detail_view(ao_id=action_id, create=True,
                                          storage_model=modelName)
        if ret:
            self._template_args.update({
                'table_columns': self.init_table_columns(ret[1]),
                'table_datas': ret[0],
            })
        self.get_accessory_from_before(
            self.get_create_form(), model_name, self.types_dict)
        return self._create_form_class(get_form_data(), obj=obj)

    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_create:
            return redirect(return_url)

        form = self.create_form()
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
        refuse_op = ('出库', Finish) if perm.can() else None
        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        details_columns = self.get_column_names(
            self.review_details_columns or self.column_details_list, None)

        cfg = ActionViewCfg(
            '', 'fa-bell-o', None, ('保存', Create), ('出库', Finish))

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

    def get_post_create_view_colums(self, outstore_category):
        category_to_columns = {
            LoanOutSTORE: self.loan_table_columns,
            BorrowReturnOutSTORE: self.borrow_return_table_columns,
            AssembleOutSTORE: self.assemble_table_columns,
            RepairOutSTORE: self.repair_table_columns,
            ScrapOutSTORE: self.scrap_table_columns,

        }
        if outstore_category in category_to_columns.keys():
            self.table_columns = category_to_columns[outstore_category]

    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        ao_id = request.args.get('id', '')
        return_url = get_redirect_target() or self.get_url('.index_view')
        model = PutOutStoreModel.query.filter_by(id=ao_id).first()
        if not self.can_edit:
            return redirect(return_url)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)
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
        refuse_op = ('出库', Finish) if perm.can() else None
        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        details_columns = self.get_column_names(
            self.review_details_columns or self.column_details_list, None)

        cfg = ActionViewCfg(
            '', 'fa-bell-o', None, ('保存', Edit), ('出库', Finish))

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

    @expose('/details/')
    def details_view(self):
        ao_id = request.args.get('id', '')
        inst_model = PutOutStoreModel.query.filter_by(id=ao_id).first()
        if not ao_id or not inst_model:
            raise BackendServiceError('')
        column = self.get_edit_details_view_colums(inst_model.outStoreCategory)
        self._template_args.update({
            'table_columns': self.get_readonly_table(column[0]),
            'table_datas': self.get_table_data_from_db(inst_model),
            'extra_table_js': 'js/inline_table_details.js'

        })
        self.creat_detail_view(exclude_list=column[2])
        return super(_PutOutStoreView, self).details_view()

    def get_readonly_table(self, which_columns=None):
        table_columns = json.loads(self.init_table_columns(which_columns))
        for column in table_columns:
            column.update({'readOnly': True})
        return json.dumps(table_columns)

    def edit_form(self, obj=None):
        ao_id = request.args.get('id', '')
        outStorageModel = PutOutStoreModel.query.filter_by(id=ao_id).first()
        des = self.get_edit_details_view_colums(
            outStorageModel.outStoreCategory)
        converter = self.model_form_converter(self.session, self)
        self._template_args.update({
            'table_columns': self.init_table_columns(des[0]),
            'table_datas': self.get_table_data_from_db(outStorageModel),
        })
        self._edit_form_class = form.get_form(
            self.model, converter,
            base_class=self.form_base_class,
            only=self.form_columns,
            exclude=des[1],
            field_args=self.form_args,
            ignore_hidden=self.ignore_hidden,
            extra_fields=self.form_extra_fields)
        return self._edit_form_class(get_form_data(), obj=obj)

    def get_edit_details_view_colums(self, outstore_category):
        column, tmp_excluded_columns = None, None
        tmp_excluded_columns = deepcopy(self.form_excluded_columns)
        detail_remove_list = []
        if outstore_category == LoanOutSTORE:
            self.table_columns = self.loan_table_columns
            column = loanOutstore
        else:
            detail_remove_list = self.common_exclude_list
        if outstore_category == BorrowReturnOutSTORE:
            tmp_excluded_columns.extend(self.common_exclude_list)
            self.table_columns = self.borrow_return_table_columns
            column = borrowReturnOutStore
        if outstore_category == AssembleOutSTORE:
            tmp_excluded_columns.extend(self.common_exclude_list)
            self.table_columns = self.assemble_table_columns
            column = assembleOutStore
        if outstore_category == RepairOutSTORE:
            tmp_excluded_columns.extend(self.common_exclude_list)
            self.table_columns = self.repair_table_columns
            column = repairOutStore
        if outstore_category == ScrapOutSTORE:
            tmp_excluded_columns.extend(self.common_exclude_list)
            self.table_columns = self.scrap_table_columns
            column = scrapOutStore
        return (column, tmp_excluded_columns, detail_remove_list)

    # 创建 新建和详细信息视图中的字段项
    def creat_detail_view(self, ao_id=None, create=False,
                          storage_model=None, exclude_list=None):
        self.review_details_columns = deepcopy(self.tmp_review_columns)
        if create:
            tmp_excluded_columns = deepcopy(self.form_excluded_columns)
            inst_model, tmp_model, des_model = None, None, None
            table_datas = json.dumps([])
            whichcolumn = None
            if ao_id and storage_model:
                if 'JCSQ' in storage_model:
                    tmp_model = LoanApplicationOrder
                    self.handle_exclude_list(tmp_excluded_columns)
                    self.table_columns = self.loan_table_columns
                    self._create_form_class.outStoreCategory.kwargs[
                        'default'] = LoanOutSTORE
                    des_model = LoanApplicationOrder.query.filter(
                        LoanApplicationOrder.id == ao_id).first()
                    table_datas = [[
                        inst.category, inst.partNumber, inst.serialNum,
                        inst.name, inst.quantity, inst.manufacturer, None,
                        inst.effectiveDate, inst.lastCheckDate, inst.nextCheckDate,
                        inst.flyTime, inst.engineTime, inst.flightTimes,
                    ] for inst in des_model.loanMaterials]
                    table_datas = json.dumps(table_datas)
                    whichcolumn = loanOutstore
                elif 'JRGH' in storage_model:
                    tmp_model = BorrowingInReturnModel
                    self.table_columns = self.borrow_return_table_columns
                    tmp_excluded_columns.extend(self.common_exclude_list)
                    self.handle_exclude_list(tmp_excluded_columns)
                    self._create_form_class.outStoreCategory.kwargs[
                        'default'] = BorrowReturnOutSTORE
                    des_model = BorrowingInReturnModel.query.filter(
                        BorrowingInReturnModel.id == ao_id).first()
                    table_datas = [[
                        inst.category, inst.partNumber, inst.serialNum,
                        inst.name, inst.quantity, None, None,
                        inst.effectiveDate, inst.flyTime,
                        inst.engineTime, inst.flightTimes,
                        inst.lastCheckDate, inst.nextCheckDate
                    ] for inst in des_model.borrowingInReturnMaterials]
                    table_datas = json.dumps(table_datas)
                    whichcolumn = borrowReturnOutStore
                elif 'ZJSQ' in storage_model:
                    tmp_model = AssembleApplication
                    self.table_columns = self.assemble_table_columns
                    tmp_excluded_columns.extend(self.common_exclude_list)
                    self.handle_exclude_list(tmp_excluded_columns)
                    self._create_form_class.outStoreCategory.kwargs[
                        'default'] = AssembleOutSTORE
                    des_model = AssembleApplication.query.filter(
                        AssembleApplication.id == ao_id).first()
                    table_datas = [[
                        inst.category, inst.partNumber, inst.serialNum,
                        inst.name, inst.quantity, inst.manufacturer, None,
                        inst.effectiveDate, inst.lastCheckDate,
                        inst.nextCheckDate, inst.flyTime,
                        inst.engineTime, inst.flightTimes, inst.planeNum,
                    ] for inst in des_model.assembleApplicationList]
                    table_datas = json.dumps(table_datas)
                    whichcolumn = assembleOutStore
                elif 'SXSQ' in storage_model:
                    tmp_model = RepairApplication
                    inst_model = tmp_model.query.filter(
                        tmp_model.id == ao_id).first()
                    self.table_columns = self.repair_table_columns
                    tmp_excluded_columns.extend(self.common_exclude_list)
                    self.handle_exclude_list(tmp_excluded_columns)
                    self._create_form_class.outStoreCategory.kwargs[
                        'default'] = RepairOutSTORE
                    des_model = RepairApplication.query.filter(
                        RepairApplication.id == ao_id).first()
                    table_datas = [[
                        inst.category, inst.partNumber, inst.serialNum,
                        inst.name, inst.quantity, inst.manufacturer, None,
                        inst.effectiveDate, inst.flyTime, inst.engineTime,
                        inst.flightTimes, inst.lastCheckDate, inst.nextCheckDate,
                        inst.planeNum, des_model.repairCompany
                    ] for inst in des_model.repairAppl]
                    table_datas = json.dumps(table_datas)
                    whichcolumn = repairOutStore
                elif 'BFSQ' in storage_model:
                    tmp_model = Scrap
                    self.table_columns = self.scrap_table_columns
                    tmp_excluded_columns.extend(self.common_exclude_list)
                    self.handle_exclude_list(tmp_excluded_columns)
                    self._create_form_class.outStoreCategory.kwargs[
                        'default'] = ScrapOutSTORE
                    des_model = Scrap.query.filter(
                        Scrap.id == ao_id).first()
                    table_datas = [[
                        inst.category, inst.partNumber, inst.serialNum,
                        inst.name, inst.quantity,None, inst.effectiveDate,
                        inst.nextCheckDate
                    ] for inst in des_model.scrapMaterial]
                    table_datas = json.dumps(table_datas)
                    whichcolumn = scrapOutStore
                else:
                    self.handle_exclude_list(tmp_excluded_columns)
                    return (table_datas, whichcolumn)
                self.inst_foreign_model = des_model
                inst_model = tmp_model.query.filter(
                    tmp_model.id == ao_id).first()
                if inst_model:
                    tem_list = list(set(self.review_details_columns) - set(
                        tmp_excluded_columns))
                    for key, value in inst_model.__dict__.iteritems():
                        if key not in tem_list:
                            continue
                        if key in ['remark', 'date', 'statusName', 'number']:
                            continue
                        tmp = getattr(self._create_form_class, key)
                        tmp.kwargs['default'] = value
                    return (table_datas, whichcolumn)
        else:
            self.normal_view()
            for val in exclude_list:
                if val in self.column_details_list:
                    self.column_details_list.remove(val)
                    self.review_details_columns.remove(val)

    def handle_exclude_list(self, tmp_excluded_columns):
        converter = self.model_form_converter(self.session, self)
        self._create_form_class =\
            form.get_form(self.model, converter,
                          base_class=self.form_base_class,
                          only=self.form_columns,
                          exclude=tmp_excluded_columns,
                          field_args=self.form_args,
                          ignore_hidden=self.ignore_hidden,
                          extra_fields=self.form_extra_fields)

    def normal_view(self):
        self.column_details_list = deepcopy(self.tmp_columns)

    def get_export_pdf_column(self, inst_id=None):
        inst = self.model.query.filter(self.model.id == inst_id).first()
        if inst.outStoreCategory != LoanOutSTORE:
            return self._export_columns
        columns = deepcopy(self._export_columns)
        columns.extend([('borrowCompany', '借用单位'), ('contactPerson', '联系人'),
                        ('telephone', '电话')])
        return columns

    @expose('/pdf/')
    def pdf_view(self):
        inst_id = request.args.get('id', '')
        inst = self.model.query.filter(self.model.id == inst_id).first()
        extra = {'name': inst.outStoreCategory}
        return render_pdf(HTML(string=self._view_handler(self.pdf_template,
                                                         inst_id,
                                                         True,
                                                         **extra)))


PutOutStoreView = partial(
    _PutOutStoreView, PutOutStoreModel, name='出库'
)
