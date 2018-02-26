# encoding: utf-8
from __future__ import unicode_literals

import json
import hashlib
from wtforms import form, fields
from wtforms.validators import DataRequired
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm
from util.fields.accessory_filed import MxpMultiFileuploadField
from ..meta import y5b_scheduled_source, da40d_flight_line_category


class FlightLineCheckForm(form.Form):
    id = fields.StringField('编号', [DataRequired()])
    source = fields.SelectField('来源', choices=y5b_scheduled_source)
    adapt = fields.StringField('适用性')
    remark = fields.StringField('备注')
    description = fields.StringField('维修描述', [DataRequired()])
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    accessory = MxpMultiFileuploadField(label='附件')
    etag = fields.HiddenField('etag')


def read_datas(row):

    data = {
        'id': row['编号'.encode('utf-8')],
        'adapt': row['适用性'.encode('utf-8')],
        'description': row['维修描述'.encode('utf-8')],
        'remark': row['备注'.encode('utf-8')],
    }

    if row['来源'.encode('utf-8')]:
        data['source'] = row['来源'.encode('utf-8')]

    md5_data = json.dumps(data)
    hash_md5 = hashlib.md5(md5_data)
    data['etag'] = hash_md5.hexdigest()

    return data
