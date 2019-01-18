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
