# coding: utf-8

from __future__ import unicode_literals

import copy

from .basic_flow import BasicFlow
from .operations import OutStoreFinish, OutStorePart
from modules.models.airmaterial import AirMaterialStorageList, AirmaterialCategory
from modules.models.base import db
from sqlalchemy import or_
from modules.models.airmaterial.storage_action import *
from modules.models.airmaterial import (
    AssembleApplication, AssembleApplicationList,
    RepairApplication, RepairMaterial,
    LoanApplicationOrder, LoanMaterial,
    Scrap, ScrapMaterial,
    BorrowingInReturnModel, BorrowingInReturnMaterial,
    PutOutStoreModel, PutOutStoreMaterial,
)
from .states import (Returned, Loaned, OutStored, Scrapped, Repairing,
                     InitialState, Edited, AllOutStored, PartOutStored)


class PutOutStoreFlow(BasicFlow):
    """出库流程"""

    states = ['created', 'edited', 'all-out-stored', 'part-out-stored']

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'all-out-stored': AllOutStored,
        'part-out-stored': PartOutStored,
    }

    def add_transition(self):
        # 新建和编辑都可以提交
        self.machine.add_transition(trigger=OutStorePart,
                                    source=['created', 'edited'],
                                    dest='part-out-stored',
                                    after='set_borrow_status')

        self.machine.add_transition(trigger=OutStoreFinish,
                                    source=['created', 'edited'],
                                    dest='all-out-stored',
                                    after='set_borrow_status')
        super(PutOutStoreFlow, self).add_transition()

    def set_borrow_status(self, **kwargs):
        self.update_allowed_change(**kwargs)

        category = {
            '借入归还出库':
                {
                    'field': 'borrowingInReturn',
                    'inline_field': 'borrow',
                    'status': Returned
                },
            '借出出库':
                {
                    'field': 'loanApplication',
                    'inline_field': '',
                    'status': Loaned
                },
            '装机出库':
                {
                    'field': 'assembleApplication',
                    'inline_field': '',
                    'status': OutStored
                },
            '报废出库':
                {
                    'field': 'scrap',
                    'inline_field': '',
                    'status': Scrapped
                },
            '送修出库':
                {
                    'field': 'repairApplication',
                    'inline_field': '',
                    'status': Repairing
                }
        }

        key = self.model.outStoreCategory

        if key not in category.keys():
            return
        inst = getattr(self.model, category[key]['field'])
        if not inst:
            return
        if self.state == 'part-out-stored':
            self.update_storageList_freezed_quantity()
        if self.state == 'all-out-stored':
            self.all_out_store_update_storagelist()
        # 装机特殊处理
        if key == '装机出库':
            inst.status = inst.auditStatus = self.status_map[self.state]
            return
        inst.status = inst.auditStatus = category[key]['status']
        if category[key]['inline_field']:
            inst = getattr(inst, category[key]['inline_field'])
            inst.status = inst.auditStatus = category[key]['status']

    def update_storageList_freezed_quantity(self):
        materials = self.model.putOutStoreMaterials
        for material in materials:
            if material.partNumber and material.serialNum:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.serialNum == material.serialNum).first()
                if not tmp:
                    raise ValueError(
                        '件号%s, 序号%s的航材已经出库' % (
                            material.partNumber, material.serialNum))
                db.session.delete(tmp)
                continue
            if not material.partNumber:
                raise ValueError('保存的航材必须有件号')
            am_category = AirmaterialCategory.query.filter(
                AirmaterialCategory.partNumber == material.partNumber).first()
            if not am_category:
                raise ValueError('航材类别中没有件号为%s的航材' % (material.partNumber))
            effective = am_category.isOrNotHaveEffectiveDate
            check = am_category.isOrNotHavePeriodCheck
            if not effective and not check:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError('没有找到件号为%s的航材' % (material.partNumber))
                tmp.quantity -= material.quantity
                tmp.freezingQuantity -= material.quantity
                if tmp.freezingQuantity < 0:
                    raise ValueError(
                        '件号%s的航材本次出库数量%s已经超出了剩余的申请数量%s' % (
                            tmp.partNumber, material.quantity,
                            tmp.freezingQuantity + material.quantity))
                if tmp.quantity <= 0:
                    db.session.delete(tmp)
                continue
            if effective and check:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.effectiveDate == material.effectiveDate,
                    AirMaterialStorageList.nextCheckDate == material.nextCheckDate,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError(
                        '库存列表里面没有件号为%s，有效期为%s，下次检查日期为%s的航材' % (
                            material.partNumber, material.effectiveDate,
                            material.nextCheckDate))
                tmp.freezingQuantity -= material.quantity
                tmp.quantity -= material.quantity
                if tmp.freezingQuantity < 0:
                    raise ValueError(
                        '件号%s，有效日期为%s，下次检查日期为%s的航材本次出库数量%s已经超出了剩余的申请数量%s' % (
                            tmp.partNumber, material.effectiveDate,
                            material.nextCheckDate, material.quantity,
                            tmp.freezingQuantity + material.quantity))
                if tmp.quantity <= 0:
                    db.session.delete(tmp)
                continue
            if effective:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.effectiveDate == material.effectiveDate,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError(
                        '库存列表里面没有件号为%s，有效期为%s的航材' % (
                            material.partNumber, material.effectiveDate))
                tmp.freezingQuantity -= material.quantity
                tmp.quantity -= material.quantity
                if tmp.freezingQuantity < 0:
                    raise ValueError(
                        '件号%s，有效日期为%s的航材本次出库数量%s已经超出了剩余的申请数量%s' % (
                            tmp.partNumber, material.effectiveDate,
                            material.quantity,
                            tmp.freezingQuantity + material.quantity))
                if tmp.quantity <= 0:
                    db.session.delete(tmp)
                continue
            if check:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.nextCheckDate == material.nextCheckDate,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError(
                        '库存列表里面没有件号为%s，下次检查日期为%s的航材' % (
                            material.partNumber, material.nextCheckDate))
                tmp.freezingQuantity -= material.quantity
                tmp.quantity -= material.quantity
                if tmp.freezingQuantity < 0:
                    raise ValueError(
                        '件号%s，下次检查日期为%s的航材本次出库数量%s已经超出了剩余的申请数量%s' % (
                            tmp.partNumber,
                            material.nextCheckDate, material.quantity,
                            tmp.freezingQuantity + material.quantity))
                if tmp.quantity <= 0:
                    db.session.delete(tmp)

    def all_out_store_update_storagelist(self, **kwargs):
        materials = self.model.putOutStoreMaterials
         # 下面更新库存的冻结数量
        all_material = self.get_all_apply_material()
        all_material_tmp = copy.deepcopy(all_material)
        unfreezed_material = self.get_all_unfreezed_material()
        # 求出未被解冻的数据
        now_freezed_partnum = {}
        now_freezed_serialnum = []
        # 获取只有件号，该件号未被解冻的数量
        for key in all_material[0].keys():
            if key in unfreezed_material[0].keys():
                now_freezed_partnum[key] = all_material[0][key]\
                    - unfreezed_material[0][key]
                if now_freezed_partnum[key] <= 0:
                    now_freezed_partnum.pop(key)
            else:
                now_freezed_partnum[key] = all_material[0][key]
        # 求取含有件号和序号未被解冻的所有元组（件号，序号）
        for val in all_material[1]:
            if val in unfreezed_material[1]:
                all_material_tmp[1].remove(val)
        now_freezed_serialnum = all_material_tmp[1]
        # 首先处理冻结数量
        # 数据库中解冻这些未被解冻的件号的数量
        unfreeze_storage_list(now_freezed_partnum)
        # 现在删除有序号的件号的冻结数
        for val in now_freezed_serialnum:
            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == val[0],
                AirMaterialStorageList.serialNum == val[1]
            ).first()
            if tmp:
                tmp.freezingQuantity = 0
        # 对数据先删除数据库中对应的数量的数据
        for material in materials:
            if material.partNumber and material.serialNum:
                if (material.partNumber, material.serialNum) not in now_freezed_serialnum:
                    raise ValueError('件号%s, 序号%s的航材已经出库' % (
                        material.partNumber, material.serialNum))
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.serialNum == material.serialNum
                ).first()
                db.session.delete(tmp)
                continue
            am_category = AirmaterialCategory.query.filter(
                AirmaterialCategory.partNumber == material.partNumber).first()
            if not am_category:
                raise ValueError('航材类别中没有件号为%s的航材' % (material.partNumber))
            effective = am_category.isOrNotHaveEffectiveDate
            check = am_category.isOrNotHavePeriodCheck
            if not effective and not check:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError('没有找到件号为%s的航材' % (material.partNumber))
                tmp.quantity -= material.quantity
                if tmp.quantity <= 0:
                    db.session.delete(tmp)
                continue
            if effective and check:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.effectiveDate == material.effectiveDate,
                    AirMaterialStorageList.nextCheckDate == material.nextCheckDate,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError(
                        '库存列表里面没有件号为%s，有效期为%s，下次检查日期为%s的航材' % (
                            material.partNumber, material.effectiveDate,
                            material.nextCheckDate))
                tmp.quantity -= material.quantity
                if tmp.quantity <= 0:
                    db.session.delete(tmp)
                continue
            if effective:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.effectiveDate == material.effectiveDate,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError(
                        '库存列表里面没有件号为%s，有效期为%s的航材' % (
                            material.partNumber, material.effectiveDate))
                tmp.quantity -= material.quantity
                if tmp.quantity <= 0:
                    db.session.delete(tmp)
                continue
            if check:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.nextCheckDate == material.nextCheckDate,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError(
                        '库存列表里面没有件号为%s，下次检查日期为%s的航材' % (
                            material.partNumber, material.nextCheckDate))
                tmp.quantity -= material.quantity
                if tmp.quantity <= 0:
                    db.session.delete(tmp)

    def get_all_apply_material(self):
        """获取所有被冻结的航材（就是在这个入库单据的申请单中）"""
        tmp = get_out_store_category(self.model.outStoreCategory)
        applModel, applMaterial, applMaterialfk = tmp[0], tmp[1], tmp[2]
        applMaterialfk = getattr(applMaterial, applMaterialfk)
        # 本单据的外键
        ownOutStorefk = getattr(self.model, tmp[3])

        materials = applMaterial.query.filter(
            applMaterial.partNumber != None,
            or_(applMaterial.serialNum == None,
                applMaterial.serialNum == ''),
            applMaterialfk == applModel.id,
            applModel.id == ownOutStorefk)
        material_number = {}
        for material in materials:
            material_number = get_pn_old_new_n_e_data(
                material.partNumber, material.quantity,
                material.effectiveDate, material.nextCheckDate,
                material_number)
            # material_number[material.partNumber] = material.quantity
        have_serial_materials = applMaterial.query.filter(
            applMaterial.serialNum != None,
            applMaterial.serialNum != '',
            applMaterialfk == applModel.id,
            applModel.id == ownOutStorefk)
        serial_material = []
        for material in have_serial_materials:
            serial_material.append((material.partNumber, material.serialNum))
        return (material_number, serial_material)

    def get_all_unfreezed_material(self):
        """获取所有已经被解冻的航材（
        就是已经出库的航材，已经出库的航材就会被解冻）
        根据本出库单-->申请单--->申请单下的所有已经部分出库的单据
        中的所有航材，并根据件号和序号进行整合（返回已经解冻的件号及有
        件号和号的航材元组）
        """
        tmp = get_out_store_category(self.model.outStoreCategory)
        applModel, applMaterial, applMaterialfk = tmp[0], tmp[1], tmp[2]
        applMaterialfk = getattr(applMaterial, applMaterialfk)
        outstoretoApplfk = getattr(PutOutStoreModel, tmp[3])
        # 本单据的外键
        ownOutStorefk = getattr(self.model, tmp[3])
        materials = PutOutStoreMaterial.query.filter(
            PutOutStoreMaterial.partNumber != None,
        ).join(
            PutOutStoreModel,
            PutOutStoreMaterial.putOutStorage_id == PutOutStoreModel.id,
        ).filter(
            PutOutStoreModel.statusName == PartOutStored,
        ).join(applModel, applModel.id == outstoretoApplfk).filter(
            applModel.id == ownOutStorefk)
        unfreezed_partnum = {}
        unfreezed_serialnum = []
        for material in materials:
            if not material.serialNum:
                unfreezed_partnum = get_pn_old_new_n_e_data(
                    material.partNumber, material.quantity,
                    material.effectiveDate, material.nextCheckDate,
                    unfreezed_partnum)
            else:
                unfreezed_serialnum.append(
                    (material.partNumber, material.serialNum))
        return (unfreezed_partnum, unfreezed_serialnum)


