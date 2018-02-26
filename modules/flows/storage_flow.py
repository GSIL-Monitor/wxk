# coding: utf-8

from __future__ import unicode_literals

from .basic_flow import BasicFlow
from .operations import Finish, InStoreFinish, InStorePart
from .states import (InitialState, Sented, Borrowed, Edited, InStored,
                     Disassembled, Returned, StoresReturned, Repaired,
                     AllInStored, PartInStored)
from modules.models.airmaterial.lend_application import LendApplication
from modules.models.airmaterial.storage_list import AirMaterialStorageList
from modules.models.base import db
from modules.models.airmaterial.storage_action import *
from bson import DBRef
from modules.models.airmaterial import AirmaterialCategory
from util.exception import BackendServiceError
from sqlalchemy import and_, or_
from flask import current_app
from ..proxy import proxy


type_key = {
    '时控件': 'time_control_unit_y5b',
    '时寿件': 'life_control_unit_y5b',
}


def get_boundedid_by_plane_pn_serialnum(plane_num, pn, serial_num, category):
    """通过飞机号、件号、序号、类型获取boundedid"""
    coll = current_app.mongodb
    mxType = {
        '时控件': 'timecontrol',
        '时寿件': 'lifecontrol',
    }
    val = coll[type_key[category]].find_one({'id': pn})
    if not val:
        return None
    refId = DBRef(type_key[category], val['_id'])
    ret = coll.aircraft_information.aggregate(
        [
            {'$match': {'id': plane_num}},
            {'$project': {'boundedItems': 1, '_id': 0}},
            {'$unwind': '$boundedItems'},
            {'$match': {'boundedItems.refId': refId,
                        'boundedItems.serialNumber': serial_num}},
        ]
    )
    ret = list(ret)
    if len(ret):
        return (ret[0]['boundedItems']['boundedId'],
                val['id'], mxType[category])
    return None


def get_plane_infos_by_pn(pn, plane_num, category):
    """通过飞机号、件号和类型获取在绑定飞机的绑定状态"""
    if category not in ['时控件', '时寿件']:
        return None
    coll = current_app.mongodb
    val = coll[type_key[category]].find_one({'id': pn})
    if not val:
        return None
    tmp_ref = DBRef(
        type_key[category], val['_id'])
    des = coll.aircraft_information.aggregate(
        [
            {'$match': {'id': plane_num}},
            {'$project': {'boundedItems': 1, '_id': 0}},
            {'$unwind': '$boundedItems'},
            {'$match': {'boundedItems.refId': tmp_ref}},
        ]
    )
    return len(list(des))


def add_boundedstatus_by_mxp_mxtype_plane_num(mxId, mxType, plane_num):
    resp = proxy.create(
        {
            'mxId': mxId,
            'mxType': mxType,
            'planeId': plane_num,
        },
        '/v1/mxp-binding/duplicate')
    if resp.status_code == 200:
        return True
    return False


