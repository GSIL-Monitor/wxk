# coding: utf-8

from __future__ import unicode_literals
from os.path import dirname

from flask_babelex import Domain


class CustomDomain(Domain):
    def __init__(self):
        super(CustomDomain, self).__init__(dirname(__file__))


_domain = CustomDomain()

gettext = _domain.gettext
ngettext = _domain.ngettext
lazy_gettext = _domain.lazy_gettext