def get_out_store_category(category):

    out_store_category = {
        LoanOutSTORE: 'loanApplication',
        BorrowReturnOutSTORE: 'borrowingInReturn',
        AssembleOutSTORE: 'assembleApplication',
        RepairOutSTORE: 'repairApplication',
        ScrapOutSTORE: 'scrap',
    }
    out_store_appl_model = {
        LoanOutSTORE: LoanApplicationOrder,
        BorrowReturnOutSTORE: BorrowingInReturnModel,
        AssembleOutSTORE: AssembleApplication,
        RepairOutSTORE: RepairApplication,
        ScrapOutSTORE: Scrap,
    }
    application_material = {
        'loanApplication': LoanMaterial,
        'borrowingInReturn': BorrowingInReturnMaterial,
        'assembleApplication': AssembleApplicationList,
        'repairApplication': RepairMaterial,
        'scrap': ScrapMaterial,
    }
    application_material_fk = {
        'loanApplication': 'loanApplication_id',
        'borrowingInReturn': 'borrowInReturn_id',
        'assembleApplication': 'assembleapplication_id',
        'repairApplication': 'application_id',
        'scrap': 'application_id',
    }
    out_storage_application_fk = {
        'loanApplication': 'loanApplication_id',
        'borrowingInReturn': 'borrowingInReturn_id',
        'assembleApplication': 'assemble_application_id',
        'repairApplication': 'repair_application_id',
        'scrap': 'scrap_id',
    }
    tmp = out_store_category[category]
    applModel = out_store_appl_model[category]
    applMaterial = application_material[tmp]
    applMaterialfk = application_material_fk[tmp]
    outstoretoApplfk = out_storage_application_fk[tmp]
    return (applModel, applMaterial, applMaterialfk, outstoretoApplfk)


