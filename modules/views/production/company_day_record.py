# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import time

from flask import url_for, redirect, request, flash
from flask_admin import expose
from flask_admin.form import FormOpts
from flask_admin.babel import gettext
from wtforms import DateTimeField, SelectField
from wtforms.validators import DataRequired
from modules.flows.states import Edited, Finished
from modules.helper import get_allowed_aircrafts
from util.fields.select import WithTypeSelectMultiField
from modules.flows import BasicFlow
from modules.models.production.company_day_record import CompanyDayRecord
from modules.views import CustomView, fullcanlendar_events
from modules.views.column_formatter import cancel_formatter
from util.widgets import DateTimeWidget
from flask_admin.helpers import get_redirect_target
from modules.views.custom import ActionViewCfg
from modules.flows.operations import Edit, Finish
from modules.views.operations import ActionNeedPermission
from ..column_formatter import accessory_formatter
from util.fields.accessory_filed import CompanyDayRecordFileuploadField


class _CompanyDayRecordView(CustomView):
    # 单位日运行记录列表视图应显示的内容

    create_template = 'companydayrecord/create.html'
    edit_template = 'companydayrecord/edit.html'

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
        '/static/js/upload_file.js',
    ]
    column_list = [
        'serialNum', 'flightDate', 'planeNum',
        'flyPlanApplicant', 'actulizeApplicant',
    ]
    column_details_list = [
        'serialNum', 'flightDate', 'planeNum',
        'windDirction', 'flySpeed', 'airPressure',
        'visibility', 'cloudCover', 'temperature',
        'highFrequencyWorkStatus', 'communicationWorkStatus',
        'flyPlanApplicant', 'flyPlanApplicationDate',
        'actulizeApplicant', 'actulizeApplicationDate1',
        'actulizeApplicationDate2', 'actulizeApplicationDate3',
        'actulizeApplicationDate4', 'xuzhouFlyTime',
        'hefeiFlyTime', 'nanjingFlyTime',
        'jinanFlyTime', 'xuzhouFlyEndTime', 'hefeiFlyEndTime',
        'nanjingFlyEndTime', 'jinanFlyEndTime', 'fileResourceUrl'
    ]

    # 对应内容的中文翻译
    column_labels = {
        'serialNum': '编号',
        'flightDate': '飞行日期',
        'planeNum': '飞机号',
        'windDirction': '风向',
        'flySpeed': '风速',
        'airPressure': '气压',
        'visibility': '能见度',
        'cloudCover': '云量',
        'temperature': '温度',
        'highFrequencyWorkStatus': '甚高频工作工作状态',
        'communicationWorkStatus': '通讯记录仪工作状态',
        'flyPlanApplicant': '飞行计划申请单位',
        'flyPlanApplicationDate': "飞行计划申请时间",
        'actulizeApplicant': '实施单位',
        'actulizeApplicationDate1': "实施单位申请时间1",
        'actulizeApplicationDate2': "实施单位申请时间2",
        'actulizeApplicationDate3': "实施单位申请时间3",
        'actulizeApplicationDate4': "实施单位申请时间4",
        'actulizeRecord': '实施记录',
        'xuzhouFlyTime': '徐州管分队起飞报',
        'hefeiFlyTime': '合肥区调起飞报',
        'nanjingFlyTime': '南京进近起飞报',
        'jinanFlyTime': '济南区调起飞报',
        'xuzhouFlyEndTime': '徐州管分队飞行结束报',
        'hefeiFlyEndTime': '合肥区调飞行结束报',
        'nanjingFlyEndTime': '南京进近飞行结束报',
        'jinanFlyEndTime': '济南区调飞行结束报',
        'fileResourceUrl': '附件',
        'maker': '制单人',
        'makeTime': '制单时间',
        'modifier': '修改人',
        'modifyTime': '修改时间',
        'operation': '操作',
    }
    form_excluded_columns = ['statusName', 'actulizeRecord']

    column_formatters = {
        'cancel': cancel_formatter,
    }

    one_line_columns = ['fileResourceUrl']

    support_flow = partial(BasicFlow, 'Finish flow')
    status_choices = [
        ('较好', '较好'),
        ('良好', '良好'),
        ('正常', '正常'),
        ('一般', '一般'),
        ('较差', '较差'),
    ]

    form_overrides = {
        'flyPlanApplicationDate': partial(
            DateTimeField, widget=DateTimeWidget()),
        'actulizeApplicationDate1': partial(
            DateTimeField, widget=DateTimeWidget()),
        'actulizeApplicationDate2': partial(
            DateTimeField, widget=DateTimeWidget()),
        'actulizeApplicationDate3': partial(
            DateTimeField, widget=DateTimeWidget()),
        'actulizeApplicationDate4': partial(
            DateTimeField, widget=DateTimeWidget()),
        'xuzhouFlyEndTime': partial(DateTimeField, widget=DateTimeWidget()),
        'hefeiFlyEndTime': partial(DateTimeField, widget=DateTimeWidget()),
        'nanjingFlyEndTime': partial(DateTimeField, widget=DateTimeWidget()),
        'jinanFlyEndTime': partial(DateTimeField, widget=DateTimeWidget()),
        'xuzhouFlyTime': partial(DateTimeField, widget=DateTimeWidget()),
        'hefeiFlyTime': partial(DateTimeField, widget=DateTimeWidget()),
        'nanjingFlyTime': partial(DateTimeField, widget=DateTimeWidget()),
        'jinanFlyTime': partial(DateTimeField, widget=DateTimeWidget()),
        'highFrequencyWorkStatus': partial(
            SelectField, choices=status_choices),
        'communicationWorkStatus': partial(
            SelectField, choices=status_choices),
        'flyPlanApplicant': partial(WithTypeSelectMultiField, choices=[
            ('徐州7分队', '徐州7分队'),
            ('合肥区调', '合肥区调'),
        ]),
        'actulizeApplicant': partial(SelectField, choices=[
            ('农行站', '农行站'),
        ]),
        'fileResourceUrl': partial(CompanyDayRecordFileuploadField),
    }

    column_formatters = {
        'fileResourceUrl': accessory_formatter('fileResourceUrl'),
    }

    @property
    def form_widget_args(self):
        return {
            'flightDate': {
                'readonly': True,
            },

        }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.serialNum.validators = [DataRequired()]
            form.flightDate.validators = [DataRequired()]
            form.planeNum.validators = [DataRequired()]
        return super(_CompanyDayRecordView, self).validate_form(form)

    @expose()
    def index_view(self):
        return redirect(url_for('flightlog.index_view'))

    def is_visible(self):
        return False

    @expose('/all-events/')
    @fullcanlendar_events
    def get_events(self, date_str, timestamp):
        className = 'label label-green-haze'
        if not CompanyDayRecord.has_related_status_by_day(date_str, Finished):
            title = u'编辑日运行记录'
            url = self.get_url('.edit_view', timestamp=timestamp)
        else:
            title = u'查看日运行记录'
            className = 'label label-green-jungle'
            url = self.get_url('.details_view', timestamp=timestamp)

        if '编辑' in title:

            if not (CompanyDayRecord.has_related_status_by_day(date_str, Edited) or\
                    CompanyDayRecord.has_related_status_by_day(date_str)):
                title = u'新增日运行记录'
                className = 'label label-green'
                url = self.get_url('.create_view', timestamp=timestamp)

        if '新增' in title and not self.can_create:
            return
        if '编辑' in title and not self.can_edit:
            return
        if '查看' in title and not self.can_view_details:
            return
        return (url, title, className)

    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        self._create_form_class.planeNum = WithTypeSelectMultiField('飞机号', choices=[
            (aircraft.id, aircraft.id) for aircraft in get_allowed_aircrafts('y5b')])

        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_create:
            return redirect(return_url)

        form = self.create_form()
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_create_rules, form=form)

        if self.validate_form(form):
            model = self.create_model(form)
            if model:
                flash(gettext('Record was successfully created.'), 'success')
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

    @expose('/edit/', methods=['GET', 'POST'])
    def edit_view(self):
        self._edit_form_class.planeNum = WithTypeSelectMultiField('飞机号', choices=[
            (aircraft.id, aircraft.id) for aircraft in get_allowed_aircrafts('y5b')])

        return_url = get_redirect_target() or self.get_url('.index_view')
        if request.method == "POST":
            ts = time.mktime(time.strptime(request.form['flightDate'], "%Y-%m-%d"))
        else:
            ts = float(request.args.get('timestamp'))
        timeori = time.strftime("%Y-%m-%d", time.localtime(ts))
        model = CompanyDayRecord.query.filter_by(flightDate=timeori).first()
        if not self.can_edit:
            return redirect(return_url)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)
        model_id = model.id
        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_edit_rules, form=form)

        if self.validate_form(form):
            if self.update_model(form, model):
                if request.method == 'POST' and self.support_flow:

                    self._custom_action(model, request.form)
                flash(gettext('Record was successfully saved.'), 'success')
                return redirect(self.get_save_return_url(model,
                                                         is_created=False))

        perm = ActionNeedPermission('companydayrecord', Finish)
        refuse_op = ('保存并完成', Finish) if perm.can() else None
        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        details_columns = self.get_column_names(
            self.review_details_columns or self.column_details_list, None)

        cfg = ActionViewCfg('', 'fa-bell-o', None, ('保存', Edit), ('保存并完成', Finish))

        return self.render(
            self.edit_template,
            action=self.get_url('.edit_view', verb='edit', id=model_id),
            model=model,
            details_columns=details_columns,
            get_value=self.get_list_value,
            return_url=return_url,
            cancel_url=return_url,
            action_name=cfg.action_name,
            icon_value=cfg.icon_value,
            form=form,
            agreed=cfg.agreed,
            refuse=refuse_op,
            form_opts=form_opts,
            model_id=model_id,
            one_line_columns=self.one_line_columns,
        )

    @expose('/details/')
    def details_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_view_details:
            return redirect(return_url)

        ts = float(request.args.get('timestamp'))
        timeori = time.strftime("%Y-%m-%d", time.localtime(ts))
        model = CompanyDayRecord.query.filter_by(flightDate=timeori).first()

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


CompanyDayRecordView = partial(
    _CompanyDayRecordView, CompanyDayRecord, name='单位日运行记录'
)