class StorageFlow(BasicFlow):
    """入库流程"""

    states = ['created', 'edited', 'all-in-stored', 'part-in-stored']

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'all-in-stored': AllInStored,
        'part-in-stored': PartInStored,
    }

    def add_transition(self):
        # 新建和编辑都可以提交
        self.machine.add_transition(trigger=InStoreFinish,
                                    source=['created', 'edited'],
                                    dest='all-in-stored',
                                    after='set_borrow_status')
        self.machine.add_transition(trigger=InStorePart,
                                    source=['created', 'edited'],
                                    dest='part-in-stored',
                                    after='set_borrow_status')
        super(StorageFlow, self).add_transition()

    def set_borrow_status(self, **kwargs):
        self.update_allowed_change(**kwargs)

        category = {
            LendSTORE:
                {
                    'field': 'borrow',
                    'inline_field': '',
                    'status': Borrowed
                },
            LoanReturnSTORE:
                {
                    'field': 'loanReturn',
                    'inline_field': 'loanApplication',
                    'status': Returned
                },
            DisassembleSTORE:
                {
                    'field': 'disassemble',
                    'inline_field': '',
                    'status': Disassembled
                },
            ReturnMaterialSTORE:
                {
                    'field': 'returnMaterial',
                    'inline_field': '',
                    'status': StoresReturned
                },
            RepairReturnSTORE:
                {
                    'field': 'repairReturnOrder',
                    'inline_field': 'repairApplication',
                    'status': Repaired,
                },
            PurchaseSTORE:
                {
                    'field': 'purchaseApplication',
                    'status': InStored,
                    'inline_field': '',
                }
        }

        key = self.model.instoreCategory

        if key not in category.keys():
            return
        inst = getattr(self.model, category[key]['field'])
        if not inst:
            return
        inst.status = inst.auditStatus = category[key]['status']
        if category[key]['inline_field']:
            inst = getattr(inst, category[key]['inline_field'])
            inst.status = inst.auditStatus = category[key]['status']
        self.update_storage_list()

    def update_storage_list(self):
        """把跟入库的数据更新至库存列表中"""
        materials = self.model.storageList
        for material in materials:
            # 首先判断有件号和序号的航材，因为件号和序号确定唯一航材
            if material.partNumber and material.serialNum:
                if material.quantity != 1:
                    raise ValueError('件号%s和序号%s的航材数量必须是1' % (
                        material.partNumber, material.serialNum))
                # 判断库存中有没有这样的航材， 如果有则报错
                des_tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.serialNum == material.serialNum
                ).first()
                if des_tmp:
                    raise ValueError('件号%s和序号%s的航材在库存中已经存在' % (
                        des_tmp.partNumber, des_tmp.serialNum))
                # 对于有序号的航材，直接插入数据库
                self.assert_material_to_storage_list(material)
                self.delete_serial_pn_from_boundeditems(material)
                continue

            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == material.partNumber).first()
            # 对于航材库中没有该件号的航材的时候，直接把航材写入(无论是否有序号)
            if not tmp:
                self.assert_material_to_storage_list(material)
                self.delete_serial_pn_from_boundeditems(material)
                continue
            no_serial_material = AirMaterialStorageList.query.filter(
                and_(AirMaterialStorageList.partNumber == material.partNumber,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == ''))).first()
            # 下面要检查该航材有没有有效期和定期检查
            am_category = AirmaterialCategory.query.filter(
                AirmaterialCategory.partNumber == material.partNumber).first()
            if not am_category:
                raise ValueError('航材类别中不存在件号为%s的航材' %(material.partNumber))
            # 对于没有有效期和定期检查属性的如果件号一样,直接相加
            if not am_category.isOrNotHaveEffectiveDate and not am_category.isOrNotHavePeriodCheck:
                if no_serial_material:
                    no_serial_material.quantity += material.quantity
                else:
                    self.assert_material_to_storage_list(material)
                self.delete_serial_pn_from_boundeditems(material)
                continue

            # 对于有有效期和定期检查属性的航材，要对他们进行分开出来
            self.update_effective_check_storage(material, am_category)
            self.delete_serial_pn_from_boundeditems(material)

    def assert_material_to_storage_list(self, material):
        res_dict = {}
        for key in material.__table__.columns.keys():
            if key in AirMaterialStorageList.__table__.columns.keys() and key != 'id':
                res_dict.update({key: material.__dict__[key]})
        des_tmp = AirmaterialCategory.query.filter(
            AirmaterialCategory.partNumber == material.partNumber).first()
        if des_tmp and des_tmp.minStock:
            res_dict.update({'minStock': des_tmp.minStock})
        sl = AirMaterialStorageList(**res_dict)
        db.session.add(sl)

    def update_effective_check_storage(self, material, am_category):
        """对于具有有效期和定期检查属性航材插入数据库时，要按其的有效期和下次检查时间进行区分"""
        effective = am_category.isOrNotHaveEffectiveDate
        check = am_category.isOrNotHavePeriodCheck
        # 对有效期和下次检查时间都需要有的航材的数据插入
        if effective and check:
            if not material.nextCheckDate or not material.effectiveDate:
                raise ValueError(
                    '件号为%s航材必须输入有效日期和下次检查时间' % (material.partNumber))
            n_e_material = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == material.partNumber,
                AirMaterialStorageList.nextCheckDate == material.nextCheckDate,
                AirMaterialStorageList.effectiveDate == material.effectiveDate,
            ).first()
            if not n_e_material:
                self.assert_material_to_storage_list(material)
            else:
                n_e_material.quantity += material.quantity
            return
        # 对自有有效期的航材的插入
        if effective:
            if not material.effectiveDate:
                raise ValueError(
                    '件号为%s航材必须输入有效日期' % (material.partNumber))
            e_material = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == material.partNumber,
                AirMaterialStorageList.effectiveDate == material.effectiveDate,
            ).first()
            if not e_material:
                self.assert_material_to_storage_list(material)
            else:
                e_material.quantity += material.quantity
            return
        if check:
            if not material.nextCheckDate:
                raise ValueError(
                    '件号为%s航材必须输入下次检查日期' % (material.partNumber))
            n_material = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == material.partNumber,
                AirMaterialStorageList.nextCheckDate == material.nextCheckDate,
            ).first()
            if not n_material:
                self.assert_material_to_storage_list(material)
            else:
                n_material.quantity += material.quantity
            return

    def delete_serial_pn_from_boundeditems(self, material):
        """从入库的表单中获取某飞机的含有件号和序号的时控件或时寿件，
        从数据库中获取它的boundedId,然后从绑定状态中删除该件和序号，
        更新到期列表。
        """
        if self.model.instoreCategory == DisassembleSTORE and material.category in ['时控件', '时寿件']:
            if material.partNumber and material.serialNum and material.planeNum:
                bounded_status = get_boundedid_by_plane_pn_serialnum(
                    material.planeNum, material.partNumber,
                    material.serialNum, material.category)
                if not bounded_status:
                    raise ValueError('%s飞机的件号:%s、序号:%s,没有找到相应的绑定状态' % (
                        material.planeNum, material.partNumber,
                        material.serialNum))
                # 判断该飞机号、件号、类型下绑定到飞机上的序号有几个，如果为1，增加一个绑定状态再删除
                tmp = get_plane_infos_by_pn(
                    material.partNumber, material.planeNum, material.category)
                if not tmp:
                    raise ValueError('查询绑定状态失败，请联系管理员')
                if tmp <= 1:
                    # 客户端增加时寿件或时控件绑定状态的处理逻辑部分
                    if not add_boundedstatus_by_mxp_mxtype_plane_num(
                        bounded_status[1], bounded_status[2], material.planeNum):
                        raise ValueError('添加绑定状态失败，请联系管理员')
                resp = proxy.delete(
                    None, '/v1/mxp-binding/?boundedid=' + bounded_status[0])
                if resp.status_code >= 400:
                    raise BackendServiceError('调用api出错')
