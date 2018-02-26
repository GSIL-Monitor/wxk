# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from copy import deepcopy

import pymongo
import bson
from flask import request, current_app
from jinja2 import Markup

from modules.perms import ActionNeedPermission
from modules.flows.operations import Finish
from modules.views.warning_level import get_predict_level
from modules.support_bounded_items import support_due_list
from modules.views.warning_level import warning_level
from modules.views.helper import convert_float_to_hh_mm
from util.jinja_filter import timestamp_to_date
from modules.views.index import list_level_compare_max

from .tranlate_column import column_labels


# 默认支持的到期列表显示内容
default_duelist_columns = [
    'checkbox', 'mxId', 'description', 'leftHour', 'leftTimes',
    'leftDay', 'leftEngineTime', 'earliest', 'warningLevel',
    'error',
]


def get_mxid_by_dbref(ref_doc):
    return current_app.mongodb[ref_doc.collection].find_one({'_id': ref_doc.id})['id']


def list_compare(x, y):
    if x['predictTime']['earliest'] > y['predictTime']['earliest']:
        return 1
    elif x['predictTime']['earliest'] < y['predictTime']['earliest']:
        return -1
    else:
        level_x = list(warning_level.keys())[list(
            warning_level.values()).index(get_predict_level(x['predictTime']))]
        level_y = list(warning_level.keys())[list(
            warning_level.values()).index(get_predict_level(y['predictTime']))]
        if level_x == 0:
            return 1
        elif level_y == 0:
            return -1
        elif level_x < level_y:
            return 1
        elif level_x > y:
            return -1
        else:
            return 0


def list_compare_by_name(x, y):
    if x['mxp_id'] < y['mxp_id']:
        return -1
    elif x['mxp_id'] > y['mxp_id']:
        return 1
    else:
        return 0


