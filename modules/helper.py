# coding: utf-8

from __future__ import unicode_literals
from collections import namedtuple

from flask import current_app
from bson import DBRef, ObjectId
import datetime

from modules.perms import ActionNeedPermission
from modules.flows.operations import View
from modules.views.helper import convert_float_to_hh_mm

from .support_bounded_items import support_due_list


BoundedItemInfo = namedtuple('BoundedItemInfo',
    ['id', 'pn', 'sn', 'mxpId', 'mxpType', 'description'])


def can_view_aircraft():
    return ActionNeedPermission('aircraft', View).can()


def get_allowed_aircrafts(plane_type=None, bounded=False):
    """获得当前用户允许的飞机列表

    注意，返回的内容为一个namedtuple，id为飞机编号，model为机型

    如果设置了bounded为True，则只返回已经存在有绑定状态的数据
    """
    AircraftTuple = namedtuple('AircraftTuple', ['id', 'model'])

    query = {}
    if plane_type is not None:
        query['planeType'] = plane_type

    if bounded:
        query['boundedMxp'] = {'$not': {'$eq': None}}

    return [AircraftTuple(id=item['id'], model=item['planeType']) for item in \
            current_app.mongodb.aircraft_information.find(query, {'id': True, 'planeType': True})]


def get_mx_item_info(plane_id, plane_type, bounded_id):

    MxItemInfo = namedtuple('MxItemInfo', ['mx_type_name', 'description', 'id', 'mx_type', 'obj'])
    item = current_app.mongodb.aircraft_information.find_one(
        {'id': plane_id, 'boundedItems.boundedId': bounded_id},
        {'boundedItems.$': True},
    )
    if item is None:
        return

    mx_type_name = ''
    mx_type = item['boundedItems'][0]['mxType']
    child_mx_types = support_due_list[plane_type]
    # 对应的方案名称
    for supported in child_mx_types:
        if supported[0] == mx_type:
            # 第二项为中文名
            mx_type_name = supported[1]
            break

    # 下面的内容,需要熟悉绑定状态的结构
    ref_doc = item['boundedItems'][0]['refId']
    mx_info = _get_mx_item_by_dbref(ref_doc)
    if mx_info is None:
        return
    return MxItemInfo(
        mx_type_name=mx_type_name, description=mx_info['description'],
        id=mx_info['id'], mx_type=mx_type, obj=mx_info)


def _get_mx_item_by_dbref(ref_doc):
    return current_app.mongodb[ref_doc.collection].find_one({'_id': ref_doc.id})


def get_aircraft_info(plane_id):
    # 使用飞机编号获取飞机实例数据, 排除绑定与推算数据
    return current_app.mongodb.aircraft_information.find_one(
        {'id': plane_id}, {'boundedItems': False, 'predictTime': False})


def get_mxp_type_id():

    id_list = []
    coll = current_app.mongodb
    type_dict = {
        '定期维修检查': coll.scheduled_mx_check_y5b,
        '时控件': coll.time_control_unit_y5b,
        '时寿件': coll.life_control_unit_y5b,
        '航线检查': coll.flight_line_check_y5b,
        '停放检查': coll.parking_mx_check_y5b,
    }

    for key, value in type_dict.iteritems():
        if key == '时控件' or key == '时寿件':
            id_list.append([mxTypeidtuple(id=item['id'], pn=item['pn'], mxpType=key, description=item['description'],)\
                for item in value.find({}, {'id':1, 'pn':1, '_id':0 ,'description':1, })])
        else:
            id_list.append([mxTypeidtuple(id=item['id'], pn='', mxpType=key, description=item['description'])\
                for item in value.find({}, {'id':1, 'pn':1, '_id':0 ,'description':1,})])
    return id_list


def get_date_after_day(strf, nday):
    try:
        if strf and nday:
            value = datetime.datetime.utcfromtimestamp(
                strf) + datetime.timedelta(days=int(nday))
            return value.strftime("%Y-%m-%d")
        else:
            return None
    except:
        return None


