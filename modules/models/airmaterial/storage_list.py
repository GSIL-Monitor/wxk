# coding: utf-8

from __future__ import unicode_literals
import logging
import sys
from datetime import datetime

from sqlalchemy import schema, types
from ..base import Model, db
from ..audit import AuditModel
from .airmaterial_category import AirmaterialCategory
from ..util_csv import read_file

reload(sys)
sys.setdefaultencoding('gbk')


class AirMaterialStorageList(Model, AuditModel):
    "库存列表的内容"

    __tablename__ = "air_material_storage_list"

    id = schema.Column(types.Integer, primary_key=True)
    # category 航材类型
    category = schema.Column(types.String(255))
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # freezingQuantity 冻结数量
    freezingQuantity = schema.Column(types.Integer, default=0)
    # unit 航材单位
    unit = schema.Column(types.String(255))
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落架次
    flightTimes = schema.Column(types.Integer)
    # applicableModel 适用机型
    applicableModel = schema.Column(types.String(255))
    # storehouse 仓库
    storehouse = schema.Column(types.String(255))
    # shelf 架位
    shelf = schema.Column(types.String(255))
    # miniStock 最低库存
    minStock = schema.Column(types.String(255))
    # effectiveDate 有效日期
    effectiveDate = schema.Column(types.String(255))
    # certificateNum 证书编号
    certificateNum = schema.Column(types.String(255))
    # airworthinessTagNum 适航标签号
    airworthinessTagNum = schema.Column(types.String(255))
    # lastCheckDate 上次检查日期
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查日期
    nextCheckDate = schema.Column(types.String(255))
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # supplier 供应商
    supplier = schema.Column(types.String(255))
    # statusName 状态值nextCheckDate
    statusName = schema.Column(types.String(100))
    # checkRecord 供应商
    checkRecord = schema.Column(types.String(1000))


def read_datas(row):

    data = {
        'category': row['类型'.encode('utf-8')],
        'partNumber': row['件号'.encode('utf-8')],
        'serialNum': row['序号'.encode('utf-8')],
        'name': row['名称'.encode('utf-8')],
        'unit': row['单位'.encode('utf-8')],
        # 'flyTime': float(row['飞行小时'.encode('utf-8')]),
        # 'engineTime': float(row['发动机小时'.encode('utf-8')]),
        # 'flightTimes': int(row['起落架次'.encode('utf-8')]),
        'applicableModel': "运5B(D)",
        'storehouse': row['仓库'.encode('utf-8')],
        'minStock': row['最低库存'.encode('utf-8')],
        'shelf': row['架位'.encode('utf-8')],
        'effectiveDate': row['库存有效期'.encode('utf-8')],
        'certificateNum': row['证书编号'.encode('utf-8')],
        'airworthinessTagNum': row['适航标签号'.encode('utf-8')],
        'lastCheckDate': row['上次检查日期'.encode('utf-8')],
        'nextCheckDate': row['下次检查日期'.encode('utf-8')],
        'manufacturer': row['生产厂商'.encode('utf-8')],
        'supplier': row['供应商'.encode('utf-8')],

    }

    if row['数量'.encode('utf-8')]:
        data['quantity'] = int(row['数量'.encode('utf-8')])

    if row['冻结数量'.encode('utf-8')]:
        data['freezingQuantity'] = int(row['冻结数量'.encode('utf-8')])

    if row['起落架次'.encode('utf-8')]:
        data['flightTimes'] = int(row['起落架次'.encode('utf-8')])

    if row['飞行小时'.encode('utf-8')]:
        data['flyTime'] = row['飞行小时'.encode('utf-8')]

    if row['发动机小时'.encode('utf-8')]:
        data['engineTime'] = row['发动机小时'.encode('utf-8')]

    if not data['name'] or not data['partNumber']:
        logging.warn("名称（%s）或件号（%s）不存在。" % (
            data['name'].decode('utf-8'), data['partNumber']))
        return None

    if data['minStock'] and data['minStock'] <= 0:
        logging.msg("航材（%s）的最低库存应大于0" % data['name'].decode("utf-8"))
        return None

    if data['partNumber'] and data['serialNum'] and data['quantity'] != 1:
        logging.warn("件号和序号都存在时，数量必须为1。第%s条数据" % row['序号1'.encode('utf-8')])
        return None

    if data['freezingQuantity'] < 0 or \
            data['freezingQuantity'] > data['quantity']:
        logging.warn("冻结数量应至少为0，且不大于数量。第%s条数据" % row['序号1'.encode('utf-8')])
        return None

    if data['lastCheckDate']:
        try:
            date = datetime.strptime(data['lastCheckDate'], "%Y-%m-%d")
        except Exception as e:
            logging.warn("lastCheckDate is wrong. number:%s" % row['序号1'.encode('utf-8')])
            return

    if data['nextCheckDate']:
        try:
            date = datetime.strptime(data['nextCheckDate'], "%Y-%m-%d")
        except Exception as e:
            logging.warn("nextCheckDate is wrong. number:%s" % row['序号1'.encode('utf-8')])
            return

    am = AirmaterialCategory.query.filter(
        AirmaterialCategory.partNumber == data['partNumber'],
        AirmaterialCategory.category == data['category'],
        AirmaterialCategory.name == data['name']).first()
    if not am:
        logging.warn("该库存对应的航材不存在或库存的名称或类型不对应. 件号：%s名称：%s" % (
            data['partNumber'], data['name'].decode("utf-8")))
        return None
    return data


def reset_datas(cfg_file, col_name, read_datas=read_datas,
                skip_first=False, clean=True):

    datas = read_file(cfg_file, read_datas, skip_first)

    count = 0
    length = len(datas)
    if len(datas):
        # 清空数据
        if clean == "true":
            db.session.query(col_name).delete()
            db.session.commit()
        for data in datas:
            try:
                inst = col_name(**data)
                asl = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == inst.partNumber,
                    AirMaterialStorageList.serialNum == inst.serialNum).first()
                if asl:
                    logging.warn("该库存已经存在。件号：%s，序号：%s" % (
                        data['partNumber'], data['serialNum']))
                    continue
                db.session.add(inst)
                count += 1
            except Exception as e:
                logging.warn(e)
        if length != count:
            logging.warn("not all the datas can import")
            return
        try:
            db.session.commit()
        except Exception as e:
            logging.warn(e)
            db.session.rollback()
    return count
