# coding: utf-8

from __future__ import unicode_literals
import logging
from functools import partial
from collections import namedtuple
import copy

from flask import url_for, redirect, request, abort, flash
from flask_security import current_user
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.contrib.sqla import ModelView as SQLModelView
from flask_admin.form import FormOpts
from flask_admin.babel import gettext
from sqlalchemy import or_
from sqlalchemy_continuum import version_class
from flask_weasyprint import HTML, render_pdf

from modules.proxy import proxy
from modules.forms.action import (ReviewForm, ApproveForm, ReviewOnlyForm,
                                  SecondApproveForm, UserSelectForm,
                                  ContractFileForm, MeetingFileForm)
from modules.views.column_formatter import cancel_formatter, plane_type_formatter
from ..perms import ActionNeedPermission
from ..flows.operations import (Create, Edit, Delete, View, Finish,
                                ReviewApprove, ReviewRefuse,
                                Approved, ApproveRefuse,
                                SubmitReview, ReviewAgain,
                                Receive, SubmitReview, ReviewAgain, Sent,
                                ReserveAgain, SecondApproved,
                                SecondApproveRefuse, PutInStore, Stored,
                                UploadContractFile, UploadMeetingFile)
from ..flows import *
from .mixin import Mixin
from modules.models.user import User
from util.jinja_filter import timestamp_to_date
from modules.models.role import Role, BasicAction
from .flow_column_labels import flow_column_labels
from .flow_column_formatters import flow_column_formatters
from modules.flows.states import ReviewedFailure, ApprovedFailure, Received
from flask_admin.helpers import get_form_data, is_form_submitted


log = logging.getLogger("flask-admin.pymongo")


ActionViewCfg = namedtuple(
    'ActionViewCfg',
    ['action_name', 'icon_value', 'form', 'agreed', 'refuse'])


flow_map = {
    'one_approve': [OneApprovalFlow, ADFlow, ApproveCanEdit, FaultReportsFlow,
                    TroubleShootingFlow, RetainFlow, EOFlow, BorrowInReturnFlow,
                    LoanInReturnFlow, ScrapFlow],
    'basic': [BasicFlow, StorageFlow, PutOutStoreFlow],
    'two_approve': [TwoApprovalFlow,
                    PurchaseRequestFlow, ScrapFlow,
                    BorrowRequestFlow, LoanApplicationFlow],
}


