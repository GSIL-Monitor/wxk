# coding: utf-8

from __future__ import unicode_literals

from flask_admin.form.widgets import Select2Widget
from flask_admin.form.fields import Select2Field
from wtforms import SelectField, SelectMultipleField
from wtforms.utils import unset_value
from werkzeug._compat import text_type

from modules.proxy import proxy
from modules.models.basic_data.airport import Airport
from modules.models.basic_data.fly_nature import FlyNature
from modules.models.basic_data.formula import Formula
from modules.models.user import User
from modules.models.role import Role
from modules.roles import SuperAdmin
from modules.models.airmaterial.supplier import Supplier
from modules.models.airmaterial.repair_supplier import RepairSupplier
from ..widgets.select import WithTypeSelect, WithTypeSelect2
from util.exception import BackendServiceError


class RefreshFileTypeSelectField(SelectField):

    def __init__(self, *args, **kwargs):

        super(RefreshFileTypeSelectField, self).__init__(choices=self.get_choice(),
                                                         *args, **kwargs)

    def get_choice(self):
        doc_type = []
        url = '/v1/doc-type/'
        resp = proxy.get(url)
        if resp.status_code != 200:
            raise BackendServiceError('API has something wrong.')
        items = resp.json().get('items')
        if not items:
            raise BackendServiceError('API has something wrong.')
        for item in items:
            # if item.get('expanded'):
            #     doc_type.append((item.get('id'), item.get('id')))
            # else:
            #     doc_type.append(("temporary", item.get('id')))
            doc_type.append((item.get('id'), item.get('id')))
        return doc_type


class RefreshPlaneTypeSelectField(SelectField):

    def __init__(self, *args, **kwargs):
        super(RefreshPlaneTypeSelectField, self).__init__(choices=self.get_choice(),
                                                          *args, **kwargs)

    def get_choice(self):
        resp = proxy.get('/v1/support-plane-types/')
        if resp.status_code != 200:
            raise BackendServiceError('API has something wrong.')
        items = resp.json()['items']
        if not items:
            raise BackendServiceError('API has something wrong.')
        result = []
        for x in items:
            tmp_dict = tuple(dict(key=items[x], value=x).values())
            result.append(tmp_dict)
        return result


class RefreshAirportSelectField(SelectField):

    def __init__(self, *args, **kwargs):
        super(
            RefreshAirportSelectField, self).__init__(
                choices=self.get_choice(),
                *args, **kwargs)

    def get_choice(self):
        airport = Airport.query.all()
        result = []
        for x in airport:
            tmp_dict = tuple(dict(key=x.name, value=x.name).values())
            result.append(tmp_dict)
        return result


class RefreshFlyNatureSelectField(SelectField):

    def __init__(self, *args, **kwargs):
        super(
            RefreshFlyNatureSelectField, self).__init__(
                choices=self.get_choice(),
                *args, **kwargs)

    def get_choice(self):
        flyNature = FlyNature.query.all()
        result = []
        for x in flyNature:
            tmp_dict = tuple(dict(key=x.name, value=x.name).values())
            result.append(tmp_dict)
        return result


class RefreshFormulaSelectField(SelectField):

    def __init__(self, *args, **kwargs):
        super(
            RefreshFormulaSelectField, self).__init__(
                choices=self.get_choice(),
                *args, **kwargs)

    def get_choice(self):
        formula = Formula.query.all()
        result = []
        for x in formula:
            tmp_dict = tuple(dict(key=x.name, value=x.name).values())
            result.append(tmp_dict)
        return result


class RefreshSupplierSelectField(SelectField):

    def __init__(self, *args, **kwargs):
        super(
            RefreshSupplierSelectField, self).__init__(
                choices=self.get_choice(),
                *args, **kwargs)

    def get_choice(self):
        def_choice = [('', '')]
        def_choice.extend([(s.name, s.name) for s in Supplier.query.all()])
        return def_choice


# 动态可更新的维修厂商选择Field
class RefreshRepairSupplierSelectField(SelectField):

    def __init__(self, *args, **kwargs):
        super(
            RefreshRepairSupplierSelectField, self).__init__(
                choices=self.get_choice(),
                *args, **kwargs)

    def get_choice(self):
        def_choice = [('', '')]
        def_choice.extend([(s.name, s.name) for s in RepairSupplier.query.all()])
        return def_choice


class WithTypeSelectField(SelectField):
    widget = WithTypeSelect()

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v[0]:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class WithTypeSelectMultiField(SelectMultipleField):
    widget = Select2Widget(multiple=True)

    def populate_obj(self, obj, name):
        setattr(obj, name, ','.join(self.data))

    def process_data(self, value):
        if value is not None:
            value = value.split(',')
        try:
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None


class choiceUserSelectField(SelectMultipleField):
    widget = Select2Widget(multiple=True)

    def __init__(self, *args, **kwargs):
        users = User.query.all()
        super(choiceUserSelectField, self).__init__(
            choices=[(user.username, user.username) for user in users],
            *args, **kwargs)

    def process_data(self, value):
        try:
            if value is not None:
                value = value.split(',')
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def populate_obj(self, obj, name):
        if self.data is not None:
            self.data = ','.join(self.data)
        setattr(obj, name, self.data)


class choiceRealNameSelectField(SelectMultipleField):
    widget = Select2Widget(multiple=True)

    def __init__(self, *args, **kwargs):
        users = User.query.filter(User.realName.isnot(None)).all()
        super(choiceRealNameSelectField, self).__init__(
            choices=[(user.realName, user.realName) for user in users],
            *args, **kwargs)

    def process_data(self, value):
        try:
            if value is not None:
                value = value.split(',')
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def populate_obj(self, obj, name):
        if self.data is not None:
            self.data = ','.join(self.data)
        setattr(obj, name, self.data)


class RefreshRoleSelectFiled(SelectField):

    def __init__(self, *args, **kwargs):
        super(RefreshRoleSelectFiled, self).__init__(choices=self.get_choice(),
                                                     *args, **kwargs)

    def get_choice(self):
        return [(r.name, r.name) for r in Role.query.filter(Role.name != '超级管理员').all()]


class UserWithRoleSelectMultiField(Select2Field):

    widget = WithTypeSelect2(multiple=True)

    def __init__(self, *args, **kwargs):
        super(UserWithRoleSelectMultiField, self).__init__(
            choices=self.get_choice(), *args, **kwargs)

    def get_choice(self):
        return [((u.realName, self.get_user_roles_str(u)),
                 u.realName) for u in User.query.filter(User.username != 'admin').all()]

    def get_user_roles_str(self, user):
        res = []
        for r in user.roles:
            res.append(r.name)
        return ','.join(res)

    def process_data(self, value):
        if value is None:
            self.data = None
        else:
            try:
                self.data = value
            except (ValueError, TypeError):
                self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = None
            else:
                try:
                    data_list = []
                    for value in valuelist:
                        realName = self.coerce(value)
                        u = User.query.filter_by(realName=realName).first()
                        data_list.append(u)
                    self.data = data_list
                except ValueError:
                    raise ValueError(self.gettext(u'Invalid Choice: could not coerce'))
        else:
            self.data = []

    def pre_validate(self, form):
        if self.allow_blank and self.data is None:
            return

        values = [d.realName for d in self.data]
        for v, _ in self.choices:
            if v[0] in values:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))
