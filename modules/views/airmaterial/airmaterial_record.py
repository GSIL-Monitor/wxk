# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from flask import request, redirect, jsonify, flash
from flask_admin import expose
from flask import request

from modules.models.airmaterial.airmaterial_list import AirmaterialList
from modules.views import CustomView
from modules.models.airmaterial.storage_action import *
from modules.models.airmaterial import *
from modules.flows.states import AllOutStored, PartOutStored, AllInStored, PartInStored


#  库存列表
StorageListMaterial = '库存'


class AirmaterialRecord(object):
    # 航材首页列表视图应显示的内容

    page_size = 20

    columns_labels = {
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
        'shelf': '架位',
        'effectiveDate': '库存有效日期',
        'outDate': '出库日期',
        'assembleDate': '装机日期',
        'repairCompany': '维修厂商',
        'nextCheckDate': '下次检查日期',
        'manufacturer': '生产厂商',
        'supplier': '供应商',
        'instorageDate': '入库日期',
        'companyName': '单位名称',
        'planeNum': '飞机注册号',
        'borrowCompany': '单位名称',
        'repairCompany': '维修厂商'
    }


    tabs = [
        StorageListMaterial, PurchaseSTORE, LendSTORE, BorrowReturnOutSTORE,
        ReturnMaterialSTORE, DisassembleSTORE, AssembleOutSTORE,
        LoanOutSTORE, LoanReturnSTORE, RepairOutSTORE, RepairReturnSTORE,
        ScrapOutSTORE]

    air_map = {
        StorageListMaterial: {
            'columns': ['category', 'partNumber', 'serialNum', 'name',
                        'quantity', 'effectiveDate', 'freezingQuantity',
                        'flyTime', 'engineTime', 'flightTimes',
                        'nextCheckDate'],
            'model': AirMaterialStorageList,
            'inline_model': '',
            'inline_column': '',
            'category': '',
            'related': ''
        },
        PurchaseSTORE: {
            'columns': ['serialNum', 'name', 'instorageDate', 'supplier',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': PurchaseApplication,
            'inline_model': PurchaseMaterial,
            'inline_column': 'application_id',
            'category': 'in',
            'related': 'purchaseApplication_id'
        },
        LendSTORE: {
            'columns': ['serialNum', 'name', 'instorageDate', 'companyName',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': LendApplication,
            'inline_model': LendApplicationMaterial,
            'inline_column': 'lendApplication_id',
            'category': 'in',
            'related': 'borrow_id'
        },
        BorrowReturnOutSTORE: {
            'columns': ['serialNum', 'name', 'outDate', 'companyName',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': BorrowingInReturnModel,
            'inline_model': BorrowingInReturnMaterial,
            'inline_column': 'borrowInReturn_id',
            'category': 'out',
            'related': 'borrowingInReturn_id'
        },
        ReturnMaterialSTORE: {
            'columns': ['serialNum', 'name', 'instorageDate', 'nextCheckDate',
                        'quantity', 'effectiveDate', 'flyTime', 'engineTime', 'flightTimes'],
            'model': ReturnMaterialOrder,
            'inline_model': ReturnMaterial,
            'inline_column': 'application_id',
            'category': 'in',
            'related': 'returnMaterial_id'
        },
        DisassembleSTORE: {
            'columns': ['serialNum', 'name', 'instorageDate', 'planeNum',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': DisassembleOrder,
            'inline_model': DisassembleMaterial,
            'inline_column': 'disassembleOrder_id',
            'category': 'in',
            'related': 'disassemble_id'
        },
        AssembleOutSTORE: {
            'columns': ['serialNum', 'name', 'assembleDate', 'planeNum',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': Assemble,
            'inline_model': AssembleApplicationList,
            'inline_column': 'assemble_id',
            'category': 'out',
            'related': 'assemble_application_id'
        },
        LoanOutSTORE: {
            'columns': ['serialNum', 'name', 'outDate', 'borrowCompany',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': LoanApplicationOrder,
            'inline_model': LoanMaterial,
            'inline_column': 'loanApplication_id',
            'category': 'out',
            'related': 'loanApplication_id'
        },
        LoanReturnSTORE: {
            'columns': ['serialNum', 'name', 'instorageDate', 'borrowCompany',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': LoanReturnOrder,
            'inline_model': LoanReturnMaterial,
            'inline_column': 'loanReturnOrder_id',
            'category': 'in',
            'related': 'loanReturn_id'
        },
        RepairOutSTORE: {
            'columns': ['serialNum', 'name', 'outDate', 'repairCompany',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': RepairApplication,
            'inline_model': RepairMaterial,
            'inline_column': 'application_id',
            'category': 'out',
            'related': 'repair_application_id'
        },
        RepairReturnSTORE: {
            'columns': ['serialNum', 'name', 'instorageDate', 'repairCompany',
                        'quantity', 'effectiveDate', 'nextCheckDate',
                        'flyTime', 'engineTime', 'flightTimes'],
            'model': RepairReturnOrder,
            'inline_model': RepairReturnMaterial,
            'inline_column': 'application_id',
            'category': 'in',
            'related': 'repairReturn_id'
        },
        ScrapOutSTORE: {
            'columns': ['serialNum', 'name', 'outDate', 'effectiveDate',
                        'nextCheckDate', 'quantity', 'flyTime', 'engineTime',
                        'flightTimes'],
            'model': Scrap,
            'inline_model': ScrapMaterial,
            'inline_column': 'application_id',
            'category': 'out',
            'related': 'scrap_id'
        },
    }

    def __init__(self, view):
        self._view = view
        self.list_template = 'airmaterial_category/airmaterial_record.html'

    def formater_value(self, name, value):
        if not value:
            return ''
        return value

    def get_query(self, key, sub, page):

        inst = AirmaterialCategory.query.filter_by(id=key).first()

        item = self.air_map[sub]
        # 库存列表
        query = AirMaterialStorageList.query.filter(
            AirMaterialStorageList.category == inst.category,
            AirMaterialStorageList.partNumber == inst.partNumber).all()
        # 入库相关
        if item['category'] == 'in':
            query = StorageList.query.filter(
                StorageList.category == inst.category,
                StorageList.partNumber == inst.partNumber).join(
                    Storage,
                    StorageList.storage_id == Storage.id).filter(
                        Storage.instoreCategory == sub,
                        Storage.auditStatus.in_([AllInStored, PartInStored])).all()
        # 出库相关
        if item['category'] == 'out':
            query = PutOutStoreMaterial.query.filter(
                PutOutStoreMaterial.category == inst.category,
                PutOutStoreMaterial.partNumber == inst.partNumber).join(
                    PutOutStoreModel,
                    PutOutStoreMaterial.putOutStorage_id == PutOutStoreModel.id).filter(
                        PutOutStoreModel.outStoreCategory == sub,
                        PutOutStoreModel.auditStatus.in_([AllOutStored, PartOutStored])).all()

        return (len(query), query[page * self.page_size: self.page_size * (page + 1)])

    def get_value(self, model, name, sub):
        # 表体本身字段
        if name in model.__dict__.keys():
            return self.formater_value(name, getattr(model, name))

        item = self.air_map[sub]
        inst = None

        # 入库或出库单相关字段
        if item['category'] == 'in':
            inst = Storage.query.join(
                StorageList, StorageList.storage_id == Storage.id).filter(
                    StorageList.id == model.id).first()

        if item['category'] == 'out':
            inst = PutOutStoreModel.query.join(
                PutOutStoreMaterial,
                PutOutStoreMaterial.putOutStorage_id == PutOutStoreModel.id).filter(
                    PutOutStoreMaterial.id == model.id).first()
        if name in inst.__dict__.keys():
            return self.formater_value(name, getattr(inst, name))

        if not item['inline_column'] or not item['inline_model']:
            return ''

        # 关联的单据内的字段
        tr = getattr(inst, item['related'])
        inline_inst = item['model'].query.filter(
            item['model'].id == tr).first()
        if inline_inst and name in inline_inst.__dict__.keys():
            return self.formater_value(name, getattr(inline_inst, name))

        return ''

    def record_list(self, key):

        page = request.args.get('page', 0, type=int)
        cate = request.args.get('cate', StorageListMaterial)

        return self._view.render(
            self.list_template,
            title='航材履历',
            tabs=self.tabs,
            get_value=self.get_value,
            get_query=self.get_query,
            id=key,
            air_map=self.air_map,
            columns_labels=self.columns_labels,
            page=page,
            page_size=self.page_size,
            num_pages=7,
            cate=cate,

        )
