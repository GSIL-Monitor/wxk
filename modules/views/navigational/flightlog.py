# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from datetime import datetime, date
from copy import deepcopy
import re
import date_converter
import collections

from flask import request, abort
from flask_security import current_user
from flask_admin import expose
from wtforms_json import from_json

from modules.proxy import proxy
from modules.models.flightlog.flightlog import FlightLog
from modules.views import CustomView, fullcanlendar_events, specified_day
from modules.views.aircraft.tranlate_column import column_labels
from modules.helper import get_allowed_aircrafts
from modules.flows import BasicFlow
from modules.flows.states import Finished, InitialState
from modules.models.basic_data.fly_nature import FlyNature
from modules.models.basic_data.airport import Airport
from modules.models.basic_data.formula import Formula
from modules.models.basic_data.pilot import Pilot
from modules.views.column_formatter import get_last_create_index
from modules.flows.operations import View
from modules.perms import ActionNeedPermission


_aircraftName = '飞行器编号'
_flyPropertyName = '飞行性质'
_inertial_mission = '惯导任务'
_takeOffAirportName = '起飞机场'
_landAirportName = '降落机场'
_formulaName = '药品配方'
_captain1 = '机长1'
_captain2 = '机长2'
_captain3 = '机长3'


# 下面的内容是飞行日志列表的显示需要的内容
# 注意顺序匹配
headers = [
    '任务类型', _flyPropertyName,  '作业区域',  _aircraftName,
    _takeOffAirportName, _landAirportName,
    # '飞行日期', 不再显示给用户，同时也不在表格中设置（通过设置该列不显示需要购买授权）
    # '开车时间',
    '滑出时间', '起飞时间', '降落时间',
    # '关车时间',
    '停止时间', '飞行时间', '发动机时间', _captain1, _captain2, _captain3, '机组成员', '其他',
    '起落次数', _formulaName, '加药量(kg)', '作业亩数', '备注',
]


# 该配置内容用于设置控件的相关属性
# 这里各顺序上的内容必须与上面的配置一致
columns = [
    # 任务类型
    dict(data='missionType', editor='select', selectOptions=['正常任务', '惯导任务']),
    # 飞行性质
    dict(data='flyProperty', editor='select', selectOptions=[]),
    dict(data='workArea'),
    # 飞行器编号
    # 用户如果删除飞机，可能会导致这里的混乱，因为原来可能已经保存了对应的日志？
    dict(data='aircraftId', editor='select', selectOptions=[]),
    # 起飞机场
    dict(data='departureAirport', editor='select', selectOptions=[]),
    # 降落机场
    dict(data='landingAirport', editor='select', selectOptions=[]),
    # 飞行日期，不再显示给用户，原因见上
    # dict(data='flightDate', readOnly=True),
    # 开车时间
    # dict(data='poweronTime', type='time', timeFormat='HH:mm:ss',
    #      correctFormat=True),
    # 滑出时间
    dict(data='skidoffTime', type='time', timeFormat='HH:mm:ss',
         correctFormat=True),
    # 起飞时间
    dict(data='departureTime', type='time', timeFormat='HH:mm:ss',
         correctFormat=True),
    # 降落时间
    dict(data='landingTime', type='time', timeFormat='HH:mm:ss',
         correctFormat=True),
    # 关车时间
    # dict(data='powerdownTime', type='time', timeFormat='HH:mm:ss',
    #      correctFormat=True),
    # 停止时间
    dict(data='stopTime', type='time', timeFormat='HH:mm:ss',
         correctFormat=True),
    dict(data='flightTime', type='time', timeFormat='HH:mm',
         correctFormat=True, readOnly=True),
    dict(data='engineTime', type='time', timeFormat='HH:mm',
         correctFormat=True, readOnly=True),
    # 机长1
    dict(data='captain', editor='select', selectOptions=[]),
    # 机长2
    dict(data='copilot', editor='select', selectOptions=[]),
    # 机长3
    dict(data='captain3', editor='select', selectOptions=[]),
    # 机组成员
    dict(data='crew'),
    # 乘客
    dict(data='passengers'),
    dict(data='landings', type='numeric', format='0', language='zh-CN'),
    dict(data='medicinePrescription', editor='select', selectOptions=[]),
    dict(data='weight', editor='select',
         selectOptions=['', '800', '900', '1000']),

    dict(data='workAcres', type='numeric', format='0.00', language='zh-CN'),
    dict(data='remark'),
]