def get_plane_infos_by_pn(pn, plane_num, category, trace=True):
    """通过飞机号、件号和类型获取在绑定飞机的绑定状态"""
    if category not in ['时控件', '时寿件']:
        return None
    result = []
    AircraftInfoTuple = namedtuple('AircraftInfoTuple', [
        'serialNumber', 'completeDate', 'ellapsedTimes',
        'ellapsedHours', 'engineTime', 'nextCheckDate'])
    coll = current_app.mongodb
    type_key = {
        '时控件': 'time_control_unit_y5b',
        '时寿件': 'life_control_unit_y5b',
    }
    val = coll[type_key[category]].find_one({'id': pn})
    if not val:
        return None
    date_value = None
    day_dict = {2: 1, 3: 30, 4: 365}
    for interval in val.get('interval'):
        types = interval.get('type')
        if types > 1 and types < 5:
            values = interval.get('value')
            date_value = values * day_dict[types]
            break
    tmp_ref = DBRef(
        type_key[category], val['_id'])
    trace_coll = None
    if trace:
        trace_coll = {'$match': {'boundedItems.refId': tmp_ref, 'boundedItems.trace': True}}
    else:
        trace_coll = {'$match': {'boundedItems.refId': tmp_ref}}
    des = coll.aircraft_information.aggregate(
        [
            {'$match': {'id': plane_num}},
            {'$project': {'boundedItems': 1, '_id': 0}},
            {'$unwind': '$boundedItems'},
            trace_coll,
        ]
    )
    ret_list = list(des)
    for val in ret_list:
        ret = val['boundedItems']
        aircraftInfo = AircraftInfoTuple(
            serialNumber=ret['serialNumber'] if 'serialNumber' in ret.keys() else '',
            completeDate=ret['completeDate'] if 'completeDate' in ret.keys() else 0,
            ellapsedTimes=ret['ellapsedTimes'] if 'ellapsedTimes' in ret.keys() else 0,
            ellapsedHours=convert_float_to_hh_mm(ret['ellapsedHours']) if 'ellapsedHours' in ret.keys() else '00:00',
            engineTime=convert_float_to_hh_mm(ret['engineTime']) if 'engineTime' in ret.keys() else '00:00',
            nextCheckDate=get_date_after_day(ret.get('completeDate'), date_value)
        )
        result.append(aircraftInfo)
    return result


def get_pn_by_category(category):
    """获取时控件和时寿件对应的件号"""
    if category not in ['时控件', '时寿件']:
        return None
    coll = current_app.mongodb
    type_dict = {
        '时控件': coll.time_control_unit_y5b,
        '时寿件': coll.life_control_unit_y5b,
    }
    ret = type_dict[category].find({}).distinct('id')
    return ret


def get_aircraft_afterrepaired_flytime_enginetime(
        aircraftId, mxpId=['Y5B(D)', 'ASZ-62IR-6', 'J12-G15']):
    """
    # 根据飞机号获取飞机大修后的飞行时间和发动机时间
    # 大修后飞行时间维修方案：Y5B(D)对应的完成后飞行小时
    # 大修后发动机时间维修方案：ASZ-62IR-6对应的发动机时间
    # 大修后螺旋桨时间维修方案：J12-G15对应的发动机时间
    """
    FlyAndEngineTimeTuple = namedtuple('FlyandEngineTimeTuple', [
        'flyTime', 'engineTime', 'propellerTime'])

    def get_singe_query(aircraftId, mxpId, display_type):
        """
        aircraftId: 飞机号，mxpId：维修方案编号，
        display_type：是显示那种时间，是发动机时间还是飞行时间
        """
        display_hour = '00:00'
        coll = current_app.mongodb
        object_data = coll.time_control_unit_y5b.find_one({'id': mxpId})
        if object_data is None:
            return display_hour
        object_id = object_data['_id']
        dbref = DBRef('time_control_unit_y5b', object_id)
        des = coll.aircraft_information.find_one(
            {'id': aircraftId, 'boundedItems.refId': dbref},
            {'boundedItems.$': True})
        if not des:
            return display_hour
        tmp = des['boundedItems'][0]
        if display_type == 'fly':
            if 'ellapsedHours' in tmp.keys():
                display_hour = convert_float_to_hh_mm(tmp['ellapsedHours'])
        if display_type == 'engine':
            if 'engineTime' in tmp.keys():
                display_hour = convert_float_to_hh_mm(tmp['engineTime'])
        return display_hour

    result = FlyAndEngineTimeTuple(
        flyTime=get_singe_query(aircraftId, mxpId[0], 'fly'),
        engineTime=get_singe_query(aircraftId, mxpId[1], 'engine'),
        propellerTime=get_singe_query(aircraftId, mxpId[2], 'engine'),
    )
    return result


