# coding: utf-8

from __future__ import unicode_literals

from flask import current_app, flash, request, redirect
from flask_admin import BaseView, expose
from flask_security import current_user
from flask_admin.helpers import get_form_data, is_form_submitted

from modules.roles import SuperAdmin
from modules.forms.basic_data.early_warning import EarlyWarningForm
from modules.models.basic_data.early_warning import EarlyWarning
from modules.proxy import proxy
from util.exception import BackendServiceError


class ConfigurationView(BaseView):
    "基础数据服务配置页面"

    def __init__(self, *args, **kwargs):
        self._template = 'configuration.html',
        super(ConfigurationView, self).__init__(
            name='基础信息配置',
            endpoint='configuration',
            **kwargs)

    def is_accessible(self):
        # 目前仅允许超级管理员访问该页面
        return current_user.has_role(SuperAdmin)

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        # 加载该界面的一些常用数据
        form = EarlyWarningForm()

        warn = EarlyWarning(current_app.redis_cache)
        warn.get_form(form)
        warn.get_value()
        warn.out_put()
        if is_form_submitted():
            form = EarlyWarningForm(formdata=get_form_data())
            if form.validate():
                warn.get_form(form)
                warnings = warn.set_warning()
                warn.out_put()
                current_app.predicts_cfg = warnings
                flash('配置设置成功。', 'success')
            else:
                flash('配置设置失败。', 'error')

        # 获取后台支持的文档类别
        resp = proxy.get('/v1/doc-type/')
        support_doctypes = []
        if resp.status_code == 200 and resp.json()['items'] is not None:
            support_doctypes = [item['id'] for item in resp.json()['items']]
        return self.render(self._template, form=form, support_doctypes=support_doctypes)

    @expose('/doc-type/', methods=['POST'])
    def add_doctype(self):
        url = '/v1/doc-type/'

        resp = proxy.get(url)
        if resp.status_code != 200:
            flash('暂时无法更新支持的文档资料列表', 'error')
            return redirect(self.get_url('.index'))

        # 原来支持的
        support_doctypes = resp.json()['items'] or []
        # 现在更新的
        doc_type = request.form.get('doc_type', None)
        if not doc_type:
            flash('文档资料类别不能为空。', 'error')
            return redirect(self.get_url('.index'))

        supported = set([item['id'] for item in support_doctypes])
        update = set(doc_type.split(','))

        if update < supported:
            flash('文档库资料类别只能新增或重置', 'error')
            return redirect(self.get_url('.index'))

        try:
            new_add = update - supported
            for item in new_add:
                doc_type = dict(id=item, value=item)
                proxy.create(doc_type, url)
        except:
            raise BackendServiceError('Update support doctype occured failure.')
        flash('文档资料类别更新成功。', 'success')
        return redirect(self.get_url('.index'))

    @expose('/reset-doctype/', methods=['POST'])
    def reset_doctype(self):
        url = '/v1/doc-type/'

        resp = proxy.get(url)
        if resp.status_code != 200:
            flash('暂时无法更新支持的文档资料列表', 'error')
            return redirect(self.get_url('.index'))

        try:
            support_doctypes = resp.json()['items']
            for item in support_doctypes:
                # 只有扩展的需要删除
                if 'expanded' in item and item['expanded']:
                    doc_type = dict(id=item['id'], value=item['id'])
                    proxy.delete_with_data(doc_type, url, item['etag'])
        except:
            raise BackendServiceError('Update support doctype occured failure.')

        flash('文档库资料类别重置完毕。', 'success')
        return redirect(self.get_url('.index'))