def get_pn_old_new_n_e_data(pn, quantity, effc, next_date, pn_n_e):
        """根据最新或以前的数据，根据件号，有效期，下次检查日期进行分类"""
        am_category = AirmaterialCategory.query.filter(
            AirmaterialCategory.partNumber == pn).first()
        if not am_category:
            raise ValueError('航材类别中没有件号为%s的航材' % (pn))
        effective = am_category.isOrNotHaveEffectiveDate
        check = am_category.isOrNotHavePeriodCheck
        if not effective and not check:
            if pn not in pn_n_e.keys():
                pn_n_e[pn] = quantity
            else:
                pn_n_e[pn] += quantity
            return pn_n_e
        if effective and check:
            if (pn, effc, next_date) not in pn_n_e.keys():
                pn_n_e[(pn, effc, next_date)] = quantity
            else:
                pn_n_e[(pn, effc, next_date)] += quantity
            return pn_n_e
        if effective:
            if (pn, effc) not in pn_n_e.keys():
                pn_n_e[(pn, effc)] = quantity
            else:
                pn_n_e[(pn, effc)] += quantity
            return pn_n_e
        if check:
            if (pn, next_date) not in pn_n_e.keys():
                pn_n_e[(pn, next_date)] = quantity
            else:
                pn_n_e[(pn, next_date)] += quantity
        return pn_n_e


