# encoding: utf-8

from __future__ import unicode_literals

from flask import abort, request
from flask_admin import expose
from flask_admin.contrib.sqla.filters import (FilterLike, FilterEqual, FilterNotLike,
                                              DateNotBetweenFilter, DateBetweenFilter,
                                              DateEqualFilter, DateGreaterFilter, DateSmallerFilter)
from flask_weasyprint import HTML, render_pdf

from modules.models.flightlog.flightlog import FlightLog
from modules.views import CustomView
from modules.perms import ActionNeedPermission
from modules.flows.operations import View
from modules.flows.states import Finished
from modules.models.basic_data.formula import SubFormula, Formula
from modules.models.basic_data.pesticide import Pesticide


class FlightlogStatBaseView(CustomView):

    extra_css = [
        '/static/css/handsontable.min.css',
    ]

    pdf_css = 'assets/static/css/pdf.css'
    pdf_template = 'flightlog/pdf.html'

    column_filters = [
        FilterLike(column=FlightLog.aircraftId, name='飞机注册号'),
        FilterNotLike(column=FlightLog.aircraftId, name='飞机注册号'),
        FilterEqual(column=FlightLog.aircraftId, name='飞机注册号'),

        DateEqualFilter(column=FlightLog.flightDate, name='飞行日期'),
        DateBetweenFilter(column=FlightLog.flightDate, name='飞行日期'),
        DateNotBetweenFilter(column=FlightLog.flightDate, name='飞行日期'),
        DateGreaterFilter(column=FlightLog.flightDate, name='飞行日期'),
        DateSmallerFilter(column=FlightLog.flightDate, name='飞行日期'),
    ]

    def is_accessible(self):
        return ActionNeedPermission('flightlog', View).can()

    def get_query(self):
        # 不要使用父类的方法，因为可能涉及流程，而此处无需流程可能的逻辑
        # 仅能查询已经完成的
        return FlightLog.query.filter(FlightLog.status==Finished)

    def extra_ctx_datas(self):
        raise NotImplementedError()

    @expose()
    def index_view(self):
        return self._view_handler(self.list_template)

    def _view_handler(self, template_name, with_404=False):
        view_args = self._get_list_extra_args()

        if 'pdf.html' in template_name:
            tag = 'stat'
        elif 'pdf_stat.html' in template_name:
            tag = 'formula'
        else:
            tag = False

        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]

        page_size = view_args.page_size or self.page_size

        count, data = self.get_list(view_args.page, sort_column, view_args.sort_desc,
                                    view_args.search, view_args.filters, page_size=page_size)

        if with_404 and not view_args.filters:
            return abort(404)

        converted_data = []
        active_data = []
        result = False
        # 需要提供过滤参数才会考虑
        if view_args.filters and data is not None:
            result = True
            totalFlightTime = []
            totalEngineTime = []
            totalLanding = []
            yaopin = []


            for i in data:
                if i.medicinePrescription:
                    yaopin.append((dict(name=i.medicinePrescription,num=i.workAcres)))
                totalFlightTime.append(i.flightTime)
                totalEngineTime.append(i.engineTime)
                totalLanding.append(i.landings)
                converted_data.append(i.to_json())
            respData = []
            total = {}

            if yaopin:
                for item in yaopin:
                    if item['name'] in total.keys():
                        if item['num']:
                            if total[item['name']]:
                                total[item['name']] += item['num']
                                continue
                    total[item['name']] = item['num']
                for x in total:
                    num = total[x]
                    if num is not None:
                        # 配方信息
                        FormulaData = Formula.query.filter_by(name=x).all()
                        # 配方id
                        FormulaId = FormulaData[0].id
                        # 农药信息
                        SubFormulaData = SubFormula.query.filter_by(formula_id=FormulaId).all()
                        if SubFormulaData is not None:
                            for sub in range(len(SubFormulaData)):
                                if SubFormulaData[sub].weight is not None:
                                    weight = float(SubFormulaData[sub].weight) * num
                                else:
                                    weight = ''
                                SubFormulaid = SubFormulaData[sub].pesticide_id
                                if SubFormulaid:
                                    PesticideData = Pesticide.query.filter_by(id=SubFormulaid).all()
                                    if PesticideData:
                                        PesticideName = PesticideData[0].name
                                        PesticideDict = dict(name=PesticideName, weight=weight)
                                        respData.append(PesticideDict)

                response = {}
                for x in respData:
                    if x['name'] in response.keys():
                        response[x['name']] += x['weight']
                        continue
                    response[x['name']] = x['weight']

            totalFlightTime = self.calTotalTimeWithFormat(totalFlightTime)
            totalEngineTime = self.calTotalTimeWithFormat(totalEngineTime)
            totalLanding = self.calcLandingsWithFormat(totalLanding)

            for index,val in enumerate(view_args.filters):
                listData = list(val)

                for num in listData:
                    if num == 7:
                        listData[0] = '小于'
                    elif num  in [3, 10]:
                        listData[0] = '等于'
                    elif num == 6:
                        listData[0] = '大于'
                    elif num == 4:
                        listData[0] = '之间'
                    elif num == 5:
                        listData[0] = '不是之间'
                    elif num in [0, 8,  11, 12, 15, 18, 21, 26, 29]:
                        listData[0] = '包含'
                    elif num in [1, 9, 13, 16, 19, 22, 30, 24, 27]:
                        listData[0] = '不包含'
                    elif num in [2, 14, 17, 20, 23, 28, 31, 25]:
                        listData[0] = '等于'
                    if tag == 'formula':
                        if num in [13, 16, 19, 22, 25]:
                            listData[0] = '等于'
                        if num in [11, 14, 17, 20, 23]:
                            listData[0] = '包含'
                        if num in [9, 12, 15, 18, 21, 24]:
                            listData[0] = '不包含'

                active_data.append(tuple(listData))
        extra_ctx_datas = self.extra_ctx_datas()

        url_args = request.args
        extra_ctx_datas.update({
            'url_args': url_args,
        })

        if result and tag:
            if tag == 'stat':
                return self.render(
                    template_name,

                    data=converted_data,
                    # 与过滤相关的内容
                    totalFlightTime=totalFlightTime,
                    totalEngineTime=totalEngineTime,
                    totalLanding=totalLanding,
                    filters=self._filters,
                    filter_groups=self._get_filter_groups(),
                    active_filters=view_args.filters,
                    active_data=active_data,
                    filter_args=self._get_filters(view_args.filters),

                    **extra_ctx_datas
                )
            elif tag == 'formula':
                if response is None:
                    response = ''
                return self.render(
                    template_name,

                    data=converted_data,
                    response=response,
                    # 与过滤相关的内容
                    totalFlightTime=totalFlightTime,
                    totalEngineTime=totalEngineTime,
                    totalLanding=totalLanding,
                    filters=self._filters,
                    filter_groups=self._get_filter_groups(),
                    active_filters=view_args.filters,
                    active_data=active_data,
                    filter_args=self._get_filters(view_args.filters),

                    **extra_ctx_datas
                )
        else:
            return self.render(
                template_name,

                data=converted_data,
                # 与过滤相关的内容
                filters=self._filters,
                filter_groups=self._get_filter_groups(),
                active_filters=view_args.filters,
                active_data=active_data,
                filter_args=self._get_filters(view_args.filters),

                **extra_ctx_datas
            )

    def calTotalTimeWithFormat(self, datas):
        # 每个数据应该都是HH:mm的格式
        total = 0;
        for index,value in enumerate(datas):
            if datas[index] is None:
                continue;
            parts = datas[index].split(":")
            total = total + (float(parts[0]) * 60) + float(parts[1])

        hours_part = int(total) / 60
        minute_parts = int(total - (hours_part * 60))
        if hours_part < 10:
            hours_part = '0'+str(hours_part)
        return '%s:%s' % (hours_part, minute_parts)

    def calcLandingsWithFormat(self, datas):
        # 每个数据应该都是HH:mm的格式
        total = 0;
        for index,value in enumerate(datas):
            if datas[index] is None:
                continue;
            total = total + int(datas[index])
        return total

    @expose('/pdf/')
    def pdf_view(self):
        return render_pdf(HTML(string=self._view_handler(self.pdf_template, True)),
            stylesheets=[self.pdf_css])