class CustomView(Mixin, SQLModelView):

    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'
    details_template = 'details.html'
    approve_edit_template = 'approve_edit.html'
    action_view_template = 'action_view.html'

    pdf_css = 'assets/static/css/pdf.css'
    pdf_template = 'pdf.html'

    export_types = ['csv', 'xlsx']

    # 所有基于sql的模型，使用id字段来默认倒序排序
    column_default_sort = ('id', True)

    # 顶部搜索控件是否显示
    top_search_form = False
    # 机型默认值
    plane_type = 'Y5D(B)'

    # 用于判断是否需要保存并添加另一个和保存并继续编辑按钮
    can_extra = True

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/bootstrap-select.min.js',
        '/static/js/jquery.multi-select.js',
        '/static/js/components-dropdowns.js',
        '/static/js/select_planeType.js',
    ]

    extra_css = [
        '/static/css/datepicker.css',
        '/static/css/dateHeight.css',
        '/static/css/bootstrap-datetimepicker.min.css',
    ]

    column_display_actions = False

    support_popup = True
    form_excluded_columns = []

    review_details_columns = []

    # 需要单行显示的字段
    one_line_columns = []

    # 是否支持打印PDF格式
    can_export_pdf = False

    use_inheritance_operation = True
    """如果想变更通用的操作格式化行为，请将该参数设置为False"""

    support_flow = partial(OneApprovalFlow, 'Default basic approval flow')

    """该视图后台允许的工作流实例，默认为基本的`一次性审批工作流`。


    一个callable实例，仅有的一个参数为当前拥有状态的模型实例。
    """

    # 支持流程操作的视图相关配置
    # 主键需要与templates/operations.html里的各操作的verb相对应
    sent_form = partial(UserSelectForm, '允许的接收人员', Receive)
    contract_form = partial(ContractFileForm, '合同文件')
    meeting_form = partial(MeetingFileForm, '会议纪要')

    _action_view_cfg = {
        'review': ActionViewCfg('复核', 'fa-tag', ReviewForm, ('复核通过', ReviewApprove), ('复核拒绝', ReviewRefuse)),
        'approve': ActionViewCfg('审批', 'fa-tags', ApproveForm, ('审批通过', Approved), ('审批拒绝', ApproveRefuse)),
        'sec-approve': ActionViewCfg('审批', 'fa-tags', SecondApproveForm, ('审批通过', Approved), ('审批拒绝', ApproveRefuse)),
        'second_approved': ActionViewCfg('二级审批', 'fa-tags', ApproveForm, ('审批通过', SecondApproved), ('审批拒绝', SecondApproveRefuse)),
        'submit_review': ActionViewCfg('提交复核', 'fa-bell-o', UserSelectForm, ('确认', SubmitReview), None),
        'edit': ActionViewCfg('', 'fa-bell-o', None, ('保存', Edit), None),
        'review_again': ActionViewCfg('再次复核', 'fa-level-up', UserSelectForm, ('确认', ReviewAgain), None),
        'sent': ActionViewCfg('下发', 'fa-bell-o', sent_form, ('确认', Sent), None),
        'reserve_again': ActionViewCfg('', 'fa-reorder (alias)', None, ('保存', ReserveAgain), None),
        'upload_contract_file': ActionViewCfg('', 'fa-bell-o', contract_form, ('上传', UploadContractFile), None),
        'upload_meeting_file': ActionViewCfg('', 'fa-bell-o', meeting_form, ('上传', UploadMeetingFile), None),
        'review_only': ActionViewCfg('复核', 'fa-tag', ReviewOnlyForm, ('复核通过', ReviewApprove), ('复核拒绝', ReviewRefuse)),
    }

    # 下面的权限使得采用配置的方式决定哪些视图可以被用户看见
    def __init__(self, *args, **kwargs):
        """ 初始化CustomView的自定义实例"""

        if not self.column_list:
            self.column_list = []

        self.column_list = list(self.column_list)

        self.column_labels = self.column_labels or {}

        if not self.column_formatters:
            self.column_formatters = dict()
        self.column_formatters.update({
            'planeType': plane_type_formatter,
        })
        self.column_details_list = self.column_details_list or []

        self.review_details_columns = copy.deepcopy(self.column_details_list)


        # 如果使用通用的行为，则将操作统一组操作格式化方式
        # RoutineWorkView展示了如何实现特殊的操作定义
        if self.support_flow:

            self.column_labels.update(flow_column_labels)

            self.column_formatters.update(flow_column_formatters)

            # self.review_details_columns = copy.deepcopy(self.column_details_list)

            self.column_details_list.extend(self.support_flow.func.get_flow_columns())

            if self.use_inheritance_operation:
                if 'operation' in self.column_list:
                    self.column_list.remove('operation')

                self.column_list.append('groupOperation')
        # WUJG: 这里无需检查查看权限，即使不存在权限，这里的显示内容也无关紧要
        # 确保返回按钮在最后

        self.column_labels.update({
            'operation': '操作',
            'return': '返回'
        })

        if 'return' not in self.column_details_list:
            self.column_details_list.append('return')

        self.column_formatters.update({
            'return': cancel_formatter,
        })

        if not self.form_excluded_columns:
            self.form_excluded_columns = []

        self.form_excluded_columns = list(self.form_excluded_columns)

        # 默认的窗体不应该包含下面内容
        self.form_excluded_columns.extend(
            ['createTime', 'updateTime', 'statusName', 'audits',
             'allowedUser', 'relatedUser', 'auditStatus', 'timestamp',
             'suggestion', 'versions'])

        super(CustomView, self).__init__(*args, **kwargs)

    # 这里把update_model从写主要是因为这里抓取的异常不支持汉语，改写后可以支持
    def update_model(self, form, model):
        """
            Update model from form.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        try:
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to update record. %(error)s', error=unicode(ex)), 'error')
                log.exception('Failed to update record.')
                # flash('无法执行指定的操作。 %s' % (unicode(ex),), category='error')
            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True

    # 这里把create_model从写主要是因为这里抓取的异常不支持汉语，改写后可以支持
    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            model = self.model()
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=unicode(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                return abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

    def date_formatter_date(self, view, ctx, model, name):
        dict = {}
        dict.update(model.__dict__)
        if dict[name] is not None:
            if type(dict[name]) is unicode:
                try:
                    value = float(dict[name])
                    return timestamp_to_date(value)
                except:
                    return dict[name]

    def get_details_columns(self):
        only_columns = (self.column_details_list or
                        self.scaffold_list_columns())

        return self.get_column_names(
            only_columns=only_columns,
            excluded_columns=self.column_details_exclude_list,
        )

    def on_model_change(self, form, model, is_created):
        flow = self.support_flow
        if is_created and flow:
            if not flow.keywords or 'support_create' not in flow.keywords or\
                    flow.keywords['support_create']:
                self._custom_action(model, form.data, Create, False)

        super(CustomView, self).on_model_change(form, model, is_created)

    def get_query(self):

        datas = self.model.query
        if not self.support_flow or \
                self.support_flow.func not in flow_map['one_approve']:
            return datas

        version = version_class(self.model)

        ids = []
        for item in datas:
            query = version.query.filter(
                version.id == item.id, version.auditStatus == InitialState)
            if not query:
                continue
            transaction_id = query[-1].transaction_id

            status = [ReviewedFailure, ApprovedFailure]
            fail_query = version.query.filter(
                version.id == item.id, version.auditStatus.in_(status))
            if fail_query.count():
                if query[-1].relatedUser_id != current_user.id:
                    tmp = version.query.filter(
                        version.id == item.id,
                        version.transaction_id > fail_query[-1].transaction_id)
                    transaction_id = tmp[0].transaction_id if tmp.count() else transaction_id

            inst = version.query.filter(
                or_(version.relatedUser_id == current_user.id,
                    version.allowedUser_id == current_user.id),
                version.id == item.id,
                version.transaction_id >= transaction_id).first()

            if inst:
                ids.append(inst.id)

        return self.model.query.filter(self.model.id.in_(ids))

    def get_recieved_query(self, datas, model_name):

        ids = [item.id for item in datas] if datas.count() else []

        role = Role.query.join(
            BasicAction, Role.id == BasicAction.role_id
        ).filter(BasicAction.receive == True,
                 BasicAction.model == model_name)

        if role.count() != 1 or role[0] not in current_user.roles:
            return datas

        query = self.model.query.filter(
            or_(self.model.id.in_(ids),
                self.model.auditStatus == Received))

        return query

    @property
    def _details_columns(self):
        return self.get_details_columns()

    @property
    def can_create(self):
        # 使用属性的方式来重写框架原自带的can_create实现
        perm = ActionNeedPermission(self.action_name, Create)
        return perm.can()

    @property
    def can_edit(self):
        perm = ActionNeedPermission(self.action_name, Edit)
        return perm.can()

    @property
    def can_delete(self):
        perm = ActionNeedPermission(self.action_name, Delete)
        return perm.can()

    @property
    def can_finish(self):
        perm = ActionNeedPermission(self.action_name, Delete)
        return perm.can()

    @property
    def can_view_details(self):
        try:
            perm = ActionNeedPermission(self.action_name, View)
            return perm.can()
        except:
            pass
        return False

    def format_export_value(self, value):
        if not value:
            value = ''
        if value is True:
            value = '是'
        if value is False:
            value = '否'

        return value

    @expose('/custom-actions', methods=['POST'])
    def custom_action(self):

        # 动作指示可能来源于请求的url

        id = request.args.get('id', '')
        action = request.args.get('action', '')

        self._custom_action(id, request.form, action)

        return redirect(self.get_url('.index_view'))

    def _custom_action(self, id_or_model, data, action='', direct_commit=True):
        # 非新增外的，支持流程操作的实现，可以使用该方法来实现流程里的状态变迁
        try:
            if isinstance(id_or_model, (str, unicode)):
                models = self.model.query.filter(
                    self.model.id.in_([id_or_model])).all()
            else:
                models = [id_or_model]
            if not action:
                # 也可能来自于请求的数据窗体
                # 目前已知的通过窗体提供的操作有
                allowed_form_actions = (
                    Approved, ApproveRefuse, ReviewApprove,
                    ReviewRefuse, SubmitReview,
                    Edit, ReviewAgain, Finish, Sent, Receive, ReserveAgain,
                    SecondApproved, SecondApproveRefuse, PutInStore,
                    UploadContractFile, UploadMeetingFile)

                for verb in allowed_form_actions:
                    if verb in data:
                        action = verb
                        break
            if not action:
                raise ValueError('没有指定的动作，请联系开发人员')

            for item in models:
                self._before_custom_action(item, action, **data)
                flow = self.support_flow(item)
                apply(getattr(flow, action), (), dict(
                    username=current_user, **data))
                # self.session.add(notifies)
            if direct_commit:
                self.session.commit()

        except Exception as ex:
            self.session.rollback()
            if "trigger event" in unicode(ex):
                flash('该单据状态已发生变化，请刷新当前单据。 %s' % (unicode(ex),), category='error')
            else:
                flash('无法执行指定的操作。 %s' % (unicode(ex),), category='error')

    def _before_custom_action(self, model, action, **kwargs):
        """为子视图的实现提供hook来影响后续的流程操作。

        如果要终止流程，请抛出异常
        """
        pass

    @expose('/download/', methods=('GET',))
    def download_view(self):
        key = request.args.get('key')
        post = {"key": key}
        url = "/v1/file-access/download"
        resp = proxy.create(post, url)
        acc_url = resp.json().get('url')
        return redirect(acc_url, 301)

    @property
    def action_name(self):
        return self.model.__name__.lower()

    def get_audit_form_class(self, model, verb):
        return None


    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        """
            Create model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_create:
            return redirect(return_url)

        form = self.create_form()
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            # in versions 1.1.0 and before, this returns a boolean
            # in later versions, this is the model itself
            model = self.create_model(form)
            if model:
                flash(gettext('Record was successfully created.'), 'success')
                if '_add_another' in request.form:
                    return redirect(request.url)
                elif '_continue_editing' in request.form:
                    # if we have a valid model, try to go to the edit view
                    if model is not True:
                        url = self.get_url('.edit_view', id=self.get_pk_value(model), url=return_url)
                    else:
                        url = return_url
                    return redirect(url)
                else:
                    # save button
                    return redirect(self.get_save_return_url(model, is_created=True))

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_create_rules)

        if self.create_modal and request.args.get('modal'):
            template = self.create_modal_template
        else:
            template = self.create_template

        return self.render(template,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url,
                           one_line_columns=self.one_line_columns)


    @expose('/action-view/', methods=['POST', 'GET'])
    def action_view(self):

        # 这个页面需要访问的url里包含verb参数
        verb = request.args.get('verb', None)
        if verb is None or verb not in self._action_view_cfg:
            return abort(404)
        cfg = self._action_view_cfg[verb]
        if verb == 'approve' and\
                self.support_flow.func in flow_map['two_approve']:
            cfg = self._action_view_cfg['sec-approve']

        return_url = get_redirect_target() or self.get_url('.index_view')
        if not self.can_view_details:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)
        if self.support_flow:
            only_columns = self.review_details_columns +\
                self.support_flow.func.get_flow_columns(model.status)
        details_columns = self.get_column_names(only_columns, None)

        form_class = cfg.form

        if self.get_audit_form_class(model, verb):
            form_class = self.get_audit_form_class(model, verb)

        if request.method == 'POST':
            self.process_flow_form(form_class, model, verb)
            return redirect(return_url)

        form = self.get_flow_form(form_class, model, verb)

        return self.render(
            self.action_view_template,
            action=self.get_url('.action_view', id=id, verb=verb),
            model=model,
            details_columns=details_columns,
            get_value=self.get_list_value,
            return_url=return_url,
            cancel_url=return_url,
            action_name=cfg.action_name,
            icon_value=cfg.icon_value,
            form=form,
            agreed=cfg.agreed,
            refuse=cfg.refuse,
            one_line_columns=self.one_line_columns,
            review_details_columns=self.review_details_columns
        )

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        if self.support_flow:
            if '/edit/' in request.url:
                url = request.url.replace('edit', 'approve-edit-view')
            return redirect(url)
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_edit_rules, form=form)

        if self.validate_form(form):
            if self.update_model(form, model):
                flash(gettext('Record was successfully saved.'), 'success')
                if '_add_another' in request.form:
                    return redirect(self.get_url('.create_view', url=return_url))
                elif '_continue_editing' in request.form:
                    return redirect(request.url)
                else:
                    # save button
                    return redirect(self.get_save_return_url(model, is_created=False))

        if request.method == 'GET' or form.errors:
            self.on_form_prefill(form, id)

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        if self.edit_modal and request.args.get('modal'):
            template = self.edit_modal_template
        else:
            template = self.edit_template

        return self.render(template,
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url,
                           one_line_columns=self.one_line_columns)



    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        """
            Edit model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            return redirect(return_url)

        self.before_edit_form(model)

        action = request.args.get('action', 'edit')

        cfg = self._action_view_cfg[action]

        details_columns = self.get_column_names(
            self.review_details_columns or self.column_details_list, None)
        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(
                ruleset=self._form_edit_rules, form=form)

        if self.validate_form(form):
            if self.update_model(form, model):
                if request.method == 'POST' and self.support_flow:

                    self._custom_action(id, request.form)
                flash(gettext('Record was successfully saved.'), 'success')
                return redirect(self.get_save_return_url(model,
                                                         is_created=False))

        if request.method == 'GET' or form.errors:
            self.on_form_prefill(form, id)

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        return self.render(
            self.approve_edit_template,
            action=self.get_url('.approve_edit_view', id=id, verb=action),
            model=model,
            details_columns=details_columns,
            get_value=self.get_list_value,
            return_url=return_url,
            cancel_url=return_url,
            action_name=cfg.action_name,
            icon_value=cfg.icon_value,
            form=form,
            agreed=cfg.agreed,
            refuse=cfg.refuse,
            form_opts=form_opts,
            one_line_columns=self.one_line_columns
        )

    @expose('/details/')
    def details_view(self):
        """
            Details model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_view_details:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        if self.details_modal and request.args.get('modal'):
            template = self.details_modal_template
        else:
            template = self.details_template

        return self.render(template,
                           model=model,
                           details_columns=self._details_columns,
                           get_value=self.get_list_value,
                           return_url=return_url,
                           one_line_columns=self.one_line_columns,
                           review_details_columns=self.review_details_columns)

    def get_flow_form(self, form_class, model, verb):
        return form_class(model_name=self.action_name)

    def process_flow_form(self, form_class, model, verb):
        self._custom_action(str(model.id), request.form)

    def create_form_with_default(self, inst, related=None, obj=None):
        tmp_form_class = self.get_create_form()
        for key, value in inst.__dict__.iteritems():
            if key not in self.review_details_columns:
                continue
            if key in ['statusName', 'number', 'remark', 'date']:
                continue
            tmp = getattr(tmp_form_class, key)
            tmp.kwargs['default'] = value
        if related:
            tmp = getattr(tmp_form_class, related)
            tmp.kwargs['default'] = inst
        return tmp_form_class(get_form_data(), obj=obj)

    def before_edit_form(self, model):
        pass

    def _export_data(self):
        # 导出数据(xls)

        export_page = request.args.get('export_page', 0, type=int)
        export_size = request.args.get('export_size', 0, type=int)
        search = request.args.get('search', '')
        view_args = self._get_list_extra_args()
        # Map column index to column name
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]
        export_data = super(CustomView, self)._export_data()
        # Get count and data
        export_data = self.get_list(export_page,
                                    sort_column,
                                    view_args.sort_desc,
                                    search,
                                    view_args.filters,
                                    page_size=export_size)

        return export_data

    def get_export_query(self, inst_id):
        return self.get_query()

    def get_export_pdf_column(self, inst_id=None):
        return self._export_columns

    def _view_handler(self, template_name, inst_id, with_404=False, **extra):
        models = self.get_export_query(inst_id)
        export_columns = self.get_export_pdf_column(inst_id)

        return self.render(
            template_name,
            models=models,
            export_columns=export_columns,
            get_export_value=self.get_export_value,
            extra=extra
        )

    @expose('/pdf/')
    def pdf_view(self):
        inst_id = request.args.get('id', '')
        return render_pdf(HTML(string=self._view_handler(self.pdf_template, inst_id,True)),
            stylesheets=[self.pdf_css])
