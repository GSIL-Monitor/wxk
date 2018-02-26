# encoding: utf-8
# 处理原维修客管理系统的飞行器信息

from __future__ import unicode_literals
import easy_date
import re
import hashlib
import json
import requests
import logging
from bson import ObjectId, Int64
import sys

from flask import current_app
from wtforms.validators import ValidationError, DataRequired
from wtforms import form, fields
from bson import DBRef

from modules.proxy import proxy
from modules.helper import get_aircraft_info
from util.fields import DateInt
from util.fields import RefreshPlaneTypeSelectField, HourMinuteField
from modules.forms.util_csv import read_file


reload(sys)
sys.setdefaultencoding('gbk')


class UtilizationForm(form.Form):
    """飞行器利用率的相关信息。"""
    hours = fields.FloatField('小时/月')
    times = fields.IntegerField('起落次数/月')


class AircraftInformationForm(form.Form):

    id = fields.StringField('飞行器注册号', [DataRequired('请输入飞行器注册号')])
    # TODO: 这个应该是选择列表
    planeType = RefreshPlaneTypeSelectField('机型')
    # sn = fields.StringField('飞行器串号', [DataRequired('请输入飞行器串号')])
    importedDate = DateInt('引进日期', [DataRequired('请输入引进日期')])
    permanentAirport = fields.StringField('常驻机场', [DataRequired('请输入常驻机场')])
    acn = fields.StringField('适航证编号', [DataRequired('请输入适航证编号')])
    acnDeadline = DateInt('适航证编号到期时间')
    nrn = fields.StringField('国籍登记证编号', [DataRequired('请输入国籍登记证编号')])
    slnDeadline = DateInt('国籍登记编号到期时间')
    sln = fields.StringField('电台执照编号', [DataRequired('请输入电台执照编号')])
    nrnDeadline = DateInt('电台执照编号到期时间', [DataRequired('请输入电台执照编号到期时间')])
    manufacturer = fields.StringField('制造商', [DataRequired('请输入制造商')])
    manufactureDate = DateInt('制造日期', [DataRequired('请输入制造日期')])
    landTimes = fields.IntegerField('初始起落次数', [DataRequired('请输入初始起落次数(整数)')])
    engineNumber = fields.StringField('发动机序号', [DataRequired('请输入发动机序号')])
    flightTime = HourMinuteField(
        '初始飞行时间', [DataRequired('请输入初始飞行时间(格式00：00)')])
    engineTime = HourMinuteField(
        '初始发动机时间', [DataRequired('请输入初始发动机时间(格式00：00)')])
    propellerTime = HourMinuteField(
        '初始螺旋桨时间', [DataRequired('请输入初始螺旋桨时间(格式00：00)')])
    machinist = fields.StringField('机械师')
    # displayName = fields.StringField('型号')
    # 暂时不支持设置飞机图片
    imageUrl = fields.HiddenField()
    remark = fields.StringField('备注')
    etag = fields.HiddenField('etag')

    def validate_manufactureDate(form, field):
        if field.data > form['importedDate'].data:
            raise ValidationError('制造日期应早于引进日期')

    def validate_id(form, field):
        if field.object_data:
            if field.object_data != field.data:
                raise ValidationError('不能更改飞行器注册号')
            return

        if get_aircraft_info(field.data) is not None:
            raise ValidationError('这个飞行器注册号已经注册过')


def date_formate(data):
    return int(easy_date.convert_from_string(
        data, '%Y-%m-%d', None, float))


def hour_formate(data):

    message = "格式00:00"
    rep = '^(\d+):[0-5]\d$'
    if not re.match(rep, data):
        raise ValidationError(message)

    minute = float('%.2f' % float(int(data.split(":")[1]) / 60.0))
    hour = int(data.split(":")[0])

    return hour + minute


