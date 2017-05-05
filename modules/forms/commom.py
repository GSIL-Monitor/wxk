# encoding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields

from util.fields import BasicIntervalField, SpecailIntervalField
from wtforms.compat import iteritems


def interval_types(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string.')

    basic = [
        (0, '飞行小时'),
        (1, '起落次数/循环次数'),
        (2, '日历天'),
        (3, '日历月'),
        (4, '日历年')]

    plane_type = plane_type.lower()
    if plane_type in ['bell206', 'bell407', 'bell429']:
        basic.append((5, '退役指数'))
    elif plane_type in ['as350']:
        basic.extend([(6, '扭矩循环次数(TC)'),
                      (7, '燃气发生器循环数(NG)'),
                      (8, '动力涡轮循环数(NF)')])
    elif plane_type in ['da40d', 'swz269c1', 'r22', 'r44']:
        pass
    else:
        raise ValueError('please check the plane type')

    class IntervalDescForm(form.Form):
                # type = fields.SelectField('间隔类型', choices=basic, coerce=int)
        # value = fields.FloatField('间隔值', default=100)
        # min = fields.FloatField('间隔下限', default=0)
        # max = fields.FloatField('间隔上限', default=0)
        # # group = fields.HiddenField('间隔分组')
        # # offsetType = fields.HiddenField('间隔类型')
        hours = BasicIntervalField('飞行小时')
        times = BasicIntervalField('起落次数')
        t_time = SpecailIntervalField('间隔值')

        def process(self, formdata=None, obj=None, data=None, **kwargs):
            # import pdb;pdb.set_trace()
            formdata = self.meta.wrap_formdata(self, formdata)

            if formdata is not None:
                obj = None

            if data is not None:
                kwargs = dict(data, **kwargs)

            for name, field, in iteritems(self._fields):
                if obj is not None:
                    for interval in obj:
                        if name == 'hours' and int(interval.get('type')) == 0:
                            field.process(formdata, interval)
                        if name == 'times' and int(interval.get('type')) == 1:
                            field.process(formdata, interval)
                        if name == 't_time' and int(interval.get('type')) > 1:
                            field.process(formdata, interval)
                else:
                    if name == 'hours':
                        field.process(formdata)
                    if name == 'times':
                        field.process(formdata)
                    if name == 't_time':
                        field.process(formdata)

        def process_form_base(self, form_data, key, word, i_type):

            processed = {}
            processed['type'] = int(i_type)

            for interval_value in form_data[key]:
                if '{}-{}-max'.format(word, key) in interval_value.keys():
                            processed['max'] = interval_value.values()[0]
                if '{}-{}-min'.format(word, key) in interval_value.keys():
                            processed['min'] = interval_value.values()[0]
                if '{}-{}-value'.format(word, key) in interval_value.keys():
                            processed['value'] = interval_value.values()[0]

            for k, v in processed.items():
                if k != 'type':
                    processed[k] = float(v)

            return processed

        def process_form_spec(self, form_data, key, word):
            processed = {}

            for interval_value in form_data[key]:
                if '{}-{}-offsetType'.format(word, key) in interval_value.keys():
                    processed['offsetType'] = interval_value.values()[0]
                if '{}-{}-type'.format(word, key) in interval_value.keys():
                    processed['type'] = interval_value.values()[0]
            base = self.process_form_base(form_data, key, word, processed['type'])

            processed.update(base)
            return processed

        @property
        def data(self):

            data_list = []
            form_data = dict((name, f.data) for name, f in iteritems(self._fields))

            for key in form_data:
                if key == 'hours' and form_data['hours'] is not None:
                    data_list.append(self.process_form_base(form_data, key, 'interval', 0))
                elif key == 'times' and form_data['times'] is not None:
                    data_list.append(self.process_form_base(form_data, key, 'interval', 1))
                elif key == 't_time' and form_data['t_time'] is not None:
                    data_list.append(self.process_form_spec(form_data, 't_time', 'interval'))
                else:
                    pass
            return data_list

    return IntervalDescForm


class RelateDocForm(form.Form):
    name = fields.StringField('文件名')
    type = fields.StringField('类型')
    key = fields.HiddenField('唯一性信息')


class AccessoryForm(form.Form):
    name = fields.StringField('附件名称')
    key = fields.HiddenField('唯一性信息')


class TrackingDescForm(form.Form):
    type = fields.IntegerField('类型')
    value = fields.FloatField('时间点值')
