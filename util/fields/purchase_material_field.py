# encoding: utf-8

from __future__ import unicode_literals

from wtforms.fields import StringField

from ..widgets.purchase_material_widget import PurchaseInputWidget


class PurchaseInputField(StringField):
    widget = PurchaseInputWidget()
