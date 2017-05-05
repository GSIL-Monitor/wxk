# coding: utf-8

from __future__ import unicode_literals

from flask_admin.model import InlineFormAdmin

from util.fields.on_off import OnOffField


class ActionsInlineForm(InlineFormAdmin):

    form_choices = {
        'model': [
            ('user', '用户'),
            ('role', '角色'),
            ('airworthiness', '适航文件'),
            ('mxp', '維修方案'),
            ('aircraft', '机队'),
        ]
    }

    form_overrides = {
        'create': OnOffField,
        'edit': OnOffField,
        'view': OnOffField,
        'delete': OnOffField,
        'submit_review': OnOffField,
        'review_approve': OnOffField,
        'review_refuse': OnOffField,
        'review_again': OnOffField,
        'approved': OnOffField,
        'approve_refuse': OnOffField,
        'approve_again': OnOffField,
        'cancel': OnOffField,
        'submit_approve': OnOffField,
    }

    @property
    def column_labels(self):
        basic = {
            'model': '关联模型',
            'create': '新建',
            'edit': '编辑',
            'view': '查看',
            'delete': '删除',
        }

        if not self._support_flow:
            return basic

        basic.update({
            'submit_review': '提交复核',
            'review_approve': '复核确认',
            'review_refuse': '复核拒绝',
            'review_again': '提交再次复核',
            'approved': '批准确认',
            'approve_refuse': '批准拒绝',
            'approve_again': '提交再付批准',
            'cancel': '撤销',
            'submit_approve': '提交审批',
        })

        return basic

    @property
    def form_columns(self):
        basic = ['id', 'model', 'create', 'edit', 'view', 'delete']

        if not self._support_flow:
            return basic

        basic.extend(['submit_review', 'review_approve', 'review_refuse',
                      'review_again', 'submit_approve', 'approved',
                      'approve_again', 'approve_refuse', 'cancel',
                      ])

    def __init__(self, model, support_flow=False, **kwargs):
        self._support_flow = support_flow
        super(ActionsInlineForm, self).__init__(model, **kwargs)