def get_aircraft_related_bounded_status(plane_id):

    status = {}
    aircraft_info = current_app.mongodb.aircraft_information.find_one(
        {'id': plane_id}, {'boundedItems': True, 'planeType': True})

    count = 0
    if aircraft_info is None:
        return status
    for x in aircraft_info:
        if x == 'boundedItems':
            count = 1
    if count == 0:
        return {}
        
    plane_type = aircraft_info['planeType']
    if aircraft_info['boundedItems'] is None:
        return {}

    # 处理该飞机的对应的绑定状态
    for bounded_item in aircraft_info['boundedItems']:
        # WUJG: 存在间隔项的内容，如果跟踪态为False则略过
        # 但是不存在间隔项的内容，可以返回
        if 'trace' in bounded_item and not bounded_item['trace']:
           continue
        sn = ''
        bounded_id = bounded_item['boundedId']
        if 'serialNumber' in bounded_item:
            sn = bounded_item['serialNumber'] or ''
        mx_info = _get_mx_item_by_dbref(bounded_item['refId'])
        if mx_info is None:
            continue
        description = mx_info['description']
        mx_id = mx_info['id']
        mx_type = bounded_item['mxType']
        pn = ''
        if mx_type in ['timecontrol', 'lifecontrol']:
            pn = mx_info['pn']

        # 转换方案类别名称
        child_mx_types = support_due_list[plane_type]
        # 对应的方案名称
        for supported in child_mx_types:
            if supported[0] == mx_type:
                # 第二项为中文名
                mx_type = supported[1]
                break

        if mx_type not in status:
            status[mx_type] = []
        status[mx_type].append(
            BoundedItemInfo(
                id=bounded_id, mxpId=mx_id, description=description,
                pn=pn, sn=sn, mxpType=mx_type))
    return status


def get_subsidiary_materials_related_available_work(plane_id, mx_id, query=None):
    """获得mx_id从属的子配件在关联飞机上的可执行项

    `Warning`: 目前限定mx_id必须为时控件的内容

    :param plane_id: 飞机编号
    :param mx_id: 维修方案编号
    :param query: 依赖的数据获取实现，应该接受`mx_id`作为查询参数，返回从属列表
    :return: 一个dict，一个是mx_id本身的可执行（到期项）信息，另一个是所属的可执行子
             到期项列表；每个可执行项内容都是一个dict，包含绑定编号、方案编号、型号（件号）及序号;
             如果不存在，是一个None
    """

    def _default_query(mx_id):
        # WUJG: 该实现的做法是从方案反推绑定状态
        # 另一种可行的办法，从绑定状态反推方案信息
        # 前一种，会导致方案的多次查询；后一种会导致方案的一次盲目查询
        # 应该由实际使用效果决定采用哪种形式

        coll = current_app.mongodb.time_control_unit_y5b
        control_unit = coll.find_one({
            'id': mx_id,
        }, {'pn': True, 'id': True})  # 仅需包含额外的型号即可

        if control_unit is None:
            return

        plane_coll = current_app.mongodb.aircraft_information

        # 找到所有附属实例
        subsidiaries = coll.find({'unitNo': control_unit['pn']}, {'id': True})

        refIds = [DBRef('time_control_unit_y5b', ObjectId(control_unit['_id']))]
        for item in subsidiaries:
            refIds.append(DBRef('time_control_unit_y5b', ObjectId(item['_id'])))

        # 查找绑定状态为跟踪，且对应数据符合下述条件的绑定项（跟踪的就是可执行的）
        available = plane_coll.aggregate([
            {'$match': {'id': plane_id}},
            {'$project': {'boundedItems': 1}},
            {'$unwind': '$boundedItems'},
            # 绑定编号对应，且为跟踪的内容
            {'$match': {'boundedItems.refId': {'$in': refIds}, 'boundedItems.trace': True}},
        ])

        ret = dict(subsidiaries=[], current=None)
        for doc in available:
            # 这个是“打散”后的每个绑定项的内容
            item = doc['boundedItems']
            ref_doc = item['refId']
            mx_info = _get_mx_item_by_dbref(ref_doc)

            obj = {
                'boundedId': item['boundedId'],
                'id': mx_info['id'],
                'pn': mx_info['pn'],
                'sn': item['serialNumber'] if 'serialNumber' in item else '',
                'description': mx_info['description'],
            }

            if mx_info['id'] != mx_id:
                ret['subsidiaries'].append(obj)
            else:
                ret['current'] = obj

        return ret

    return query(mx_id) if query is not None else _default_query(mx_id)

def get_sn_by_pn(pn=None, bounded=False):
    """根据件号查序号

    注意，返回的内容为一个namedtuple，id为飞机编号，model为机型

    如果设置了bounded为True，则只返回已经存在有绑定状态的数据
    """
    AircraftList = []

    # query = {}
    # if pn is not None:
    #     query['planeType'] = plane_type

    # if bounded:
    #     query['boundedMxp'] = {'$not': {'$eq': None}}

    # return [AircraftTuple(id=item['id'], model=item['planeType']) for item in \
    #         current_app.mongodb.aircraft_information.find(query, {'id': True, 'planeType': True})]