class _FlightLogView(CustomView):

    create_template = 'flightlog/modify.html'
    list_template = 'flightlog/list.html'

    extra_js = [
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/moment.min.js',
        '/static/js/moment-duration-format.js',
        '/static/js/pikaday.js',
        '/static/js/numbro.js',
        '/static/js/languages.js',
        '/static/js/zh-CN.min.js',
        '/static/js/handsontable.min.js',
        '/static/js/fullcalendar.js',
        '/static/js/flightlog_table.js',
    ]

    extra_css = [
        '/static/css/bootstrap-datetimepicker.min.css',
        '/static/css/handsontable.min.css',
        '/static/css/pikaday.css',
        '/static/css/jquery-ui.css',
        '/static/css/fullcalendar.css',
        '/static/css/profile.css',
    ]

    # 飞行日志列表视图应显示的内容
    column_list = [
        'aircraftId', 'aircraftType', 'departureAirport', 'formmakeTime',
        'landingAirport', 'flightDate', 'captain', 'copilot', 'crew',
        'passengers', 'departureTime', 'landingTime', 'flightTime',
        'landings', 'remark', 'logTime', 'aircraftType', 'formMaker',
    ]

    # 对应内容的中文翻译
    column_labels = column_labels

    _timestamp_format = '%Y-%m-%d'

    support_flow = partial(BasicFlow, '飞行日志流', support_create=True)

    def __init__(self, *args, **kwargs):

        super(_FlightLogView, self).__init__(*args, **kwargs)

        self._create_form_class.from_json = from_json

    def is_accessible(self):
        return ActionNeedPermission('flightlog', View).can()

    @expose('/commit/', methods=['POST'])
    @specified_day
    def commit_log(self, date_str):

        def prepare_commit(data):
            self._custom_action(data, dict(), action='finish',
                                direct_commit=False)
            self.session.add(data)
            return data.to_api_data()

        try:
            exists = FlightLog.get_all_data_by_day(date_str)
            status = [data.status for data in exists]
            if Finished in status:
                return (400, '当天的日志已经提交了，你可能提交的是旧数据？', {})

            # 这个地方进行判断数据是否有相同的flightlogId 如果有，则报错
            log_ids = [data.flightlogId for data in exists]
            logId_count = collections.Counter(log_ids)
            if logId_count.values().count(1) != len(logId_count.values()):
                return (400, '当天的日志的编号有相同的，请从新填写，再提交', {})

            commit_datas = [prepare_commit(data) for data in exists]

            # 执行远程REQUEST请求
            # TODO: 写死的机型
            resp = proxy.create(commit_datas, '/v1/y5b/flightlog/?batch=1')
            if resp.status_code != 200 and resp.status_code != 201:
                raise ValueError(resp.json()['message'])

            if resp.json()['count'] != len(commit_datas):
                raise ValueError('\n'.join(resp.json()['uninserted']))

            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            return (400, unicode(ex), {})

        return (200, 'ok', {'username': current_user.realName,
                            'timestamp': date.today().strftime('%Y-%m-%d')})

    @expose('/save/', methods=['POST'])
    @specified_day
    def save_log(self, date_str):
        try:
            all_data = request.get_json()
            if all_data is None or 'datas' not in all_data:
                return (400, '请求的数据没有使用正确的格式。', {})

            all_data = all_data['datas'] or []
            if not len(all_data):
                return (400, '为什么要存储空的数据内容呢？', {})

            # TODO: 简单点，把之前的数据全部清掉
            exists = FlightLog.get_all_data_by_day(date_str)
            for item in exists:
                if item.status == Finished:
                    return (400, '当天的日志已经提交了，你可能提交的是旧数据？', {})
                self.session.delete(item)

            mission_data = self.saved_fly_type_check(all_data)
            for index, data in enumerate(all_data):
                # WUJG: 对数据的格式进行转换，以便允许生成下面的实例
                computed_data = {}
                # TODO: 徐州的机务应为停电问题导致暂存不进行必填验证
                # 但暂存验证应该是能更加确保数据准确性
                # 到底如何进行验证值得思考
                # if data[0] is None or data[0] == '':
                #     return (400, '请选择任务类型', {})
                # if data[6] is None or data[6] == '':
                #     return (400, '请输入正确的滑出时间', {})
                # if data[7] is None or data[7] == '':
                #     return (400, '请输入正确的起飞时间', {})
                # if data[8] is None or data[8] == '':
                #     return (400, '请输入正确的降落时间', {})
                # if data[9] is None or data[9] == '':
                #     return (400, '请输入正确的停止时间', {})
                for idx, cl_cfg in enumerate(columns):
                    data[idx] = data[idx] if data[idx] else ''
                    computed_data[cl_cfg['data']] = data[idx]
                    if cl_cfg['data'] == 'engineTime' and \
                            self.time_check(data[idx]) and \
                            self.relate_engineTimeCheck(computed_data):
                        arn = computed_data.get('aircraftId')
                        if arn in mission_data:
                            if mission_data[arn]:
                                computed_data['EngineTimeExtra'] = '00:06'
                            else:
                                computed_data['EngineTimeExtra'] = '00:02'
                            mission_data.pop(arn)

                form = self._create_form_class.from_json(computed_data)
                model = self.model()
                form.populate_obj(model)

                # 由于日志编号在API端计算的时候必须提供，下面使用自动生成的算法
                model.flightlogId = ''.join(['FXRZBH', date_str,
                                             '%02d' % (index + 1,)])
                model.flightDate = date_converter.string_to_date(
                    date_str, self._timestamp_format)

                # TODO: 能做到新建的新建、更新的更新吗？
                # WUJG: 为了简化，目前这里全部标识为新建
                self._custom_action(model, dict(), action='create',
                                    direct_commit=False)

                self.session.add(model)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            return (400, ex, {})

        return (200, 'ok', {'username': current_user.realName,
                            'timestamp': date.today().strftime('%Y-%m-%d')})

    @expose('/edit/')
    def create_view(self):
        # 飞行器列表编辑页面的视图处理

        if not self.can_create and \
                not self.can_edit and \
                not self.can_view_details and \
                not self.can_finish:
            return abort(403)

        timestamp = request.args.get('timestamp', None)
        if timestamp is None:
            return abort(404)
        try:
            timestamp = float(timestamp)
        except ValueError:
            return abort(404)
        except TypeError:
            return abort(404)

        timestamp_obj = date_converter.timestamp_to_datetime(timestamp)
        if timestamp_obj > datetime.now():
            return abort(404)

        td = date_converter.timestamp_to_string(
            timestamp, self._timestamp_format)

        exist = FlightLog.get_all_data_by_day(td)
        datas = []
        # 与状态相关的内容
        creator, create_time, commiter, commit_time = None, None, None, None

        # 转为可JSON序列化的内容
        # 这段for 循环的逻辑实在是尴尬
        # 为啥要这么做
        for item in exist:
            if creator is None:
                creator = get_last_create_index(
                    item, InitialState, 'createUserName')
            if create_time is None:
                create_time = get_last_create_index(
                    item, InitialState, 'createTime')
                if create_time:
                    create_time = create_time.strftime('%Y-%m-%d')
            if commiter is None:
                commiter = get_last_create_index(
                    item, Finished, 'reviewUserName')
            if commit_time is None:
                commit_time = get_last_create_index(
                    item, Finished, 'reviewTime')
                if commit_time:
                    commit_time = commit_time.strftime('%Y-%m-%d')

            datas.append(item.to_json())

        # 获取可选择的飞机
        _columns = deepcopy(columns)
        # TODO: 注意，目前强制编码为y5b的飞机
        _columns[headers.index(_aircraftName)]['selectOptions'] = [
            aircraft.id for aircraft in get_allowed_aircrafts('y5b')]
        _columns[headers.index(_flyPropertyName)]['selectOptions'] = [
            item.name for item in FlyNature.query.all()]
        allowed_airports = [item.name for item in Airport.query.all()]
        _columns[headers.index(_takeOffAirportName)][
            'selectOptions'] = allowed_airports
        _columns[headers.index(_landAirportName)][
            'selectOptions'] = allowed_airports
        _columns[headers.index(_formulaName)]['selectOptions'] = [
            item.name for item in Formula.query.all()]
        # 获取允许的飞行员
        _columns[headers.index(_captain1)]['selectOptions'] = [
            item.name for item in Pilot.get_all()]
        _columns[headers.index(_captain2)]['selectOptions'] = [
            item.name for item in Pilot.get_all()]
        _columns[headers.index(_captain3)]['selectOptions'] = [
            item.name for item in Pilot.get_all()]

        is_readonly = FlightLog.has_related_status_by_day(td, Finished)

        contextMenu = {
            "items": {
                "row_above": {
                    "name": '向上新增一行',
                },
                "row_below": {
                    "name": '向下新增一行',
                },
                "remove_row": {
                    "name": '删除选中行',
                },
                "hsep1": "---------",
                "undo": {
                    "name": '撤销',
                },
                "redo": {
                    "name": '重做',
                }
            }
        }

        if not self.can_create:
            contextMenu['items'].pop('row_above')
            contextMenu['items'].pop('row_below')

        if not self.can_delete:
            contextMenu['items'].pop('remove_row')

        if is_readonly:
            contextMenu = None
            # 每一个内容都不允许编辑
            for item in _columns:
                item['readOnly'] = True
        return self.render(
            template=self.create_template,
            form=self.create_form(),
            headers=headers,
            columns=_columns,
            date_str=td,
            datas=datas,
            save_url=self.get_url('.save_log'),
            commit_url=self.get_url('.commit_log'),
            creator=creator,
            createTime=create_time,
            commiter=commiter,
            commitTime=commit_time,
            is_readonly=is_readonly,
            can_create=self.can_create,
            can_delete=self.can_delete,
            can_edit=self.can_edit,
            can_commit=self.can_finish,
            context_menu=contextMenu,
            time_columns=[
                # headers.index('开车时间'),
                headers.index('滑出时间'),
                headers.index('起飞时间'),
                headers.index('降落时间'),
                # headers.index('关车时间'),
                headers.index('停止时间'),
            ],
            calc_index={
                'typeProp': 'missionType',
                'typeIndex': headers.index('任务类型'),
                'startProp': 'skidoffTime',
                'startIndex': headers.index('滑出时间'),
                'endProp': 'stopTime',
                'endIndex': headers.index('停止时间'),
                'aircraftIdIndex': headers.index(_aircraftName),
                'aircraftIdProp': 'aircraftId',
                'flightTimeIndex': headers.index('飞行时间'),
                'engineTimeProp': 'engineTime',
                'engineTimeIndex': headers.index('发动机时间'),
            },
        )

    @expose('/all-events/')
    @fullcanlendar_events
    def get_events(self, date_str, timestamp):
        # 首先查是否有完成的日志，其优先级最高
        flightlog_title = u'编辑飞行日志' \
            if not FlightLog.has_related_status_by_day(date_str, Finished) \
            else u'查看飞行日志'
        className = 'label label-success'
        if '编辑' in flightlog_title:
            className = 'label label-primary'

            # 但是如果实际上不存在飞行日志的话，我们应该提示为新建
            if not FlightLog.has_related_status_by_day(date_str):
                flightlog_title = u'新增飞行日志'
                className = 'label label-info'

        if '新增' in flightlog_title and not self.can_create:
            return
        if '编辑' in flightlog_title and not self.can_edit:
            return
        if '查看' in flightlog_title and not self.can_view_details:
            return

        return (self.get_url('.edit_view', timestamp=timestamp),
                flightlog_title, className)

    def saved_fly_type_check(self, data):
        check = {}
        for item in data:
            fly_type, arn, engineTime = item[0], item[3], item[11]
            if fly_type and arn and engineTime:
                check[arn] = False
                if not check[arn] and fly_type == _inertial_mission:
                    check[arn] = True
        return check

    def time_check(self, time):

        time_reg = r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$'

        if not time or not re.match(time_reg, time):
            return False
        return True

    def relate_engineTimeCheck(self, data):

        fields = ['missionType', 'aircraftId', 'engineTime']

        return reduce(lambda x, y: x and y,
                      map(lambda f: data.get(f) is not None, fields))


FlightLogView = partial(
    _FlightLogView, FlightLog, name='飞行日志',
    endpoint='flightlog'
)
