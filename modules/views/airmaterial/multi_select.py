# coding: utf-8

from __future__ import unicode_literals

from flask_admin import expose
from flask import redirect, request
from functools import partial
from modules.views import CustomView
from modules.models.airmaterial import (PurchaseApplication, LendApplication,
                                        LoanApplicationOrder,
                                        RepairApplication,
                                        BorrowingInReturnModel,
                                        AssembleApplication,
                                        Scrap)
from modules.flows.operations import Create
from modules.perms import ActionNeedPermission


class MultiSelectView(CustomView):

    type_url = {}

    @property
    def can_purchase(self):
        perm = ActionNeedPermission(
            PurchaseApplication.__name__.lower(), Create)
        return perm.can()

    @property
    def can_lend(self):
        perm = ActionNeedPermission(
            LendApplication.__name__.lower(), Create)
        return perm.can()

    @property
    def can_loan(self):
        perm = ActionNeedPermission(
            LoanApplicationOrder.__name__.lower(), Create)
        return perm.can()

    @property
    def can_assemble(self):
        perm = ActionNeedPermission(
            AssembleApplication.__name__.lower(), Create)
        return perm.can()

    @property
    def can_scrap(self):
        perm = ActionNeedPermission(Scrap.__name__.lower(), Create)
        return perm.can()

    @property
    def can_repair(self):
        perm = ActionNeedPermission(
            RepairApplication.__name__.lower(), Create)
        return perm.can()

    @property
    def can_borrowing_return(self):
        perm = ActionNeedPermission(
            BorrowingInReturnModel.__name__.lower(), Create)
        return perm.can()

    @expose('/multi_checkbox_redirect/', methods=['POST'])
    def multi_checkbox_redirect(self):
        types = self.type_url.get(request.form.get('type'))
        rowid = request.form.get('rowids[]')
        return_url = self.get_url(types)
        if types and rowid:
            rowid = rowid.split(',')
            return_url = partial(self.get_url, types, rowid=rowid)()
            if 'stockwarning' in request.args.get('url'):
                return_url = partial(self.get_url, types, aoid=rowid)()
        return redirect(return_url)
