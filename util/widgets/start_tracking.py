# encoding: utf-8

from __future__ import unicode_literals

from wtforms.widgets import HTMLString


class BasicStartTracking:
    template = """
    <div id=%(id)s>
      <div class="row">
        <div class="col-md-1">
          <input class="form-control radio-group"
          type="radio" id="%(id)s" name="startTracking">
        </div>
        <div class="col-md-4">
          <input type="text" name="%(name)s-value"
          disabled="disabled" value="%(value)s"
          class="form-control" placeholder="%(place)s">
        </div>
      </div>
    </div>
    """

    def init_template(self, field):
        if field.short_name == 'time':
            place = '小时'
        elif field.short_name == 'count':
            place = '次'
        else:
            place = ''
        try:
            value = field.data.get('value')
        except:
            value = ''
        radio = {'id': field.name,
                 'name': field.name,
                 'value': value,
                 'place': place}
        return self.template % radio

    def __call__(self, field, **kwargs):
        return HTMLString(self.init_template(field))


class SpecialStartTracking(BasicStartTracking):
    template = """
    <div id="%(id)s">
      <div class="row">
        <div class="col-md-1">
          <input class="form-control radio-group"
          type="radio" id="%(id)s" name="startTracking">
        </div>
        <div class="col-md-4">
          <input type="text" name="%(name)s-value"
          disabled="disabled" value="%(value)s" class="form-control">
        </div>
        <div class="col-md-2">
          <select class="form-control" name="%(name)s-type"
          disabled="disabled" value="%(type)s">
            <option selected="selected"value="4">年</option>
            <option value="3">月</option>
            <option value="2">日</option>
          </select>
        </div>
      </div>
    </div>
    """

    def init_template(self, field):
        keys = ('value', 'type')
        values = {}
        for key in keys:
            try:
                values[key] = field.data.get(key)
            except:
                values[key] = ''
        radio = {'id': field.name,
                 'name': field.name}
        radio.update(values)
        return self.template % radio
