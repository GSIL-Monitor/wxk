# coding: utf-8

from __future__ import unicode_literals
import json
from collections import namedtuple
import datetime
import threading
import Queue
import time

from flask_admin.form import FormOpts
from flask import request, redirect, render_template, jsonify, flash
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.babel import gettext
from flask_admin.model.helpers import get_mdict_item_or_list

from modules.views.mongo_custom_view import MongoCustomView
from modules.proxy import proxy
from modules.views.operations import normal_modal_operation_formatter
from util.jinja_filter import timestamp_to_date
from util.exception import BackendServiceError
from .formatter import interval_formmatter


def get_allowed_models():
    "获取为当前用户授权的维修方案（机型）列表"

    resp = proxy.get('/v1/support-plane-types/')
    if resp.status_code != 200:
        return []

    supported = resp.json()['items']

    AircraftModel = namedtuple('AircraftModel', ['label', 'value'])
    return [AircraftModel(label=value, value=key) for key, value in supported.items()]


class MxpBaseView(MongoCustomView):

    list_template = 'mxp/list.html'
    create_modal_template = 'mxp/create_twoline.html'
    edit_modal_template = 'mxp/edit_twoline.html'
    details_modal_template = 'mxp/details.html'

    column_display_actions = False

    extra_css = [
        '/static/css/profile.css',
    ]

    column_list = None

    create_modal = edit_modal = details_modal = True

    column_formatters = dict(interval=interval_formmatter)

    column_searchable_list = (
        'id', 'source', 'ataCode', 'name',
        'reference', 'adapt', 'pn', 'description')

    # 具体的机型方案应该提供下面的内容
    @property
    def maintain_list(self):
        """具体机型的维修方案应该提供相应子方案实例的列表。"""
        return {}

    def __init__(self, db, endpoint, *args, **kwargs):

        self._mongo = db
        self.column_formatters = self.column_formatters or {}
        self.column_formatters.update({
            'operation': normal_modal_operation_formatter,
        })

        self.extra_js = self.extra_js or []
        self.extra_js.extend(['/static/js/jquery.validate.min.js'])

        super(MxpBaseView, self).__init__(
            db, None, 'mxp', endpoint='%s-view' % endpoint, *args, **kwargs)

    @expose('/download/', methods=('GET',))
    def download_view(self):
        key = request.args.get('key')
        post = {"key": key}
        url = "/v1/file-access/download"
        resp = self._api_proxy.create(post, url)
        acc_url = resp.json().get('url')
        return redirect(acc_url, 301)

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
        doc_type = [t_item.get('id') for t_item in
                    type_resp.json().get('items')]

        if not files_resp.json().get('total'):
            for type_item in doc_type:
                doc_files[type_item] = None
            return render_template('mxp/relate_doc.html', doc_type=doc_type,
                                   doc_files=doc_files)

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

    def get_save_return_url(self, model, is_created=False):
        sub = request.args.get('sub')
        return self.get_url('.index_view', sub=sub)

    def _search(self, query, search_term):
        coll_name = self._delegate_to_sub('coll_name')
        self.coll = self._mongo[coll_name]
        return super(MxpBaseView, self)._search(query, search_term)

    @expose('/')
    def index_view(self):
        _api_url = '/v1/mxp/'
        resp = self._api_proxy.get(_api_url)
        if resp.status_code != 200:
            raise BackendServiceError('Please contact the service maintainer.')

        # TODO: 根据用户授权的方案模型，全部显示
        for item in resp.json().get('items'):
            if item.get('mxpName') == 'y5b':
                model_name = item.get('modelName')
                onlineTime = item.get('onlineTime')
                offlineTime = item.get('offlineTime')
                boundedCount = item.get('boundedCount')
                typeManufacturer = item.get('typeManufacturer')
        self._template_args.update({
            'modelName': model_name,
            'onlineTime': timestamp_to_date(onlineTime),
            'offlineTime': timestamp_to_date(offlineTime),
            'boundedCount': boundedCount,
            'typeManufacturer': typeManufacturer,
            'not_on_top_search': True,
        })
        return super(MxpBaseView, self).index_view()

    @expose('/unique_value/')
    def unique_value(self):
        try:
            field = request.args.get('field', None)
            value = request.args.get('value', None)
            if field and value:
                if not self.coll.find_one({field: value}):
                    return jsonify(code=200, message='Ok')

            return jsonify(code=409, message='Already Exist')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/details/')
    def details_view(self):
        sub = request.args.get('sub', self.default_subordinate_view)
        self._template_args.update({
            'sub': sub,
            'time_formatter': datetime.time,
        })
        self._edit_form_class = self._delegate_to_sub('form')
        self.override_fields(self._edit_form_class)

        return_url = get_redirect_target() or self.get_url('.index_view')

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        form = self.edit_form(obj=model)

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        return self.render(self.details_modal_template,
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)

    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        self.two_line_init()
        return super(MxpBaseView, self).create_view()

    @expose('/edit/', methods=['GET', 'POST'])
    def edit_view(self):
        self.two_line_init()
        self.edit_modal_template = MxpBaseView.edit_modal_template
        return super(MxpBaseView, self).edit_view()

    def scaffold_list_columns(self):
        ret = super(MxpBaseView, self).scaffold_list_columns()
        ret.append('operation')
        return ret

    def override_fields(self, class_name):
        if class_name.__name__ in ['TimeControlUnitForm', 'LifeControlUnitForm']:
            pns = self.coll.find({}, {'_id': 0, 'pn': 1})
            choice = [(pn.get('pn'), pn.get('pn')) for pn in pns]
            choice.insert(0, ('', ''))
            class_name.unitNo.kwargs.update({'choices': choice})

    def two_line_init(self):
        twolines = -1
        self._create_form_class = self._delegate_to_sub('form')
        for index, key in enumerate(self._create_form_class()._fields):
            if key == 'description':
                twolines = index + 1
        self._template_args.update({
            'twolines': twolines
        })


def get_api_response(queue, api_proxy, url, name):
    resp = api_proxy.get(url)
    queue.put({name: resp})
