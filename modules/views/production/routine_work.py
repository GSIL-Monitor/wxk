# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import date_converter
import time
from datetime import date, datetime
import threading
import Queue
import json

from wtforms import HiddenField, SelectField
from wtforms.validators import DataRequired
from flask import redirect, request, abort, jsonify, flash, render_template
from flask_admin import expose
from flask import current_app
from flask_admin.babel import gettext
from flask_admin.model.template import TemplateLinkRowAction

from modules.proxy import proxy
from modules.models.production.routine_work import RoutineWork
from modules.views import CustomView, ActionViewCfg
from modules.flows import BasicFlow
from modules.flows.operations import Finish
from modules.helper import get_mx_item_info
from modules.views.mxp.base import get_allowed_models
from modules.views.helper import timestamp_to_date_formater, serial_number_formatter
from modules.views.select_plantype import PlaneTypeSelectableMixin
from modules.helper import get_allowed_aircrafts, get_aircraft_related_bounded_status
from modules.views.operations import custom_operation_formatter
from modules.forms.action import RoutineWorkFinishForm
from ..column_formatter import accessory_formatter, relate_doc_formatter
from util.widgets import DateIntWidget
from util.fields import DateInt
from util.fields.select import WithTypeSelectField
from util.fields.accessory_filed import RoutineWorkFileuploadField
from util.fields.relate_doc_field import RoutineWorkRelateDocField
from modules.models.project_tech.retain import Retain
from util.fields.select import choiceRealNameSelectField


class FinishAction(TemplateLinkRowAction):
    def __init__(self):
        super(FinishAction, self).__init__(
            'custom_op.routine_work_finish', '完成')


