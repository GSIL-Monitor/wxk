# coding: utf-8

from __future__ import unicode_literals

from .base import db


class FlowMixin(object):

    @property
    def business_id(self):
        raise NotImplementedError()
