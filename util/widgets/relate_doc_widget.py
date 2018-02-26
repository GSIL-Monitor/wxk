# encoding: utf-8

from __future__ import unicode_literals
import json

from flask import url_for
from wtforms.widgets import HTMLString, html_params
import time


class RelateDocSelect:

    template = ('<a type="button" data-target="#rd_modal_window" class="btn blue" %(kwargs)s href="%(url)s&modal=True" data-toggle="modal">'
                '<i class="fa fa-plus">选择文档</i></a>'
                '%(show)s'
                "<input id='doc_files' type='hidden' name='doc_files' value='%(values)s'>")

    def __call__(self, field, **kwargs):

        show_head = ('<div id="doc_number"><div class="table-responsive">'
                     '<table class="table table-striped table-hover table-bordered">')
        show_tail = ('</table></div></div>')
        table_head = ('<tr><td>')
        table_tail = ('</tr></td>')

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        if field.data:
            show = show_head
            for file_obj in field.data:
                show += table_head
                name = file_obj.get('name')
                key = file_obj.get('key')
                aStr = '<a href=' + url_for('.download_view', key=key) + '>'
                show += aStr
                show += name
                show += '</a>'
                show += table_tail
            show += show_tail
            values = json.dumps(field.data)
        else:
            values = ""
            show = '<div id="doc_number"></div>'

        return HTMLString(self.template % {
            'url': url_for(".relate_doc_view", ts=time.time()),
            'kwargs': html_params(**kwargs),
            'values': values,
            'show': show,
        })
