# encoding: utf-8
from __future__ import unicode_literals

import json
import hashlib
from wtforms import form, fields
from wtforms.validators import DataRequired
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm, Y5BIntervalDescForm
from util.fields.accessory_filed import MxpMultiFileuploadField
from ..meta import y5b_scheduled_source, type_map


class TimeControlUnitForm(form.Form):
    id = fields.StringField('编号', [DataRequired()])
    ataCode = fields.StringField('ATA章节号')
    source = fields.SelectField('来源', choices=y5b_scheduled_source)
    pn = fields.StringField('型号', [DataRequired()])
    name = fields.StringField('名称', [DataRequired()])
    pieceNo = fields.StringField('件号', [DataRequired()])
    unitNo = fields.SelectField('部件型号', choices=[])
    remark = fields.StringField('备注')
    description = fields.StringField('维修描述', [DataRequired()])
    interval = InlineFormField(Y5BIntervalDescForm, '间隔类型 *')
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    accessory = MxpMultiFileuploadField(label='附件')
    etag = fields.HiddenField('etag')


def read_datas(row):

    data = {
        'id': row['编号'.encode('utf-8')],
        'ataCode': row['ATA章节号'.encode('utf-8')],
        'pn': row['型号'.encode('utf-8')],
        'name': row['名称'.encode('utf-8')],
        'pieceNo': row['件号'.encode('utf-8')],
        'description': row['维修描述'.encode('utf-8')],
        'remark': row['备注'.encode('utf-8')],
        'interval': []
    }

    if row['来源'.encode('utf-8')]:
        data['source'] = row['来源'.encode('utf-8')]

    if row['部件型号'.encode('utf-8')]:
        data['unitNo'] = row['部件型号'.encode('utf-8')]

    if row['基准h'.encode('utf-8')]:
        item = {
            'type': 0,
            'value': float(row['基准h'.encode('utf-8')]),
            'max': 0.0,
            'min': 0.0,
        }
        if row['最小值h'.encode('utf-8')]:
            item['min'] = float(row['最小值h'.encode('utf-8')])
        if row['最大值h'.encode('utf-8')]:
            item['max'] = float(row['最大值h'.encode('utf-8')])
        data['interval'].append(item)

    if row['基准t'.encode('utf-8')]:
        item = {
            'type': 1,
            'value': float(row['基准t'.encode('utf-8')]),
            'max': 0.0,
            'min': 0.0,
        }
        if row['最小值t'.encode('utf-8')]:
            item['min'] = float(row['最小值t'.encode('utf-8')])
        if row['最大值t'.encode('utf-8')]:
            item['max'] = float(row['最大值t'.encode('utf-8')])
        data['interval'].append(item)

    if row['基准d'.encode('utf-8')]:
        item = {
            'type': type_map[row['基准类型d'.encode('utf-8')].decode('utf-8')],
            'value': float(row['基准d'.encode('utf-8')]),
            'max': 0.0,
            'min': 0.0,
            'offsetType': 2
        }
        if row['最小值d'.encode('utf-8')]:
            item['min'] = float(row['最小值d'.encode('utf-8')])
        if row['最大值d'.encode('utf-8')]:
            item['max'] = float(row['最大值d'.encode('utf-8')])
        if row['偏差类型d'.encode('utf-8')]:
            item['offsetType'] = type_map[row['偏差类型d'.encode('utf-8')].decode('utf-8')]
        data['interval'].append(item)

    if row['基准e'.encode('utf-8')]:
        item = {
            'type': 9,
            'value': float(row['基准e'.encode('utf-8')]),
            'max': 0.0,
            'min': 0.0,
        }
        if row['最小值e'.encode('utf-8')]:
            item['min'] = float(row['最小值e'.encode('utf-8')])
        if row['最大值e'.encode('utf-8')]:
            item['max'] = float(row['最大值e'.encode('utf-8')])
        data['interval'].append(item)

    md5_data = json.dumps(data)
    hash_md5 = hashlib.md5(md5_data)
    data['etag'] = hash_md5.hexdigest()

    return data