def unfreeze_storage_list(freezed_pn):
    for val in freezed_pn.keys():
        if isinstance(val, (str, unicode)):
            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == val,
                or_(AirMaterialStorageList.serialNum == None,
                    AirMaterialStorageList.serialNum == '')).first()
            if not tmp:
                raise ValueError('件号%s的航材不在库存列表中' % (val))
            if tmp.freezingQuantity:
                tmp.freezingQuantity -= freezed_pn[val]
            continue
        am_category = AirmaterialCategory.query.filter(
            AirmaterialCategory.partNumber == val[0]).first()
        if not am_category:
            raise ValueError('航材类别中没有件号为%s的航材' % (val[0]))
        effective = am_category.isOrNotHaveEffectiveDate
        check = am_category.isOrNotHavePeriodCheck
        if effective and check:
            if len(val) < 3:
                raise ValueError(
                    '件号为%s的航材必须有有效日期和下次检查时间' % (val[0]))
            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == val[0],
                AirMaterialStorageList.effectiveDate == val[1],
                AirMaterialStorageList.nextCheckDate == val[2],
                or_(AirMaterialStorageList.serialNum == None,
                    AirMaterialStorageList.serialNum == '')).first()
            if not tmp:
                raise ValueError(
                    '库存中没有件号为%s，有效期为%s，下次检查日期为%s的航材' % (
                        val[0], val[1], val[2]))
            if tmp.freezingQuantity:
                tmp.freezingQuantity -= freezed_pn[val]
            continue
        if effective:
            if len(val) < 2:
                raise ValueError(
                    '件号为%s的航材必须有有效日期' % (val[0]))
            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == val[0],
                AirMaterialStorageList.effectiveDate == val[1],
                or_(AirMaterialStorageList.serialNum == None,
                    AirMaterialStorageList.serialNum == '')).first()
            if not tmp:
                raise ValueError(
                    '库存中没有件号为%s，有效期为%s的航材' % (val[0], val[1]))
            if tmp.freezingQuantity:
                tmp.freezingQuantity -= freezed_pn[val]
            continue
        if check:
            if len(val) < 2:
                raise ValueError(
                    '件号为%s的航材必须有下次检查时间' % (val[0]))
            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == val[0],
                AirMaterialStorageList.nextCheckDate == val[1],
                or_(AirMaterialStorageList.serialNum == None,
                    AirMaterialStorageList.serialNum == '')).first()
            if not tmp:
                raise ValueError(
                    '库存中没有件号为%s，下次检查日期为%s的航材' % (val[0], val[1]))
            if tmp.freezingQuantity:
                tmp.freezingQuantity -= freezed_pn[val]
