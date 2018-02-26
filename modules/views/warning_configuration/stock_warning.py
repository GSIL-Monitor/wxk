# coding: utf-8

from __future__ import unicode_literals

from flask import current_app, flash
from flask_admin import BaseView, expose
from flask_security import current_user
from flask_admin.helpers import get_form_data, is_form_submitted

from modules.roles import SuperAdmin
from modules.forms.basic_data.stock_warning import StockWarningForm
from modules.models.maturity_warning_configuration.stock_warning import StockWarning


class StockWaringConfigurationView(BaseView):
    """库存预警服务配置页面"""

    def __init__(self, *args, **kwargs):
        self._template = 'maturity_warning/stock_warning.html',
        super(StockWaringConfigurationView, self).__init__(
            name='库存预警信息配置',
            endpoint='stockwarning_configuration',
            **kwargs)

    def is_accessible(self):
        # 目前仅允许超级管理员访问该页面
        return current_user.has_role(SuperAdmin)

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        # 加载该界面的一些常用数据
        form = StockWarningForm()
        warn = StockWarning(current_app.redis_cache)
        warn.get_form(form)
        warn.get_value()
        warn.out_put()
        if is_form_submitted():
            form = StockWarningForm(formdata=get_form_data())
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
