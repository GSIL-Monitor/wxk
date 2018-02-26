# coding: utf-8

from __future__ import unicode_literals

from flask_admin import expose
from modules.views import CustomView
from .inline_table import InlineTable
from modules.models.airmaterial import Manufacturer


class WithInlineTableView(InlineTable, CustomView):

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/bootstrap-select.min.js',
        '/static/js/jquery.multi-select.js',
        '/static/js/components-dropdowns.js',
        '/static/js/select_planeType.js',
        '/static/js/inline_table.js',
        '/static/js/numbro.js',
        '/static/js/languages.js',
        '/static/js/zh-CN.min.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/moment.min.js',
        '/static/js/pikaday.js',
        '/static/js/pikaday-zh.js',
        '/static/js/upload_file.js',
    ]

    extra_css = [
        '/static/css/datepicker.css',
        '/static/css/bootstrap-datetimepicker.min.css',
        '/static/css/jquery-ui.css',
        '/static/css/pikaday.css',
        '/static/css/dateHeight.css',
    ]

    inline_model = None
    inline_column = None

    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        self._template_args.update({
            'table_columns': self.init_table_columns(),
        })

        return super(WithInlineTableView, self).approve_edit_view()

    def before_edit_form(self, model):
        self._template_args.update({
            'table_datas': self.get_table_data_from_db(model),
        })

    @expose('/details/')
    def details_view(self):

        self._template_args.update({
            'table_columns': self.get_readonly_table(),
            'table_datas': self.get_table_data_from_db(),
            'extra_table_js': 'js/inline_table_details.js'
        })

        return super(WithInlineTableView, self).details_view()

    @expose('/action-view/', methods=['POST', 'GET'])
    def action_view(self):
        self._template_args.update({
            'table_columns': self.get_readonly_table(),
            'table_datas': self.get_table_data_from_db(),
            'extra_table_js': 'js/inline_table_details.js'
        })
        return super(WithInlineTableView, self).action_view()

    def get_manafacturers(self):
        # 获取生产厂商
        return [m.name for m in Manufacturer.query.all()]

    @staticmethod
    def get_extra_js():
        return [
            '/static/js/inline_table.js',
            '/static/js/numbro.js',
            '/static/js/languages.js',
            '/static/js/zh-CN.min.js',
            '/static/js/jquery.validate.min.js',
            '/static/js/moment.min.js',
            '/static/js/pikaday.js',
            '/static/js/pikaday-zh.js',
        ]



