# encoding: utf-8

from __future__ import unicode_literals

from wtforms import fields
try:
    from wtforms.fields.core import _unset_value as unset_value
except ImportError:
    from wtforms.utils import unset_value

from tonghangyun_common.models.model import Address
from ..widgets.address import AddressInput


class AddressField(fields.Field):
    """
       Address 相关的Field
    """
    widget = AddressInput()

    def __init__(self, label=None, validators=None, **kwargs):
        super(AddressField, self).__init__(label, validators, **kwargs)

        self._province = self._city = self._county = self._detail = unset_value

    def process(self, formdata, data=unset_value):
        if formdata:
            province, city, county, detail = (
                '%s-province' % self.name, '%s-city' % self.name,
                '%s-county' % self.name, '%s-detail' % self.name
            )

            if province in formdata:
                self._province = formdata[province]

            if city in formdata:
                self._city = formdata[city]

            if county in formdata:
                self._county = formdata[county]

            if detail in formdata:
                self._detail = formdata[detail]

        return super(AddressField, self).process(formdata, data)

    def populate_obj(self, obj, name):
        # 存储数据库的时候，会掉用该方法

        self.data = Address(
            province=self._province,
            city=self._city,
            county=self._county,
            detail=self._detail)

        return super(AddressField, self).populate_obj(obj, name)
