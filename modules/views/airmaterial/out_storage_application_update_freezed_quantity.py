# coding: utf-8

from __future__ import unicode_literals

from flask import request
from modules.models.airmaterial import AirMaterialStorageList, AirmaterialCategory
from .with_inline_table import WithInlineTableView
import logging
from sqlalchemy import or_

# Set up logger
log = logging.getLogger("flask-admin.sqla")


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


class UpdateStorageListFreezedQuantity(WithInlineTableView):
    """更新库存冻结数量"""
    # freezed_pn 是原来的冻结件号和数量的字典
    # new_freezed_pn 是最新的冻结件号和字典
    # freezed_pn_serialnumber 是原来有件号序号的列表
    # new_freezed_pn_serialnumber 是最新的有件号序号的列表
    def update_storage_list_freezed_quantity(
            self, freezed_pn, new_freezed_pn,
            freezed_pn_serialnumber, new_freezed_pn_serialnumber):
        # 首先判断一遍新的冻结件号是否在旧的里面，如果在更新数量差存入新的件号冻结字典里
        for val in new_freezed_pn.keys():
            if val in freezed_pn.keys():
                new_freezed_pn[val] -= freezed_pn[val]
        # 再次判断旧的件号是否在新的里面是否存在，如果不存在则表示编辑的时候删除，则
        # 把数量取负数存入新的里面
        for val in freezed_pn.keys():
            if val not in new_freezed_pn.keys():
                new_freezed_pn[val] = 0 - freezed_pn[val]
        # 对于有序号的件号，只需要获取增加的序号和删除的序号
        # 下面先得到删除的序号，再得到添加的序号
        add_freezed_pn_serialnumber = []
        del_freezed_pn_serialnumber = []
        for val in freezed_pn_serialnumber:
            if val not in new_freezed_pn_serialnumber:
                del_freezed_pn_serialnumber.append(val)
        for val in new_freezed_pn_serialnumber:
            if val not in freezed_pn_serialnumber:
                add_freezed_pn_serialnumber.append(val)
        # 更新数据库
        for val in new_freezed_pn.keys():
            if isinstance(val, (str, unicode)):
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == val,
                    or_(AirMaterialStorageList.serialNum == None,
                        AirMaterialStorageList.serialNum == '')).first()
                if not tmp:
                    raise ValueError('件号%s的航材不在库存列表中' % (val))
                if tmp.freezingQuantity:
                    tmp.freezingQuantity += new_freezed_pn[val]
                else:
                    tmp.freezingQuantity = new_freezed_pn[val]
                if tmp.freezingQuantity > tmp.quantity:
                    return False
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
                        '库存中没有件号为%s，有效期为%s，下次检查日期为%s的航材' % (val[0],
                        val[1], val[2]))
                if tmp.freezingQuantity:
                    tmp.freezingQuantity += new_freezed_pn[val]
                else:
                    tmp.freezingQuantity = new_freezed_pn[val]
                if tmp.freezingQuantity > tmp.quantity:
                    return False
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
                    tmp.freezingQuantity += new_freezed_pn[val]
                else:
                    tmp.freezingQuantity = new_freezed_pn[val]
                if tmp.freezingQuantity > tmp.quantity:
                    return False
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
                    tmp.freezingQuantity += new_freezed_pn[val]
                else:
                    tmp.freezingQuantity = new_freezed_pn[val]
                if tmp.freezingQuantity > tmp.quantity:
                    return False
                continue
        for val in add_freezed_pn_serialnumber:
            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == val[0],
                AirMaterialStorageList.serialNum == val[1]).first()
            if not tmp:
                raise ValueError('件号%s，序号%s的航材不在库存列表中' % (val[0], val[1]))
            tmp.freezingQuantity += 1
            if tmp.freezingQuantity > 1:
                return False
        for val in del_freezed_pn_serialnumber:
            tmp = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.partNumber == val[0],
                AirMaterialStorageList.serialNum == val[1]).first()
            if not tmp:
                raise ValueError('件号%s，序号%s的航材不在库存列表中' % (val[0], val[1]))
            tmp.freezingQuantity -= 1
            if tmp.freezingQuantity != 0:
                return False
        return True

    def on_model_change(self, form, model, is_created):
        freezed_pn_n_e = {}
        freezed_pn_serialnumber = []
        new_freezed_pn_n_e = {}
        new_freezed_pn_serialnumber = []
        for old_material in getattr(model, self.relationField):
            # 这里要执行删除数据，再删除之前获取编辑之前原数据中这个件号下的数量
            # 当保存时去更新库存列表里面的冻结数量
            # 如果有序号，则数量一定是1，保存起来防止后面编辑表时被删除掉
            if not old_material.serialNum:
                freezed_pn_n_e = get_pn_old_new_n_e_data(
                    old_material.partNumber, old_material.quantity,
                    old_material.effectiveDate, old_material.nextCheckDate,
                    freezed_pn_n_e)
            else:
                freezed_pn_serialnumber.append(
                    (old_material.partNumber, old_material.serialNum))
        table_data = request.form.get('table_datas').replace('null', 'None')
        table_data = eval(table_data)
        table_data = [col if col != '' else None for col in [row for row in table_data]]
        for row in table_data:
            new_pn_quantity = 0
            new_serialNum = None
            new_pn = None
            new_effec = None
            new_nextd = None
            for i, r in enumerate(row):
                if self.table_columns.keys()[i] == 'partNumber':
                    new_pn = r
                if self.table_columns.keys()[i] == 'quantity':
                    new_pn_quantity = r
                if self.table_columns.keys()[i] == 'serialNum':
                    new_serialNum = r
                if self.table_columns.keys()[i] == 'effectiveDate':
                    new_effec = r
                if self.table_columns.keys()[i] == 'nextCheckDate':
                    new_nextd = r
            # 这里建立一个新的字典去对比原来应该冻结的个数，做差去更新库存列表中的冻结数量
            if not new_serialNum:
                if new_pn and new_pn_quantity:
                    new_freezed_pn_n_e = get_pn_old_new_n_e_data(
                        new_pn, new_pn_quantity,
                        new_effec, new_nextd, new_freezed_pn_n_e)
            else:
                if new_pn:
                    new_freezed_pn_serialnumber.append(
                        (new_pn, new_serialNum))
        ret = self.update_storage_list_freezed_quantity(
            freezed_pn_n_e, new_freezed_pn_n_e,
            freezed_pn_serialnumber, new_freezed_pn_serialnumber)
        if not ret:
            raise ValueError('库存数量已经发生改变，请退出或重新调整数量')
        super(UpdateStorageListFreezedQuantity, self).on_model_change(
            form, model, is_created)

    def on_model_delete(self, model):
        freezed_pn_n_e = {}
        freezed_pn_serialnumber = []
        for old_material in getattr(model, self.relationField):
            # 这里要执行删除数据，再删除之前获取编辑之前原数据中这个件号下的数量
            # 如果有序号，则数量一定是1，在库存列表中直接删除
            if not old_material.serialNum:
                freezed_pn_n_e = get_pn_old_new_n_e_data(
                    old_material.partNumber, old_material.quantity,
                    old_material.effectiveDate, old_material.nextCheckDate,
                    freezed_pn_n_e)
            else:
                freezed_pn_serialnumber.append(
                    (old_material.partNumber, old_material.serialNum))
        self.update_storage_list_freezed_quantity(
            freezed_pn_n_e, {},
            freezed_pn_serialnumber, [])
        super(UpdateStorageListFreezedQuantity, self).on_model_delete(model)
