# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
from util.fields.accessory_filed import AirmaterialFileuploadField
from wtforms.fields.core import Label


class ContractFileForm(form.Form):
    contractFile = AirmaterialFileuploadField('合同文件')

    def __init__(self, label='', *args, **kwargs):
        super(ContractFileForm, self).__init__(*args, **kwargs)
        if label:
            self.contractFile.label = Label('contractFile', label)

class MeetingFileForm(form.Form):
    meetingFile = AirmaterialFileuploadField('会议纪要')

    def __init__(self, label='', *args, **kwargs):
        super(MeetingFileForm, self).__init__(*args, **kwargs)
        if label:
            self.meetingFile.label = Label('meetingFile', label)