# encoding: utf-8

from __future__ import unicode_literals

from flask_admin.form.upload import FileUploadInput
from flask import url_for
import json
from wtforms.widgets import HTMLString, html_params
from werkzeug.datastructures import FileStorage


class AccessoryFileuploadInput(FileUploadInput):

    empty_template_head = ('<div class="row">'
                           '<div class="col-md-4">'
                           '</div>'
                           '<div class="col-md-8">')

    empty_template_con = ('<span class="btn green fileinput-button">'
                          '<i class="fa fa-plus"></i>'
                          '<span>上传附件</span>'
                          '<input %(file)s onchange="$(\'#info\').html(this.files[0].name)">'
                          '</span>'
                          '<span class="label label-info" id="info"></span>')

    empty_template_tail = ('</div></div>')

    data_template_head = ('<div class="form-group">'
                          '<div class="col-md-4">'
                          '<a class="btn blue" target="_blank" %(a)s>'
                          '<div class="filename">%(file_name)s</div></a>'
                          '<input name="accessory-old" %(old)s type="hidden">'
                          '</div>'
                          '<div class="col-md-8">')
    data_template_tail = ('</div></div>')

    empty_template = empty_template_head + empty_template_con + empty_template_tail
    data_template = data_template_head + empty_template_con + data_template_tail

    def __call__(self, field, **kwargs):

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        key = ''

        file_name = ''

        old = {}
        old.setdefault('value', '')

        template = self.data_template if field.data else self.empty_template

        if field.errors:
            template = self.empty_template

        if field.data and isinstance(field.data, FileStorage):
            value = field.data.filename
        else:
            value = field.data or ''
            old['value'] = field.data
            if field.data:
                key = field.data.get('key')
                file_name = field.data.get('name')

        url = url_for('.download_view', key=key)

        a = {}
        a.setdefault('href', url)

        return HTMLString(template % {
            'file_name': file_name,
            'a': html_params(**a),
            'old': html_params(**old),
            'file': html_params(type='file',
                                value=value,
                                **kwargs),
        })


class MysqlFileuploadInput(FileUploadInput):

    empty_template_head = ('<div class="row">'
                           '<div class="col-md-4">'
                           '</div>'
                           '<div class="col-md-8">')

    empty_template_con = ('<span class="btn green fileinput-button">'
                          '<i class="fa fa-plus"></i>'
                          '<span>上传附件</span>'
                          '<input %(file)s onchange="$(\'#info\').html(this.files[0].name)">'
                          '</span>'
                          '<span class="label label-info" id="info"></span>')
    
    empty_template_tail = ('</div></div>')

    data_template_head = ('<div class="row">'
                          '<div class="col-md-4">'
                          '<a class="btn blue" target="_blank" %(a)s>'
                          '<div class="filename">%(file_name)s</div></a>'
                          '</div>'
                          '<div class="col-md-8">')

    data_template_tail = ('</div></div>')

    empty_template = empty_template_head + empty_template_con + empty_template_tail
    data_template = data_template_head + empty_template_con + data_template_tail

    def __call__(self, field, **kwargs):

        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        key = ''
        file_name = ''

        template = self.data_template if field.data else self.empty_template

        if field.errors:
            template = self.empty_template

        value = field.data or ''
        try:
            items = field.data.split(',')
            for item in items:
                k, v = item.split(':')
                if k == 'name':
                    file_name = v
                if k == 'key':
                    key = v
        except:
            value = ''

        a_dict = {}
        a_dict.setdefault('href', url_for('.download_view', key=key))

        return HTMLString(template % {
            'file_name': file_name,
            'a': html_params(**a_dict),
            'file': html_params(type='file',
                                value=value,
                                **kwargs),
        })


class MultiFileuploadInput(object):

    head = ('<input id="upload" name="filenumber" class="btn green fileinput-button" type="button" value="上传附件"/>'
            '<div class="row">'
            '<div class="col-md-8">'
            '<ul class="list-group">')

    tail = ('<li class="list-group-item filename1" style="display: none;">'
            '<span id="name1"></span>'
            '</li></ul></div>'
            '<div class="inputs">'
            '<input name="acce1" id="accefile1" type="file" style="display: none;" />'
            '</div>'
            '</div>')

    def __call__(self, field, **kwargs):
        if field.data and field.data not in (u'[]', '[]'):
            template = self.process_str(field)
        else:
            template = self.joinStr([self.head, self.tail])

        return HTMLString(template)

    def joinStr(self, str_list):
        return ''.join(str_list)

    def addLi(self, index, file_name, key):
        index = str(index)
        a_dict = {}
        a_dict.setdefault('href', url_for('.download_view', key=key))
        a_dict.setdefault('target', "_blank")

        a_item = '<a %(a)s>' % {'a': html_params(**a_dict)}
        liItem = self.joinStr(['<li class="list-group-item filename', index,
                               '"><span id="name',
                               index, '">', a_item, file_name,
                               '</a></span>',
                               '<span class="badge badge-danger">删除</span></li>'])
        return HTMLString(liItem)

    def addInput(self, index, value):
        index = str(index)
        return self.joinStr(['<input name="acce', index, '" id="accefile',
                             index, '" value=\'', value, '\' style="display: none;" />'])

    def emptyLi(self, index):
        index = str(index)
        return self.joinStr(['<li class="list-group-item filename', index,
                             '" style="display: none;"><span id="name',
                             index, '"></span></li>'])

    def savedList(self, str_obj):
        list_str = ''
        input_str = ''
        for i, file_dict in enumerate(json.loads(str_obj)):
            key = file_dict.get('key')
            name = file_dict.get('name')
            list_str = self.joinStr([list_str,
                                     self.addLi(i+1, name, key)])
            input_str = self.joinStr([input_str,
                                      self.addInput(i+1,
                                                    json.dumps(file_dict))])
            index = i + 2

        return self.joinStr([self.head, list_str, self.emptyLi(index),
                             '</ul></div><div class="inputs">',
                             input_str, self.emptyInput(index), '</div></div>'])

    def emptyInput(self, index):
        index = str(index)
        return self.joinStr(['<input name="acce', index, '" id="accefile',
                             index, '" type="file" style="display: none;" />'])

    def process_str(self, field):
        if field.data and isinstance(field.data, (str, unicode)):
            return self.savedList(field.data)

        if field.data and isinstance(field.data, (list)):
            if not field.object_data:
                return HTMLString(self.joinStr([self.head, self.tail]))
            else:
                return self.savedList(field.object_data)


class MxpMultiFileuploadInput(MultiFileuploadInput):

    def process_str(self, field):
        list_str = ''
        input_str = ''

        for i, file_str in enumerate(field.data):
            file_name = file_str.get('name')
            key = file_str.get('key')
            list_str = self.joinStr([list_str, self.addLi(i+1, file_name, key)])
            input_str = self.joinStr([input_str, self.addInput(i+1, json.dumps(file_str))])
            index = i + 2
        return self.joinStr([self.head, list_str, self.emptyLi(index),
                             '</ul></div><div class="inputs">',
                             input_str, self.emptyInput(index), '</div></div>'])
