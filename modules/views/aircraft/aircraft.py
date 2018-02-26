# coding: utf-8

from __future__ import unicode_literals
import logging
from math import ceil
import datetime
import bson

import pymongo
from flask import redirect, flash, request, abort, current_app, jsonify
from flask_admin.babel import gettext
from flask_admin.base import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.contrib.pymongo.filters import FilterEqual
from jinja2 import Markup
from flask_admin.model.template import macro
from flask_admin.model.template import TemplateLinkRowAction
from flask import jsonify
from wtforms.validators import Length, DataRequired

from modules.cache import cache
from modules.flows.operations import Create, Edit, Delete, View
from modules.forms.aircraft.aircraft import AircraftInformationForm
from modules.views.mongo_custom_view import MongoCustomView
from modules.perms import ActionNeedPermission
from modules.flows.operations import EditBoundStatus, RemoveBoundStatus
from modules.helper import (
    get_aircraft_info, get_subsidiary_materials_related_available_work,
    get_aircraft_afterrepaired_flytime_enginetime,
)
from modules.views.helper import hour_formater

from .basic import Basic
from .flight_log import FlightLog
from .maintenance_log import MaintenanceLog
from .tranlate_column import column_labels
from .due_list import DuelistLogic, support_due_list
from modules.views.helper import convert_float_to_hh_mm


log = logging.getLogger("flask-admin.pymongo")


def aircrafttype_formatter(view, ctx, model, name, id_name=None):
    id_name = 'id' if id_name is None else id_name
    plane = get_aircraft_info(model[id_name])

    # 有显示名称用显示名称
    if 'displayName' in plane:
        return plane['displayName'] or model[name]

    return model[name]