class DuelistLogic(object):

    def __init__(self, view):
        self._view = view

    @property
    def can_finish(self):
        perm = ActionNeedPermission(self._view._action_name, Finish)
        return perm.can()

    @property
    def can_routine_work(self):
        return self._view.can_routine_work

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        # 参考原MongoView的实现

        # WUJG: 暂不支持额外的过滤器或搜索
        first_query = dict(_id='')
        try:
            first_query['_id'] = bson.ObjectId(request.args.get('id'))
        except:
            pass

        query = {
            # 通常情况下默认都是scheduled
            'predictTime.mxType': request.args.get('mxtype', 'scheduled'),
        }

        basic_command = [
            {'$match': first_query},
            {'$project': {'predictTime': 1}},
            {'$unwind': '$predictTime'},
            # 以预计工作时间的升序排序
            {'$sort': {'predictTime.earliest': 1}},
            {'$match': query},
        ]

        # Get count
        # TODO: 这里没找到好方法解决该问题
        count = len(list(
            self._view.coll.aggregate(basic_command)
        )) if not self._view.simple_list_pager else None

        # Sorting
        sort_by = None

        if sort_column:
            sort_by = [(
                sort_column,
                pymongo.DESCENDING if sort_desc else pymongo.ASCENDING)]
        # WUJG: 默认的行为会对_id进行排序, 这个模型不支持
        # else:
        #     order = self._view._get_default_order()

        #     if order:
        #         sort_by = [(
        #             order[0],
        #             pymongo.DESCENDING if order[1] else pymongo.ASCENDING)]

        # Pagination
        if page_size is None:
            page_size = self._view.page_size

        skip = 0

        if page and page_size:
            skip = page * page_size

        if sort_by:
            basic_command.append({'$sort': sort_by})
        # 由于需要先全部排序，所以去掉按页去查询
        # basic_command.append({
        #     '$skip': skip,
        # })
        # basic_command.append({
        #     '$limit': page_size,
        # })

        # 仅保留下面的内容

        results = self._view.coll.aggregate(basic_command)

        if execute:
            results = list(results)
        for itemval in results:
            mx_ref_db = itemval['predictTime']['mxRefId']
            mxp_id = get_mxid_by_dbref(mx_ref_db)
            if mxp_id:
                itemval['mxp_id'] = mxp_id
            else:
                itemval['mxp_id'] = ''
            itemval['level'] = get_predict_level(itemval['predictTime'])
            itemval['intervaltype'] = {}
            for intervalvalue in itemval['predictTime']['intervalTimes']:
                itemval['intervaltype'][intervalvalue['type']] = intervalvalue['left']
        results.sort(list_compare_by_name)
        results.sort(list_level_compare_max)

        if not skip and not page_size:
            return count, results
        result = results[skip:skip + page_size]
        return count, result

    def __call__(self):
        def render_aircraft_but(view, ctx, model, name):
            if self.can_finish:
                return Markup(
                    '<a type="button" class="btn btn-group-item green">'
                    '<i class="fa fa-check">&nbsp;&nbsp;完成</i>'
                    '</a>')
            else:
                return ''

        def format_left(need_format, expect_type, view, ctx, model, name):

            data = model['predictTime']

            interval_times = None
            if 'intervalTimes' in data:
                interval_times = data['intervalTimes']
            if interval_times is None:
                return ''

            for interval in interval_times:
                if interval['type'] == expect_type:
                    return Markup(need_format % interval['left'])
            return ''

        def format_left_hours(expect_type, view, ctx, model, name):

            data = model['predictTime']

            interval_times = None
            if 'intervalTimes' in data:
                interval_times = data['intervalTimes']
            if interval_times is None:
                return ''

            for interval in interval_times:
                if interval['type'] == expect_type:
                    return convert_float_to_hh_mm(interval['left'])

            return ''

        def pn_sn_formater(view, ctx, model, name):

            # 下面的操作直接在数据库里找对对应的绑定项
            _id = request.args.get('id', '')
            boundedId = model['predictTime']['itemId']

            item = self._view.coll.find_one(
                {'_id': bson.ObjectId(_id), 'boundedItems.boundedId': boundedId},
                {'boundedItems.$': True},
            )
            if item is None:
                return ''

            # 下面的内容,需要熟悉绑定状态的结构
            ref_doc = item['boundedItems'][0]['refId']
            mx_type = item['boundedItems'][0]['mxType']
            mx_info = current_app.mongodb[ref_doc.collection].find_one({'_id': ref_doc.id})

            if mx_info is None:
                return ''

            if name == 'pn':
                return mx_info['pn']

            if name == 'name':
                return mx_info['name']

            return item['boundedItems'][0]['serialNumber']

        column_list = deepcopy(default_duelist_columns)
        if request and 'mxtype' in request.args and request.args['mxtype'] in ['timecontrol', 'lifecontrol']:
            column_list.insert(2, 'pn')
            column_list.insert(3, 'serialNumber')
            column_list.insert(4, 'name')

        return {
            '_api_url': '/v1/mxp/as350/flight-line-check/',
            'template': 'aircraft/due_list.html',
            'column_labels': column_labels,
            'column_list': column_list,
            'title': '到期列表',
            'coll_name': 'aircraft_information',
            # 到期列表的查询列表方法与默认的不同
            'find_method': self.get_list,
            'extra': self.extra_args,
            'column_formatters': {
                'checkbox': self.checkbox_formatter,
                'mxId': self.predict_time_formatter,
                'description': self.predict_time_formatter,
                'warningLevel': self.predict_time_formatter,
                'earliest': self.predict_time_formatter,
                'error': self.predict_time_formatter,
                'leftHour': partial(format_left_hours, 0),
                'leftTimes': partial(format_left, '%d', 1),
                'leftDay': partial(format_left, '%d', 2),
                'leftEngineTime': partial(format_left_hours, 9),
                'pn': pn_sn_formater,
                'serialNumber': pn_sn_formater,
                'name': pn_sn_formater,
            }
        }

    def checkbox_formatter(self, view, ctx, model, name):
        return Markup(
            '<input type="checkbox" value="%s">' % (
                str(model['predictTime']['itemId'])))

    def predict_time_formatter(self, view, ctx, model, name):
        # 主要是针对要显示的那几个字段的格式化
        predict_info = model['predictTime']
        # TODO: 继续优化显示
        if name in ['mxId', 'description']:
            # 下面的处理有些许复杂，需要了解一些mongo的机制和dbref的操作
            ref_doc = predict_info['mxRefId']
            # TODO: 能做到在这里跳转到对应的维修方案么？
            mx_item = self._view._mongo[ref_doc.collection].find_one(
                {'_id': ref_doc.id})
            if mx_item is None:
                return Markup(
                    '<span class="label label-danger" data="%s">'
                    '该项数据有误，请联系开发人员</span>' % (
                        str(ref_doc.id),
                    ))
            return mx_item['id'] if name == 'mxId' else mx_item['description']

        if name in predict_info:
            if name == 'earliest':
                return timestamp_to_date(predict_info[name])
            if name == 'warningLevel':
                return get_predict_level(predict_info)
        if name == 'error':
            for interval in predict_info['intervalTimes']:
                # 返回任意一个对应间隔报错的问题
                if interval['err'] != '':
                    return interval['err']

        return ''

    def extra_args(self, *args, **kwargs):

        model = kwargs.get('model', None)
        # 如果对应的飞机实例已经绑定了方案
        if model is not None and model['boundedMxp']:
            # TODO: 找到一个好的方法以知道各种机型方案的哪些子方案可以有到期
            return {
                # TODO: 下面的key是hardcode
                'due_list_view': [item for item in support_due_list[model['planeType']] if item[2]],
                'can_routine_work': self.can_routine_work,
            }

        return {}
