# coding: utf-8

from __future__ import unicode_literals

import json
import logging
from flask import request, redirect, flash
from flask_admin.babel import gettext
from flask_admin.model.helpers import get_mdict_item_or_list
from exceptions import ValueError
from modules.helper import get_allowed_aircrafts
from modules.models.airmaterial import Supplier, Manufacturer, RepairSupplier

log = logging.getLogger("flask-admin.sqla")


class InlineTable(object):

    def after_model_change(self, form, model, is_created):
        try:
            if not getattr(model, 'id'):
                raise ValueError('记录建立失败')
            for old_material in getattr(model, self.relationField):
                self.session.delete(old_material)
            table_data = request.form.get('table_datas').replace('null', 'None')
            if not table_data:
                raise ValueError('航材列表数据出现错误')
            table_data = eval(table_data)
            table_data = [[col if col != '' else None for col in row] for row in table_data]
            for row in table_data:
                model_dict = {}
                for i, r in enumerate(row):
                    model_dict.update({self.table_columns.keys()[i]: r})
                model_dict.update({self.f_key: model.id})
                rl_model = self.relationModel(**model_dict)
                self.session.add(rl_model)
            self.session.commit()
        except Exception:
            self.session.rollback()
            self.session.commit()
            flash('航材列表数据出现错误，记录建立失败', 'error')
            log.exception('Failed to create record.')

    def on_model_delete(self, model):
        for old_material in getattr(model, self.relationField):
            self.session.delete(old_material)
        self.session.commit()

    def get_table_data_from_db(self, model=None):

        if not model:
            id = get_mdict_item_or_list(request.args, 'id')
            return_url = self.get_url('.index_view')

            if id is None:
                return redirect(return_url)

            model = self.get_one(id)

            if model is None:
                flash(gettext('Record does not exist.'), 'error')
                return redirect(return_url)

        table_datas = []
        for table_model in getattr(model, self.relationField):
            data = []
            for fields in self.table_columns.keys():
                data.append(getattr(table_model, fields))
            table_datas.append(data)
        return json.dumps(table_datas)

    def get_readonly_table(self):
        table_columns = json.loads(self.init_table_columns())
        for column in table_columns:
            column.update({'readOnly': True})
        return json.dumps(table_columns)

    def get_aircraft(self, bounded=None):
        # 获取机号列表
        rest = []
        if bounded == '1':
            bounded = 1
        else:
            bounded = None
        for aircraft in get_allowed_aircrafts('y5b', bounded):
            rest.append(aircraft.id)
        return rest

    def get_manufacturer(self):
        return [s.name for s in Manufacturer.query.all()]

    def get_supplier(self):
        return [s.name for s in Supplier.query.all()]

    def get_repair_supplier(self):
        return [s.name for s in RepairSupplier.query.all()]

    def get_accessory_from_before(self, form, number, types_dict):
        key = number[0:4]
        acce_field = getattr(form, 'accessory')
        type_model = types_dict[key][0]
        inst = type_model.query.filter(
            type_model.number == number).first()
        if 'accessory' in inst.__dict__.keys():
            acce_field.data = inst.accessory

    def get_export_query(self, inst_id):
        if self.inline_model and inst_id:
            tr = getattr(self.inline_model, self.inline_column)
            return self.inline_model.query.join(self.model).filter(tr == inst_id)

    def get_export_value(self, model, name):

        if name in model.__dict__.keys():
            return self._get_list_value(
                None,
                model,
                name,
                self.column_formatters_export,
                self.column_type_formatters_export,
            )
        if not self.inline_column or not self.inline_model:
            return ''

        tr = getattr(self.inline_model, self.inline_column)
        inst = self.model.query.join(
            self.inline_model).filter(
                tr == self.model.id, self.inline_model.id == model.id).first()

        return self._get_list_value(
            None,
            inst,
            name,
            self.column_formatters_export,
            self.column_type_formatters_export,
        )