class AircraftInformationView(MongoCustomView):
    "飞行器的通用视图"

    create_template = 'aircraft/create.html'
    details_modal_template = 'modal/details.html'
    edit_modal_template = 'modal/edit.html'
    create_modal_template = 'modal/create.html'

    # 为了使用datepicker相关插件
    extra_js = [
        '/static/js/list_light.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/jquery.magnific-popup.min.js',
        '/static/js/custom_action.js',
        '/static/js/jquery.json-2.2.js',
        '/static/js/datetostr.js',
        # 利用率的弹出框
        '/static/js/jquery.uniform.min.js',
        '/static/js/jquery.slimscroll.min.js',
        '/static/js/jquery.mockjax.js',
        '/static/js/bootstrap-editable.js',
        # select插件
        '/static/js/jquery-migrate.min.js',
        '/static/js/jquery.blockUI.min.js',
        '/static/js/bootstrap-selectsplitter.min.js',
        '/static/js/components-form-tools2.js',
        '/static/js/bluebird.js',
    ]

    extra_css = [
        '/static/css/aircraft.css',
        # '/static/css/bootstrap-switch.min.css',
        '/static/css/bootstrap-editable.css',
        # '/static/css/fonts.css',
        '/static/css/datepicker.css',
        '/static/css/bootstrap-datetimepicker.min.css',
    ]

    column_labels = column_labels

    support_popup = True

    column_list = (
        'id', 'planeType',
        'totalHours', 'totalTimes',
        'boundedMxp',
    )

    details_modal = True
    create_modal = True
    edit_modal = True

    form = AircraftInformationForm

    one_line_columns = ['imageUrl', 'etag']

    column_filters = [
        FilterEqual(column='aircraftId', name='aircraftId'),
        FilterEqual(column='aircraftType', name='aircraftType'),
    ]

    def basic_operation(view, ctx, model, name):
        # 操作按钮
        html = [
            '<div class="clearfix">'
            '<div class="btn-group btn-group-xs btn-group-solid">']
        for op in _buttons_map:
            html.append(_buttons_map[op].render_ctx(
                ctx, view.get_pk_value(model), model))

        html.append('</div></div>')
        return Markup(''.join(html))

    def render_aircraft_id(view, ctx, model, name):
        # 由于分为多个页面，如果存在sub指示为非机队列表首页
        sub = request.args.get('sub', None)

        # 如果用户无法查看飞机详情，只显示对应的名称即可
        if view.can_view_details and sub is None:
            return Markup('<a class="btn grey-steel btn-xs green-stripe" href="%s"><i class="fa fa-plane"></i>%s</a>' % (
                view.get_url('.aircraft_details_view', id=str(model['_id']),
                             sub='basic'), model['id']))

        return Markup('<span class="label label-info">%s</span>' % (model['id'],))

    _column_formatters = {
        'id': render_aircraft_id,
        'planeType': aircrafttype_formatter,
        'operation': basic_operation,
        'departureTime': macro('timetostr'),
        'landingTime': macro('timetostr'),
        'importedDate': macro('timetostr'),
        'manufactureDate': macro('timetodate'),
        'acnDeadline': macro('timetodate'),
        'slnDeadline': macro('timetodate'),
        'nrnDeadline': macro('timetodate'),
        'totalHours': hour_formater,
    }

    # 绑定状态缓存，无需频繁查询
    # WUJG: 这里缓存还是去掉吧，正常情况下，原来担心的API访问速度慢的问题一定是
    # 部署导致的
    # @cache.memoize(timeout=3600*24)
    def get_bindable_status(self, model):
        resp = self._api_proxy.get(
            '/v1/mxp-binding/status?id=%s' % (model['id'],))
        bounded_status = []
        if resp.status_code == 200:
            bounded_status = resp.json()
            for item in bounded_status:
                if 'status' in item and item['status']:
                    return bounded_status, True
        return bounded_status, False

    @expose('/bind-mxp', methods=['POST'])
    def bind_mxp(self):
        mxp_id = request.args.get('id', '')
        plane_id = request.args.get('plane', '')
        return_url = request.args.get('return_url') or get_redirect_target() or self.get_url('.index_view')
        # 默认为解除绑定
        is_bind = request.args.get('bind', '')

        dest_url = '/v1/mxp-binding/unbind'
        if is_bind:
            dest_url = '/v1/mxp-binding/bind'

        if not mxp_id or not plane_id:
            return redirect(return_url)

        resp = self._api_proxy.create({
            'force': True,
            'mxpId': mxp_id,
            'planeId': plane_id,
        }, dest_url)

        if resp.status_code != 200:
            return abort(503)

        cache.delete_memoized(self.get_bindable_status)
        return redirect(return_url)

    @expose('/update-util/', methods=['POST'])
    def update_util(self):

        return_url = get_redirect_target() or self.get_url('.index_view')
        # 正常应该跳转到对应飞机的详情页
        id = request.args.get('id', '')
        if request.form.get('name') == 'hours':
            times = None
            hours = request.form.get('value', None)
            if hours is not None:
                hours = float(hours)
        elif request.form.get('name') == 'times':
            hours = None
            times = request.form.get('value', None)
            if times is not None:
                times = int(float(times))

        if id:
            return_url = self.get_url(
                '.aircraft_details_view', id=id, sub='basic')
            try:
                self._api_proxy.create({
                    'id': id,
                    'hours': hours,
                    'times': times,
                }, '/v1/utilization/')
            except Exception as ex:
                # TODO: 客户端应该根据返回的JSON数据确定是否保存成功
                return jsonify(status='400', message=unicode(ex))
        # TODO: 根据前端所需要的JSON内容进行返回
        return jsonify(status='200', msg='ok', times=times, hours=hours)

    @expose('/aircraft-details/')
    def aircraft_details_view(self):
        sub = request.args.get('sub')
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_view_details:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        model = self.get_aircraft(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        # 获得绑定状态
        bind_status, bounded = self.get_bindable_status(model)

        # 获得当前飞机实例支持的绑定状态
        # 无需显示的绑定状态会在构建列表时剔除
        boundable_categories = [{ 'id': item[0], 'name': item[1]}
                                for item in support_due_list[model['planeType']] if item[2]]

        self._template_args.update({
            'sub': sub,
            'bind_status': bind_status,
            'bounded': bounded,
            'support_bounded_categories': boundable_categories,
        })

        find_method = self._delegate_to_sub('find_method') or self.get_list

        extra_args = self._delegate_to_sub('extra') or {}

        if callable(extra_args):
            extra_args = extra_args(model=model)

        self._template_args.update(**extra_args)
        self._template_args.update({
            'sub': sub,
            'time_formatter': datetime.time,
        })
        return self.render_aircraft_or_list(
            id, model, sub, return_url, find_method, **extra_args)

    def get_aircraft(self, id):
        return self._mongo[self.view_list['basic']['coll_name']].find_one(
            {'_id': self._get_valid_id(id)}, {'predictTime': False, 'boundedItems': False})

    @property
    def view_list(self):
        # 每一个具体的子方案在界面视图处理时应该提供下面的信息
        # 1. 子方案的名称
        # 2. 子方案对应的主键
        # 3. 子方案的集合名称（mongo）
        # 4. 一些与flask-admin相关的视图配置信息
        return {
            'basic': dict(**Basic()),
            'flightlog': dict(**FlightLog()),
            'due_list': dict(**DuelistLogic(self)()),
            'maintenancelog': dict(**MaintenanceLog()),
        }

    def render_aircraft_or_list(
            self, id, model, sub, return_url, find_method, **kwargs):
        """
        :param model: 通常就是飞机实例
        :param sub: 当前的子视图
        :param find_method: 根据需要可能替换为子文档的查询
        """
        template = self._delegate_to_sub('template')

        for x in model:
            if x != 'imageUrl':
                if model[x] is None:
                    model[x] = '--'
        ret = get_aircraft_afterrepaired_flytime_enginetime(model['id'])
        total_ellapse_hour = '00:00'
        total_engine_time = '00:00'
        total_propeller_time = '00:00'
        if ret:
            total_ellapse_hour = ret.flyTime
            total_engine_time = ret.engineTime
            total_propeller_time = ret.propellerTime
        if not sub or sub == 'basic':
            return self.render(
                template,
                model=model,
                total_ellapse_hour=total_ellapse_hour,
                total_engine_time=total_engine_time,
                total_propeller_time=total_propeller_time,
                id=id,
                return_url=return_url)

        # WUJG: 下面的实现，类似于显示列表页，绝大多数重复使用了原Index view的实现

        if self.can_delete:
            delete_form = self.delete_form()
        else:
            delete_form = None

        # Grab parameters from URL
        view_args = self._get_list_extra_args()
        # Map column index to column name
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]

        # Get page size
        page_size = view_args.page_size or self.page_size

        # Get count and data
        count, data = find_method(
            view_args.page, sort_column, view_args.sort_desc,
            view_args.search, view_args.filters, page_size=page_size)

        list_forms = {}
        if self.column_editable_list:
            for row in data:
                list_forms[self.get_pk_value(row)] = self.list_form(obj=row)

        # Calculate number of pages
        if count is not None and page_size:
            num_pages = int(ceil(count / float(page_size)))
        elif not page_size:
            num_pages = 0  # hide pager for unlimited page_size
        else:
            num_pages = None  # use simple pager

        # Various URL generation helpers
        def pager_url(p):
            # Do not add page number if it is first page
            if p == 0:
                p = None

            return self._get_list_url(view_args.clone(page=p))

        def sort_url(column, invert=False, desc=None):
            if not desc and invert and not view_args.sort_desc:
                desc = 1

            return self._get_list_url(view_args.clone(
                sort=column, sort_desc=desc))

        def page_size_url(s):
            if not s:
                s = self.page_size

            return self._get_list_url(view_args.clone(page_size=s))

        # Actions
        actions, actions_confirmation = self.get_actions_list()
        if actions:
            action_form = self.action_form()
        else:
            action_form = None

        clear_search_url = self._get_list_url(
            view_args.clone(page=0,
                            sort=view_args.sort,
                            sort_desc=view_args.sort_desc,
                            search=None,
                            filters=None))

        return self.render(
            template,
            model=model,
            data=data,
            list_forms=list_forms,
            delete_form=delete_form,
            action_form=action_form,

            # List
            list_columns=self.get_column_names(
                only_columns=self.scaffold_list_columns(),
                excluded_columns=self.column_exclude_list,
            ),
            sortable_columns=self._sortable_columns,
            editable_columns=self.column_editable_list,
            list_row_actions=self.get_list_row_actions(),

            # Pagination
            count=count,
            pager_url=pager_url,
            num_pages=num_pages,
            can_set_page_size=self.can_set_page_size,
            page_size_url=page_size_url,
            page=view_args.page,
            page_size=page_size,
            default_page_size=self.page_size,

            # Sorting
            sort_column=view_args.sort,
            sort_desc=view_args.sort_desc,
            sort_url=sort_url,

            # Search
            search_supported=self._search_supported,
            clear_search_url=clear_search_url,
            search=view_args.search,

            # Filters
            filters=self._filters,
            filter_groups=self._get_filter_groups(),
            active_filters=view_args.filters,
            filter_args=self._get_filters(view_args.filters),

            # Actions
            actions=actions,
            actions_confirmation=actions_confirmation,

            # Misc
            enumerate=enumerate,
            get_pk_value=self.get_pk_value,
            get_value=self.get_list_value,
            return_url=self._get_list_url(view_args),
            **kwargs
        )

    @property
    def default_subordinate_view(self):
        return 'basic'

    @property
    def _details_columns(self):
        return self.get_column_names(
            only_columns=self._delegate_to_sub('details_columns'),
            excluded_columns=self.column_details_exclude_list)

    def get_real_url(self, url, model):
        requestPath = request.path.split('/')
        if 'delete' in requestPath:
            url = url % {'plane_type': ''}
        else:
            sub = request.args.get('sub', self.default_subordinate_view)

            plane_type_dict = dict(
                basic='planeType',
                flightlog='aircraftType')

            if sub not in plane_type_dict:
                raise ValueError('Not correct subordinate view type.')
            url = url % {'plane_type': model[plane_type_dict[sub]] + '/'}
        return url

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        # if request.method == 'POST':
        #     engineTime = request.form['engineTime']
        #     if engineTime is not None:
 
        # 在该视图下，当前支持飞机实例和飞行日志实例的创建
        # 这里的主要逻辑是判断使用哪个窗体来创建对应的实例

        # 注意, super使用的就是MongoCustomView而非AircraftInformationView
        sub = request.args.get('sub', self.default_subordinate_view)
        aircraft_type = request.args.get('type', '').lower()
        if not aircraft_type:
            self._create_form_class = self._delegate_to_sub('form')
            return super(MongoCustomView, self).create_view()

        allowed_forms = self._delegate_to_sub('form')
        if aircraft_type not in allowed_forms:
            return abort(400)

        self._create_form_class = allowed_forms.get(aircraft_type)
        self._template_args.update({
            'sub': sub,
            'type': aircraft_type,
        })

        return super(MongoCustomView, self).create_view()

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        # 类似于create_view的逻辑，但要复杂一些，因为编辑时，即使飞机实例本身
        # 也会存在机型信息
        return_url = request.url or self.get_url('.index_view')
        aircraft_type = request.args.get('type', '').lower()

        if not aircraft_type:
            return redirect(return_url)

        sub = request.args.get('sub', self.default_subordinate_view)
        self._template_args.update({
            'sub': sub,
            'type': aircraft_type,
        })
        if sub == self.default_subordinate_view:
            self._edit_form_class = self._delegate_to_sub('form')
            return super(MongoCustomView, self).edit_view()

        if sub == 'flightlog':
            allowed_forms = self._delegate_to_sub('form')
            if aircraft_type not in allowed_forms:
                return abort(400)

            self._edit_form_class = allowed_forms.get(aircraft_type)

        return super(MongoCustomView, self).edit_view()

    def get_save_return_url(self, model, is_created):
        sub = request.args.get('sub')
        type = request.args.get('type')

        if sub == 'basic':
            id = request.args.get('id')
            if 'edit' in request.url:
                return self.get_url(
                    '.aircraft_details_view', id=id, type=type, sub=sub)
            elif 'delete' in request.url:
                return self.get_url('.aircraft_details_view')
        elif sub == 'flightlog':
            id = request.args.get('basicId')
            return self.get_url(
                '.aircraft_details_view',
                flt_0=model['aircraftId'], id=id, flt_1=type, sub=sub)
        elif sub is None:
            return self.get_url('.aircraft_details_view')

    def get_one(self, id):
        # WUJG: 重写该方法实现，避免包含不必要的数据
        return self.coll.find_one(
            {'_id': self._get_valid_id(id)},
            projection={'predictTime': False, 'boundedItems': False})

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        # WUJG: 这里的实现，几乎与flask-admin的框架实现一样，唯一不同的就是查询时做了
        # 投影的设置，避免数据过大，导致加载很慢的问题
        query = {}

        # Filters
        if self._filters:
            data = []

            for flt, flt_name, value in filters:
                f = self._filters[flt]
                data = f.apply(data, value)

            if data:
                if len(data) == 1:
                    query = data[0]
                else:
                    query['$and'] = data

        # Search
        if self._search_supported and search:
            query = self._search(query, search)

        # Get count
        count = self.coll.find(query, projection={
                'id': True,
            }).count() if not self.simple_list_pager else None

        # Sorting
        sort_by = None

        if sort_column:
            sort_by = [(
                sort_column,
                pymongo.DESCENDING if sort_desc else pymongo.ASCENDING)]
        else:
            order = self._get_default_order()

            if order:
                sort_by = [(
                    order[0],
                    pymongo.DESCENDING if order[1] else pymongo.ASCENDING)]

        # Pagination
        if page_size is None:
            page_size = self.page_size

        skip = 0

        if page and page_size:
            skip = page * page_size

        results = self.coll.find(
            query, sort=sort_by, skip=skip, limit=page_size, projection={
                'boundedItems': False,
                'predictTime': False,
            })

        if execute:
            results = list(results)

        return count, results

    @property
    def column_formatters(self):
        formatters = self._delegate_to_sub('column_formatters')
        if formatters is not None:
            return formatters

        return self._column_formatters

    @column_formatters.setter
    def column_formatters(self, val):
        pass

    @property
    def can_edit_status(self):
        perm = ActionNeedPermission(self._action_name, EditBoundStatus)
        return perm.can()

    @property
    def can_remove_status(self):
        perm = ActionNeedPermission(self._action_name, RemoveBoundStatus)
        return perm.can()

    @expose('/mx-bounded-status/', methods=['POST', 'GET'])
    def get_bounded_status(self):
        # TODO: 如果是POST则需要执行更新操作
        if request.method == 'GET':
            resp = self._api_proxy.get(
                '/v1/mxp-binding/details?id=%s&mxtype=%s' % (
                    request.args.get('id'), request.args.get('mxtype')))
        else:
            model = request.get_json(force=True)
            resp = self._api_proxy.update(
                model, None,
                '/v1/mxp-binding/update?batch=1')

        if resp.status_code == 200:
            return jsonify(code=200, data=resp.json())

        return jsonify(code=resp.status_code, message=resp.json()['message'])

    @expose('/mx-duplicate/', methods=['GET'])
    def get_duplicate(self):
        resp = self._api_proxy.create({
                'mxId': request.args.get('mxId'),
                'mxType': request.args.get('mxType'),
                'planeId': request.args.get('planeId'),
            },
            '/v1/mxp-binding/duplicate')

        if resp.status_code == 200:
            return jsonify(code=200, data=resp.json())

        return jsonify(code=resp.status_code, message=resp.json()['message'])

    @expose('/get-subsidiary-work/')
    def get_subsidiary_work(self):

        # if not self.can_routine_work:
        #     return jsonify(code=403, message='You are not allowed to do so.')

        plane_id = request.args.get('plane', '')
        mx_id = request.args.get('mxid', '')

        if not plane_id or not mx_id:
            return jsonify(code=400, message='You should provide plane and mx id.')

        ret = get_subsidiary_materials_related_available_work(plane_id, mx_id)
        if ret is None:
            return jsonify(code=404, message='Nothing of the related work.')

        return jsonify(code=200, **ret)

    # 下面内容为打印相关实现
    @expose('/export/<export_type>/')
    def export(self, export_type):
        mx_type = request.args.get('mxtype', 'scheduled')
        self._export_columns = self.get_export_columns(mx_type)
        return_url = get_redirect_target() or self.get_url('.index_view')

        if export_type == 'csv':
            return self._export_csv(return_url)
        else:
            return self._export_tablib(export_type, return_url)

    def get_export_columns(self, mx_type=None):
        # 定检打印字段

        col = [
            ('mxId', '维修方案编号'),
            ('description', '描述信息'),
            ('leftHour', '剩余小时'),
            ('leftTimes', '剩余次数'),
            ('leftDay', '剩余天'),
            ('leftEngineTime', '剩余发动机时间'),
            # ('best', '预计检查日期'),
            # ('warningLevel', '预警等级'),
            # ('error', '错误提示'),
            # ('completeDate', '上次完成时间')
        ]
        if mx_type != 'scheduled':
            # 时空/时寿
            col = [
                # ('mxId', '维修方案编号'),
                # ('description', '描述信息'),
                ('pn', '件号'),
                ('serialNumber', '序号'),
                ('name', '名称'),
                ('completeDate', '装机日期'),
                ('leftHour', '剩余小时'),
                ('leftTimes', '剩余次数'),
                ('leftDay', '剩余天'),
                ('leftEngineTime', '剩余发动机时间'),
                ('best', '预计检查日期'),
                # ('warningLevel', '预警等级'),
                # ('error', '错误提示'),
            ]

        return col

    def get_export_value(self, model, name):

        if name in model:
            return model[name]
        return ''

    def _export_data(self):
        # 导出数据

        export_page = request.args.get('export_page', 0, type=int)
        export_size = request.args.get('export_size', 0, type=int)
        search = request.args.get('search', '')
        air_id = request.args.get('id', '')
        mx_type = request.args.get('mxtype', 'scheduled')
        view_args = self._get_list_extra_args()
        due_list = DuelistLogic(self)

        count, export_data = due_list.get_list(export_page,
                                               None,
                                               view_args.sort_desc,
                                               search,
                                               view_args.filters,
                                               page_size=export_size)

        export_data = self.get_export_data(export_data, air_id, mx_type)

        return count, export_data

    def get_bangding(self):
        # 绑定相关信息
        com = {}
        air = self.coll.find(
            {"_id": bson.ObjectId(request.args.get('id'))})
        if not air.count():
            return com
        bounds = air[0]['boundedItems']
        for item in bounds:
            if item['refId'].collection not in \
                    ['time_control_unit_y5b', 'life_control_unit_y5b']:
                continue
            com[item['boundedId']] = [
                self.unix_to_string(
                    item['completeDate']), item['serialNumber']]
        return com

    def get_export_data(self, data, id, mx_type):
        mxp = self.get_mx_name(mx_type)
        export_datas = []

        for item in data:

            export_data = {
                'mxId': mxp[item['predictTime']['mxRefId'].id][0],
                'description': mxp[item['predictTime']['mxRefId'].id][1],
                'warningLevel': item['level'],
                'error': item['predictTime']['err'],
                'best': self.unix_to_string(item['predictTime']['earliest']),
                'leftHour': item['intervaltype'][0] if 0 in item['intervaltype'].keys() else '',
                'leftTimes': item['intervaltype'][1] if 1 in item['intervaltype'].keys() else '',
                'leftDay': item['intervaltype'][2] if 2 in item['intervaltype'].keys() else '',
                'leftEngineTime': item['intervaltype'][9] if 9 in item['intervaltype'].keys() else '',
            }
            if export_data['leftHour']:
                export_data['leftHour'] = convert_float_to_hh_mm(export_data['leftHour'])
            if export_data['leftEngineTime']:
                export_data['leftEngineTime'] = convert_float_to_hh_mm(export_data['leftEngineTime'])
            if mx_type != 'scheduled':
                com = self.get_bangding()
                export_data["completeDate"] = com[item['predictTime']['itemId']][0]
                export_data["serialNumber"] = com[item['predictTime']['itemId']][1]
                export_data['pn'] = mxp[item['predictTime']['mxRefId'].id][2]
                export_data['name'] = mxp[item['predictTime']['mxRefId'].id][3]

            export_datas.append(export_data)
        return export_datas

    def unix_to_string(self, data):
        # unix 时间戳格式化
        if not data:
            return ''
        data = datetime.datetime.fromtimestamp(data)
        return data.strftime("%y-%m-%d")

    def get_mx_name(self, mx_type):
        # 获取维修方案相关信息
        if mx_type != 'scheduled':
            coll = 'time_control_unit_y5b' if mx_type == 'timecontrol' else 'life_control_unit_y5b'
            datas = list(self._mongo[coll].find(
                {}, {"id": 1, "description": 1, "pn": 1, "name": 1}))
            data = {}
            for item in datas:
                data[item['_id']] = [
                    item['id'], item['description'], item['pn'], item['name']]
            return data
        datas = list(self._mongo['scheduled_mx_check_y5b'].find(
            {}, {"id": 1, "description": 1}))
        data = {}
        for item in datas:
            data[item['_id']] = [item['id'], item['description']]
        return data

    # 下面的内容为通用的飞机实例与飞行日志实例同处于相同页面的实现
    # 如果日志需要分开实现，无需提供下面的操作
    @property
    def can_create_flightlog(self):
        return ActionNeedPermission('flightlog', Create).can()

    @property
    def can_edit_flightlog(self):
        return ActionNeedPermission('flightlog', Edit).can()

    @property
    def can_delete_flightlog(self):
        return ActionNeedPermission('flightlog', Delete).can()

    @property
    def can_view_details_flightlog(self):
        return ActionNeedPermission('flightlog', View).can()

    @property
    def can_routine_work(self):
        perm = ActionNeedPermission(
            'routinework', 'create')
        return perm.can()


class AircraftDetailsRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(AircraftDetailsRowAction, self).__init__(
            'custom_op.aircraft_details_row', '查看')


class AircraftEditRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(AircraftEditRowAction, self).__init__(
            'custom_op.aircraft_edit_row', '编辑')


class AircraftDelRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(AircraftDelRowAction, self).__init__(
            'custom_op.aircraft_delete_row', '删除')


_buttons_map = {
    'aircraft_details': AircraftDetailsRowAction(),
    'aircraft_edit': AircraftEditRowAction(),
    'aircraft_delete': AircraftDelRowAction(),
}
