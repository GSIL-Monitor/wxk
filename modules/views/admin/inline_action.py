# coding: utf-8

from __future__ import unicode_literals

from flask_admin.model import InlineFormAdmin

from modules.flows import all_actions
from util.fields.on_off import OnOffField
from .column_labels import all_labels
from ..perms import models


class ActionsInlineForm(InlineFormAdmin):

    form_choices = {
        'model': [(item[0], item[1]) for item in models]
    }

    form_overrides = dict([(action, OnOffField) for action in all_actions])

    @property
    def column_labels(self):
        return all_labels

    @property
    def form_columns(self):
        basic = ['id', 'model', 'create', 'edit', 'view', 'delete']

        if not self._support_flow:
            return basic

        basic.extend(['submit_review', 'review_approve', 'review_refuse',
                      'review_again', 'approved', 'second_approved',
                      'edit_bound_status', 'remove_bound_status', 'approve_refuse', 'cancel',
                      'finish', 'second_approve_refuse'
                      ])

    def __init__(self, model, support_flow=False, **kwargs):
        self._support_flow = support_flow
        super(ActionsInlineForm, self).__init__(model, **kwargs)
