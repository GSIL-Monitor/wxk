# encoding: utf-8

from __future__ import unicode_literals

from wtforms.widgets import HTMLString


class InputSelectWidget(object):

    template = """
      <div class="row">
        <div class="col-md-4">
           <input type="text"
           name="%(name)s-value" value="%(value)s"
           class="form-control">
        </div>
        <div class="col-md-4">
          <select class="form-control"
          name="%(name)s-type" for="%(type)s">
            <option value="天">天</option>
            <option value="小时">小时</option>
            <option value="年">年</option>
            <option value="月">月</option>
          </select>

        </div>
      </div>
      """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        placeholder = ''
        data = ['', '']
        selected = ''
        if field.data:
            for item in ['天', '小时', '年', '月']:
                if field.data.endswith(item):
                    data = field.data.split(item)
                    data[1] = item
                    break

        placeholder = self.template % {
            'name': field.name,
            'value': str(data[0]),
            'type': data[1],
            'selected': selected
        }

        return HTMLString(placeholder)
