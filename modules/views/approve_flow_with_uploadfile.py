# coding: utf-8

from __future__ import unicode_literals

from flask_admin import expose
from flask import request, abort
from flask_admin.helpers import get_form_data, is_form_submitted

from modules.views.airmaterial.with_inline_table import WithInlineTableView


class ApproveFlowUploadFileView(WithInlineTableView):
    """
    如果审批流程中添加了上传文件的功能，可以通过继承该类，
    但需要在子类中
    1.用accessory_formatter对改字段进行格式化
    2.添加upload_file.js
    在子类模型中定义相关的文件字段如contractFile或者meetingFile
    """

    @expose('/action-view/', methods=['POST', 'GET'])
    def action_view(self):
        verb_files = {
            'upload_contract_file': 'contractFile',
            'upload_meeting_file': 'meetingFile',
        }

        # 这个页面需要访问的url里包含verb参数
        verb = request.args.get('verb', None)
        if verb is None or verb not in self._action_view_cfg:
            return abort(404)
        if verb in ['upload_contract_file', 'upload_meeting_file']:
            tmp_id = request.args.get('id', '')
            model = self.model.query.filter(self.model.id == tmp_id).first()
            cfg = self._action_view_cfg[verb]
            self.form = cfg.form()
            field = verb_files[verb]
            files = getattr(model, field)
            if files:
                setattr(getattr(self.form, field), 'data', files)
            if is_form_submitted():
                self.file_upload_process(cfg.form, model)
        return super(ApproveFlowUploadFileView, self).action_view()

    def file_upload_process(self, file_form, model):
        tmp_form = file_form(formdata=get_form_data())
        if tmp_form.validate():
            tmp_form.populate_obj(model)
            self.session.commit()

    def get_flow_form(self, form_class, model, verb):
        if verb in ['upload_contract_file', 'upload_meeting_file']:
            verb_files = {
                'upload_contract_file': 'contractFile',
                'upload_meeting_file': 'meetingFile',
            }
            form = form_class()
            field = verb_files[verb]
            files = getattr(model, field)
            if files:
                setattr(getattr(form, field), 'data', files)
            return form
        else:
            return super(ApproveFlowUploadFileView, self).\
                get_flow_form(form_class, model, verb)

    def process_flow_form(self, form_class, model, verb):
        if verb in ['upload_contract_file', 'upload_meeting_file']:
            form = form_class(formdata=get_form_data())
            if form.validate():
                form.populate_obj(model)
            self.session.commit()
        else:
            super(ApproveFlowUploadFileView, self).\
                process_flow_form(form_class, model, verb)