def read_datas(row):

    data = {
        'id': row['飞行器注册号'.encode('utf-8')],
        'planeType': row['机型'.encode('utf-8')],
        'permanentAirport': row['常驻机场'.encode('utf-8')],
        'acn': row['适航证编号'.encode('utf-8')],
        'nrn': row['国籍登记证编号'.encode('utf-8')],
        'sln': row['电台执照编号'.encode('utf-8')],
        'manufacturer': row['制造商'.encode('utf-8')],
        'landTimes': int(row['初始起落次数'.encode('utf-8')]),
        'engineNumber': row['发动机序号'.encode('utf-8')],
        'displayName': current_app.config['PLANE_TYPE']

    }
    data['totalTimes'] = data['landTimes']

    if row['引进日期'.encode('utf-8')]:
        data['importedDate'] = date_formate(row['引进日期'.encode('utf-8')])

    if row['适航证编号到期时间'.encode('utf-8')]:
        data['acnDeadline'] = date_formate(row['适航证编号到期时间'.encode('utf-8')])

    if row['国籍登记编号到期时间'.encode('utf-8')]:
        data['slnDeadline'] = date_formate(row['国籍登记编号到期时间'.encode('utf-8')])

    if row['电台执照编号到期时间'.encode('utf-8')]:
        data['nrnDeadline'] = date_formate(row['电台执照编号到期时间'.encode('utf-8')])

    if row['制造日期'.encode('utf-8')]:
        data['manufactureDate'] = date_formate(row['制造日期'.encode('utf-8')])

    if row['初始飞行时间'.encode('utf-8')]:
        data['flightTime'] = hour_formate(row['初始飞行时间'.encode('utf-8')])
        data['totalHours'] = data['flightTime']

    if row['初始发动机时间'.encode('utf-8')]:
        data['engineTime'] = hour_formate(row['初始发动机时间'.encode('utf-8')])
        data['totalengineTime'] = data['engineTime']

    if row['初始螺旋桨时间'.encode('utf-8')]:
        data['propellerTime'] = hour_formate(row['初始螺旋桨时间'.encode('utf-8')])
        data['totalpropellerTime'] = data['propellerTime']

    if row['备注'.encode('utf-8')]:
        data['remark'] = hour_formate(row['备注'.encode('utf-8')])
        data['totalHours'] = data['flightTime']

    md5_data = json.dumps(data)
    hash_md5 = hashlib.md5(md5_data)
    data['etag'] = hash_md5.hexdigest()

    if data['manufactureDate'] > data['importedDate']:
        logging.warn('manufactureDate is bigger than importedDate.The plane id:%s' % data['id'])
        return None

    return data


def bound_mxp():

    aircraft_conn = current_app.mongodb['aircraft_information']
    plane_ids = aircraft_conn.distinct("id")

    bind_url = current_app.config['WXK_API_BASE'] + '/v1/mxp-binding/bind'
    status_url = current_app.config['WXK_API_BASE'] + '/v1/mxp-binding/status'

    msg = {
        'login': current_app.config['WXK_USERNAME'],
        'password': current_app.config['WXK_PASSWORD']
    }

    auth_url = current_app.config['PLATFORM_API_BASE'] + '/auth'

    res = requests.post(auth_url, json=msg)

    if 'accessToken' not in res.json().keys():
        logging.warn('The user is auth failed.')

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'JWT %s' % res.json()['accessToken']
    }

    count = 0
    for item in plane_ids:
        data = {
            'planeId': item,
            'force': False
        }

        try:

            res = requests.get(status_url + '?id=%s' % item, headers=header)
            if res.status_code == 200:
                data['mxpId'] = res.json()[0]['id']

            res = requests.post(bind_url, json=data, headers=header)
            if res.status_code not in [201, 200]:

                logging.warn('bind the plane faild, plane : %s' % item)
                logging.warn(res)
                continue
        except Exception as e:
            logging.warn(e)
        count += 1
    return count


