# coding: utf-8

from __future__ import unicode_literals

import time
from flask import current_app
from .basic_flow import BasicFlow
from .operations import *
from .states import OutStored, InitialState, Edited, Assembled
from util.exception import BackendServiceError
from ..proxy import proxy
from util.helper import convert_hh_mm_to_float
from modules.models.airmaterial.storage_list import AirMaterialStorageList


class AssembleFlow(BasicFlow):
    """装机流程"""

    states = ['created', 'edited', 'finished', 'assembled']

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'assembled': Assembled,

    }

    def add_transition(self):

        # 新建和编辑都可以提交
        self.machine.add_transition(trigger=Finish, source='created',
                                    dest='assembled',
                                    after='set_status')
        self.machine.add_transition(trigger=Finish, source='edited',
                                    dest='assembled',
                                    after='set_status')
        super(AssembleFlow, self).add_transition()

    def set_status(self, **kwargs):
        self.update_allowed_change(**kwargs)

        inst = self.model.assembleApplication
        if inst:
            inst.status = inst.auditStatus = Assembled
        self.update_to_bounded_status()

    # 当完成装机以后把件号和序号更新到绑定状态中，并完成到期列表推算
    def update_to_bounded_status(self):
        bounded_items = []
        coll = current_app.mongodb
        type_dict = {
            '时控件': coll.time_control_unit_y5b,
            '时寿件': coll.life_control_unit_y5b,
        }
        mxType = {
            '时控件': 'timecontrol',
            '时寿件': 'lifecontrol',
        }
        for material in self.model.assembleApplicationList:
            if material.category in ['时控件', '时寿件'] and material.planeNum and material.serialNum:
                tmp = AirMaterialStorageList.query.filter(
                    AirMaterialStorageList.partNumber == material.partNumber,
                    AirMaterialStorageList.serialNum == material.serialNum).first()
                if tmp:
                    raise ValueError('件号为%s,序号为%s的航材没有完成装机出库' % (
                        material.partNumber, material.serialNum))
        for material in self.model.assembleApplicationList:
            if material.category in ['时控件', '时寿件'] and material.planeNum and material.serialNum:
                # 获取维修方案编号
                mx_p = type_dict[material.category].find_one(
                    {'id': material.partNumber})
                if not mx_p:
                    raise ValueError('没有件号"%s"的维修方案' % (material.partNumber))
                mxId = mx_p['id']
                # 客户端增加时寿件或时控件绑定状态的处理逻辑部分
                resp = proxy.create(
                    {
                        'mxId': mxId,
                        'mxType': mxType[material.category],
                        'planeId': material.planeNum,
                    },
                    '/v1/mxp-binding/duplicate')
                if resp.status_code == 200:
                    bounded_id = resp.json()['boundedId']
                    bounded_item = {
                        'engineTime': convert_hh_mm_to_float(material.engineTime) if material.engineTime else 0,
                        'trace': True,
                        'serialNumber': material.serialNum,
                        'completeDate': str_to_time(material.lastCheckDate),
                        'nf': None,
                        'tc': None,
                        'ng': None,
                        'ellapsedTimes': material.flightTimes if material.flightTimes else 0,
                        'retiredIndex': None,
                        'ellapsedHours': convert_hh_mm_to_float(material.flyTime) if material.flyTime else 0,
                        'boundedId': bounded_id,
                    }
                    bounded_items.append(bounded_item)

        if len(bounded_items) > 0:
            resp = proxy.update(
                bounded_items, None,
                '/v1/mxp-binding/update?batch=1')
            if resp.status_code != 200:
                raise BackendServiceError('更新绑定状态失败')


def str_to_time(timestring):
    if not timestring:
        return 0
    return int(time.mktime(time.strptime(timestring, '%Y-%m-%d')))
