# encoding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask import request, jsonify
from flask_admin import expose
from flask_admin.contrib.sqla.filters import (FilterLike, FilterEqual, FilterNotLike,
                                              TimeGreaterFilter, TimeSmallerFilter, TimeBetweenFilter,
                                              TimeEqualFilter, FilterGreater, FilterSmaller)

from .stat_base import FlightlogStatBaseView, FlightLog
from modules.models.basic_data.formula import SubFormula, Formula
from modules.models.basic_data.pesticide import Pesticide
from modules.flows.operations import View
from modules.perms import ActionNeedPermission


headers = [
    '日期', '飞机注册号',
    '飞行性质', '任务性质', '起飞机场', '降落机场',
    '作业区域', '作业亩数', '药品配方', '加药量（g）'
]

columns = [
    dict(data='flightDate', readOnly=True),
    dict(data='aircraftId', readOnly=True),
    dict(data='flyProperty', readOnly=True),
    dict(data='missionType', readOnly=True),
    dict(data='departureAirport', readOnly=True),
    dict(data='landingAirport', readOnly=True),
    dict(data='workArea', readOnly=True),
    dict(data='workAcres', readOnly=True),
    dict(data='medicinePrescription', readOnly=True),
    dict(data='weight', readOnly=True),
]


class _FormulaStatisticsView(FlightlogStatBaseView):
    "农药用量统计视图"

    list_template = 'flightlog/formula_stat.html'
    pdf_template = 'flightlog/pdf_stat.html'

    extra_js = [
        '/static/js/handsontable.min.js',
        '/static/js/formula_stat.js',
    ]

    def extra_ctx_datas(self):
        return {
            'headers': headers,
            'columns': columns,
        }

    def is_accessible(self):
        return ActionNeedPermission('formulastat', View).can()

    def __init__(self, *args, **kwargs):

        ori_column_filters = []
        ori_column_filters.extend(self.column_filters)
        self.column_filters = ori_column_filters

        self.column_filters.extend([
            FilterLike(column=FlightLog.captain, name='飞行人员1'),
            FilterNotLike(column=FlightLog.captain, name='飞行人员1'),
            FilterEqual(column=FlightLog.captain, name='飞行人员1'),

            FilterLike(column=FlightLog.copilot, name='飞行人员2'),
            FilterNotLike(column=FlightLog.copilot, name='飞行人员2'),
            FilterEqual(column=FlightLog.copilot, name='飞行人员2'),

            FilterLike(column=FlightLog.captain3, name='飞行人员3'),
            FilterNotLike(column=FlightLog.captain3, name='飞行人员3'),
            FilterEqual(column=FlightLog.captain3, name='飞行人员3'),

            FilterLike(column=FlightLog.departureAirport, name='起飞机场'),
            FilterNotLike(column=FlightLog.departureAirport, name='起飞机场'),
            FilterEqual(column=FlightLog.departureAirport, name='起飞机场'),

            FilterLike(column=FlightLog.landingAirport, name='降落机场'),
            FilterNotLike(column=FlightLog.landingAirport, name='降落机场'),
            FilterEqual(column=FlightLog.landingAirport, name='降落机场'),

            FilterLike(column=FlightLog.flyProperty, name='飞行性质'),
            FilterNotLike(column=FlightLog.flyProperty, name='飞行性质'),
            FilterEqual(column=FlightLog.flyProperty, name='飞行性质'),

            FilterLike(column=FlightLog.missionType, name='任务性质'),
            FilterNotLike(column=FlightLog.missionType, name='任务性质'),
            FilterEqual(column=FlightLog.missionType, name='任务性质'),

            FilterLike(column=FlightLog.workArea, name='作业区域'),
            FilterNotLike(column=FlightLog.workArea, name='作业区域'),
            FilterEqual(column=FlightLog.workArea, name='作业区域'),
        ])
        self.column_filters = ori_column_filters

        super(_FormulaStatisticsView, self).__init__(*args, **kwargs)

    @expose('/get-name/', methods=['GET'])
    def getName(self):
        if request.args:
            respData = []
            for x in request.args:
                num = float(request.args[x])
                # 配方信息
                FormulaData = Formula.query.filter_by(name=x).all()
                # 配方id
                FormulaId = FormulaData[0].id
                # 农药信息
                SubFormulaData = SubFormula.query.filter_by(formula_id=FormulaId).all()

                for sub in range(len(SubFormulaData)):
                    weight = float(SubFormulaData[sub].weight) * num
                    SubFormulaid = SubFormulaData[sub].pesticide_id
                    PesticideData = Pesticide.query.filter_by(id=SubFormulaid).all()
                    if PesticideData:
                        PesticideName = PesticideData[0].name
                        PesticideDict = dict(name=PesticideName, weight=weight)
                        respData.append(PesticideDict)
            return jsonify(code=200, data=respData)
        else:
            return jsonify(code=400)


FormulaStatisticsView = partial(
    _FormulaStatisticsView, FlightLog, name='加药量统计',
    endpoint='forumula-stat')
