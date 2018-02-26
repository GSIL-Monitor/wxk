# coding: utf-8

from __future__ import unicode_literals

from flask import current_app, flash
from flask_admin import BaseView, expose
from flask_security import current_user
from flask_admin.helpers import get_form_data, is_form_submitted

from modules.roles import SuperAdmin
from modules.forms.basic_data.check_warning import CheckWarningForm
from modules.models.maturity_warning_configuration.check_warning import CheckWarning


class CheckWaringConfigurationView(BaseView):
    """航材预警服务配置页面"""

    def __init__(self, *args, **kwargs):
        self._template = 'maturity_warning/check_warning.html',
        super(CheckWaringConfigurationView, self).__init__(
            name='检查预警信息配置',
            endpoint='airmaterial_configuration',
            **kwargs)

    def is_accessible(self):
        # 目前仅允许超级管理员访问该页面
        return current_user.has_role(SuperAdmin)

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        # 加载该界面的一些常用数据
        form = CheckWarningForm()
        warn = CheckWarning(current_app.redis_cache)
        warn.get_form(form)
        warn.get_value()
        warn.out_put()
        if is_form_submitted():
            form = CheckWarningForm(formdata=get_form_data())
            try:
                if form.validate():
                    warn.get_form(form)
                    warnings = warn.set_warning()
                    warn.out_put()
                    current_app.predicts_cfg = warnings
                    flash('配置设置成功。', 'success')
                else:
                    flash('配置设置失败！请检查您的输入数据类型是否为整数。', 'error')
            except ValueError as ex:
                flash('Failed. %s' % ex.message, 'error')
        return self.render(self._template, form=form, support_doctypes=None)