def read_bind_information(row):

    data = {
        'planeId': row['飞机编号'.encode('utf-8')],
        # 'boundedId': '',  # 绑定项的唯一编号str上次完成
        # 'serialNumber': row['时寿件串号'.encode('utf-8')],#时寿件串号
        'category': row['时寿件/时控件'.encode('utf-8')],
        'mxp_id': row['对应的维修方案编号'.encode('utf-8')],
        'ellapsedTimes': 0,
        'completeDate': 0,
        'ellapsedHours': 0,
        'engineTime': 0,
    }
    if row['距离上次完成时间过后的起飞次数'.encode('utf-8')]:
        data['ellapsedTimes'] = int(row['距离上次完成时间过后的起飞次数'.encode('utf-8')])
    if row['完成时间'.encode('utf-8')]:
        data['completeDate'] = date_formate(row['完成时间'.encode('utf-8')])
    try:
        if row['距离上次完成时间过后的飞行小时数'.encode('utf-8')]:
            data['ellapsedHours'] = hour_formate(
                row['距离上次完成时间过后的飞行小时数'.encode('utf-8')])
    except Exception as e:
        logging.warn("xiaoshi:" % row['距离上次完成时间过后的飞行小时数'.encode('utf-8')])

    data['trace'] = True if row['是否跟踪'.encode('utf-8')] else False

    try:
        if row['发动机时间'.encode('utf-8')]:
            data['engineTime'] = hour_formate(row['发动机时间'.encode('utf-8')])
    except Exception as e:
        logging.warn("fagongji:%s" % row['发动机时间'.encode('utf-8')])

    data['serialNumber'] = row['时寿件串号'.encode('utf-8')].decode('utf-8').split(',')

    return data


def change_bind_information(cfg_file, col_name, read_datas=read_datas,
                            skip_first=False, clean=True):

    datas = read_file(cfg_file, read_datas, skip_first)

    aircraft_conn = current_app.mongodb['aircraft_information']

    count = 0
    for data in datas:
        collection = 'time_control_unit_y5b'
        mxp_conn = current_app.mongodb['time_control_unit_y5b']
        if data['category'] == '时寿件'.encode('utf-8'):
            collection = 'life_control_unit_y5b'
            mxp_conn = current_app.mongodb['life_control_unit_y5b']

        inst = mxp_conn.find_one(
            {"id": data['mxp_id'], "pieceNo": data['mxp_id']})

        if not inst:
            logging.warn('The mxp is not exist. Mxp: %s' % data['planeId'])
            logging.warn('The mxp is not exist. Mxp: %s' % data['serialNumber'])
            print data['mxp_id']
            continue

        ref_id = DBRef(collection, inst['_id'])

        tmp_item = aircraft_conn.find_one({
            'id': data['planeId'],
            'boundedItems.refId': ref_id}, {'boundedItems.$': 1})

        if not tmp_item:
            logging.warn('The bind information is not exit. Mxp: %s' % data['planeId'])
            logging.warn('The bind information is not exit. Mxp: %s' % data['mxp_id'].decode("utf-8"))
            logging.warn('The bind information is not exit. Mxp: %s' % data['completeDate'])
            continue

        tmp = tmp_item['boundedItems'][0]
        tmp['ellapsedTimes'] = data['ellapsedTimes']
        tmp['completeDate'] = Int64(data['completeDate'])
        tmp['ellapsedHours'] = float(data['ellapsedHours'])
        tmp['engineTime'] = float(data['engineTime'])
        tmp['trace'] = data['trace']
        # tmp['serialNumber'] = data['serialNumber']

        for i in range(len(data['serialNumber'])):
            tmp['serialNumber'] = data['serialNumber'][i]
            if i < 1:
                aa = aircraft_conn.update(
                    {'id': data['planeId'], 'boundedItems.refId': ref_id},
                    {'$set': {'boundedItems.$': tmp}}
                )
            else:
                tmp['boundedId'] = str(ObjectId())
                aa = aircraft_conn.update(
                    {'id': data['planeId'], 'boundedItems.refId': ref_id},
                    {'$addToSet': {'boundedItems': tmp}}
                )

        count = count + aa['n']

    return count