class _RoutineWorkView(CustomView, PlaneTypeSelectableMixin):
    """例行工作记录"""
    create_template = 'routinework/create.html'
    approve_edit_template = 'routinework/approve_edit.html'
    details_template = 'oldDetails.html'
    action_view_template = 'routinework/action_view.html'


    extra_js = [
        '/static/js/jquery.validate.min.js',
        '/static/js/additional-methods.min.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/jquery.uniform.min.js',
        '/static/js/jquery-ui.min.js',
        '/static/js/jquery-migrate.min.js',
        '/static/js/bootstrap-hover-dropdown.min.js',
        '/static/js/jquery.slimscroll.min.js',
        '/static/js/jquery.cokie.min.js',
        '/static/js/custom_action.js',
        '/static/js/bluebird.js',
        # select2
        '/static/js/bootstrap-select.min.js',
        '/static/js/jquery.multi-select.js',
        '/static/js/components-dropdowns.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/routine_work_validation.js',
    ]

    extra_css = [
        '/static/css/routine_work.fonts',
        '/static/css/uniform.default.css',
        '/static/css/bootstrap-switch.min.css',
        '/static/css/select2.css',
    ]

    # 指示不使用通用的groupOperation格式化方式
    use_inheritance_operation = False

    # 例行工作列表视图应显示的内容
    column_list = [
        'jihao', 'jcType', 'mxId',
        'jcTime', 'jcAdress', 'statusName',
        # 因为使用自己的操作格式化，所以这里需要额外定义
        'operation',
    ]

    column_details_list = [
        'lxgzNum', 'jihao', 'jcType', 'mxId', 'aircraftPn', 'serialNumber',
        'description', 'contextDesc', 'jcTime', 'jcAdress', 'statusName',
        'planeType', 'boundedid', 'user', 'relateDocFiles', 'fileUrlaccessory',
    ]

    # 对应内容的中文翻译
    column_labels = {
        'jihao': '飞机注册号',
        'jcType': '检查类型',
        'aircraftPn': '型号',
        'serialNumber': '序号',
        'contextDesc': '检查内容',
        'description': '维修方案描述',
        'jcTime': '检查时间',
        'jcAdress': '检查地点',
        'statusName': '状态',
        'lxgzNum': '单据编号',
        'user': '涉及人员',
        'cancel': '返回',
        'mxId': '维修方案编号',
        # 同样，还需要额外的翻译
        'operation': '操作',
        'planeType': '机型',
        'relateDoc': '相关文档',
        'relateDocFiles': '相关文档',
        'fileUrl': '附件',
        'fileUrlaccessory': '附件',
    }

    # 这里展示了如何在子视图里定制自己的操作按钮
    # 该完成按钮是否存在，取决于模型实例的检查日期是否设置
    finish_btn = lambda s, m: FinishAction() if m.jcTime else None

    form_excluded_columns = [
        'approveSuggestions', 'approveTime',
        'approveUserName', 'reviewSuggestions',
        'reviewTime', 'reviewUserName',
        'insNum', 'yuliuCon', 'retain'
    ]

    support_flow = partial(BasicFlow, 'Finish flow')

    form_widget_args = {
        'lxgzNum': {
            'readonly': True
        },
        'mxId': {
            'readonly': True,
        },
        'description': {
            'readonly': True,
        },
        'jcType': {
            'readonly': True,
        },
        'aircraftPn': {
            'readonly': True,
        },
        'serialNumber': {
            'readonly': True,
        }
    }

    one_line_columns = ['boundedid', 'fileUrl', 'relateDoc']

    column_searchable_list = [
        'planeType', 'jihao', 'jcType', 'jcTime', 'jcAdress', 'mxId']

    form_overrides = {
        'jcTime': partial(DateInt, widget=DateIntWidget()),
        'boundedid': HiddenField,
        'user': partial(choiceRealNameSelectField),
        'fileUrl': partial(RoutineWorkFileuploadField),
        'relateDoc': partial(RoutineWorkRelateDocField),
        # 'serialNumber': HiddenField,
    }

    column_formatters = {
        # 以及非默认的操作格式化方式，虽然使用的也是“通用的”格式化实现
        # 但该实现允许视图自己定义使用的操作按钮
        'operation': custom_operation_formatter,
        'jcTime': timestamp_to_date_formater,
        'serialNumber': serial_number_formatter,
        'fileUrlaccessory': accessory_formatter('fileUrl'),
        'relateDocFiles': relate_doc_formatter('relateDoc'),
    }

    def create_form(self, obj=None):
        self.select_override('_create_form_class')

        retain_id = request.args.get('id', '')
        if retain_id:
            inst = Retain.query.filter(Retain.id == retain_id).first()
            return self.create_form_with_default(inst)

        return super(_RoutineWorkView, self).create_form(obj)

    def edit_form(self, obj=None):
        form = self.select_override('_edit_form_class')

        if obj is not None:
            aircraft_id = obj.jihao
            bounded_status = get_aircraft_related_bounded_status(aircraft_id)
            if bounded_status:
                form.jcType = SelectField('检查类型', choices=[
                    (item, item) for item in bounded_status.keys()
                ])
                if request.method == 'POST':
                    obj.jcType = request.form['jcType']

                if obj.jcType:
                    allowed_mxpid = set()

                    for x in bounded_status:
                        if x == obj.jcType:
                            for item in bounded_status[obj.jcType]:
                                allowed_mxpid.add(item.mxpId)

                    form.mxId = SelectField(
                        '维修方案编号',
                        choices=[(item, item) for item in allowed_mxpid])
                    # 序号变成列表
                    mxp_id = obj.mxId
                    if mxp_id and obj.serialNumber:
                        # 已经存在对应的维修方案的话，需要判断是否有多个序号
                        items_with_type = bounded_status[obj.jcType]
                        # choices = []
                        # for item in items_with_type:
                        #     # 同一个编号的所有序号聚合到一起
                        #     if item.mxpId == mxp_id:
                        #         choices.append(((item.sn, item.id), item.sn))
                        # form.serialNumber = WithTypeSelectField(
                        #     '序号', choices=choices)

            # TODO: 其他需要变更为choices的内容

        return super(_RoutineWorkView, self).edit_form(obj)

    @expose('/batch-generate', methods=['POST'])
    def batch_create_view(self):
        plane_id = request.args.get('planeid', '')
        plane_type = request.args.get('planetype', '')
        bounded_ids = request.args.getlist('boundedid', None)

        # TODO: 这里没有检验用户是否拥有创建该实例的权限

        form = self._create_form_class()
        form.planeType.data = plane_type
        form.jihao.data = plane_id

        if not plane_id or not plane_type or not bounded_ids:
            return abort(400)
        mxIds = []
        for bounded_id in bounded_ids:
            # 查找对应的方案内容
            info = get_mx_item_info(plane_id, plane_type, bounded_id)
            if info is None:
                continue

            item = current_app.mongodb['aircraft_information'].find_one(
                {'boundedItems.boundedId': bounded_id},
                {'boundedItems.$': True}
            )

            if item is None:
                return ''
            mxIds.append(info.obj['id'])
        mxIds = set(mxIds)

        for mxId in mxIds:
            bounds = []
            serialNumbers = []
            for bounded_id in bounded_ids:
                # 查找对应的方案内容
                info = get_mx_item_info(plane_id, plane_type, bounded_id)
                if info is None:
                    continue

                item = current_app.mongodb['aircraft_information'].find_one(
                    {'boundedItems.boundedId': bounded_id},
                    {'boundedItems.$': True}
                )

                if item is None:
                    return ''

                bounds.append(bounded_id)
                if info.mx_type == 'timecontrol' or info.mx_type == 'lifecontrol':
                    if info.obj['id'] == mxId:
                        serialNumbers.append(item['boundedItems'][0]['serialNumber'])

            info = get_mx_item_info(plane_id, plane_type, bounds[0])
            bounds = ','.join(bounds)
            serialNumbers = ','.join(serialNumbers)
            form.description.data = info.description
            form.mxId.data = info.obj['id']
            form.jcType.data = info.mx_type_name
            form.boundedid.data = bounds

            if info.mx_type == 'timecontrol' or info.mx_type == 'lifecontrol':
                form.aircraftPn.data = info.obj['pn'] or ''
                form.serialNumber.data = serialNumbers or ''

            model = self.model()
            form.populate_obj(model)

            self.session.add(model)
            self._on_model_change(form, model, True)

        try:
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext(
                    'Failed to create record. %(error)s',
                    error=unicode(ex)), 'error')

            self.session.rollback()

        # 自动创建
        return redirect(self.get_url('.index_view'))

    @expose('/get-info/', methods=['GET'])
    def get_aircraft_info(self):
        aircraft_id = get_allowed_aircrafts(bounded=True)
        aircraft_type = get_allowed_models()
        return jsonify(
            code=200, data={'id': aircraft_id, 'type': aircraft_type})

    @expose('/get-bounded-status/', methods=['GET'])
    def get_bounded_status(self):
        planeId = request.args.get('planeId')
        status = get_aircraft_related_bounded_status(planeId)
        return jsonify(code=200, data=status)

    def __init__(self, *args, **kwargs):

        self.extra_js = getattr(self, 'extra_js', [])
        self.extra_js.extend([
            '/static/js/bootstrap-datetimepicker.min.js',
            '/static/js/datetimepicker.zh-cn.js',
            '/static/js/select_planeType.js',
            '/static/js/routineWork.js',
            '/static/js/upload_file.js',
        ])

        self.extra_css = getattr(self, 'extra_css', [])
        self.extra_css.extend([
            '/static/css/datepicker.css',
            '/static/css/bootstrap-datetimepicker.min.css',
        ])

        # 除了通用的自定义操作外，我们需要自己的设置
        self._action_view_cfg = self._action_view_cfg or {}
        self._action_view_cfg.update({
            'finish': ActionViewCfg('完成', 'fa-check', RoutineWorkFinishForm, ('完成', Finish), None)
        })

        self._api_proxy = proxy

        super(_RoutineWorkView, self).__init__(*args, **kwargs)

    def _before_custom_action(self, model, action, **kwargs):
        if action == Finish:
            # 执行远端请求

            # WUJG: 确保model.jcTime的值为时间戳字符串
            timestamp = int(model.jcTime)
            bounded_id = model.boundedid

            if model.jcType == '航线检查' or model.jcType == '停放检查':
                return;

            if int(time.mktime(datetime.today().timetuple())) < timestamp:
                raise ValueError('完成时间为何大于今天?')

            if model.contextDesc is None:
                raise ValueError('请输入“检查内容”')

            if ',' in bounded_id:
                bounded_id = bounded_id.split(",")
                data = [{'boundedId': x, 'finishTime': int(timestamp), 'remark': ''} for x in bounded_id]
            elif bounded_id:
                data = [{'boundedId': bounded_id, 'finishTime': int(timestamp), 'remark': ''}]
            else:
                raise ValueError('数据有误，请联系管理员?')

            proxy.create(data, '/v1/mxm/accomplish?batch=1')

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.jcTime.validators = [DataRequired()]
            form.contextDesc.validators = [DataRequired()]

        return super(_RoutineWorkView, self).validate_form(form)

    def on_model_change(self, form, model, is_created):
        super(_RoutineWorkView, self).on_model_change(form, model, is_created)
        retain_id = request.args.get('id', '')
        if is_created and retain_id:
            model.retain_id = retain_id

    @expose('/relate-doc/', methods=('GET', 'POST'))
    def relate_doc_view(self):
        doc_files = {}
        type_url = '/v1/doc-type/'
        files_url = '/v1/file-access/stat'
        result = {}
        q = Queue.Queue()
        t1 = threading.Thread(target=get_api_response,
                              args=(q, self._api_proxy, type_url, 'type'))
        t2 = threading.Thread(target=get_api_response,
                              args=(q, self._api_proxy, files_url, 'files'))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        while not q.empty():
            result.update(q.get())

        type_resp = result.get('type')
        files_resp = result.get('files')

        if not type_resp or not files_resp or\
                type_resp.status_code != 200 or files_resp.status_code != 200:
            raise Exception('Please contact the service maintainer.')

        doc_type = [t_item.get('id')
                    for t_item in type_resp.json().get('items')]

        if not files_resp.json().get('total'):
            for type_item in doc_type:
                doc_files[type_item] = None
            return render_template('mxp/relate_doc.html',
                                   doc_type=doc_type, doc_files=doc_files)

        for files_item in files_resp.json().get('items'):
            file_type = files_item.get('type')
            if file_type in doc_type:
                files_item.pop('mimeType')
                if file_type not in doc_files:
                    doc_files.update({file_type: [{'name': files_item.get('name'),
                                                   'value': json.dumps(files_item)}]})
                else:
                    doc_files.get(file_type).append({'name': files_item.get('name'),
                                                     'value': json.dumps(files_item)})

        return render_template('mxp/relate_doc.html', doc_type=doc_type, doc_files=doc_files)


def get_api_response(queue, api_proxy, url, name):
    resp = api_proxy.get(url)
    queue.put({name: resp})


RoutineWorkView = partial(
    _RoutineWorkView, RoutineWork, name='例行工作记录'
)
