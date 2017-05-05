# encoding: utf-8

from __future__ import unicode_literals

from wtforms.widgets import HTMLString


class BasicIntervalInput(object):
    "间隔类型的通用显示界面"

    template = """
    <div id="%(id)s">
    <div class="row">
      <div class="col-md-1">
        <div class="checkbox">
          <div class="checker">
            <span class=""><input type="%(check_or_radio)s" name='%(name)s' class="check-group"></span>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="input-icon">
           <i class="fa fa-sliders"></i>
           <input type="text" disabled="disabled" name="%(name)s-value" value="%(value)s" class="form-control" placeholder="基准">
        </div>
      </div>

      <div class="col-md-3">
        <div class="input-icon">
           <i class="fa fa-minus"></i>
           <input type="text" disabled="disabled" name="%(name)s-min" value="%(min)s" class="form-control" placeholder="下限">
        </div>
      </div>
      <div class="col-md-3">
        <div class="input-icon">
           <i class="fa fa-plus"></i>
           <input type="text" disabled="disabled" name="%(name)s-max" value="%(max)s" class="form-control" placeholder="上限">
        </div>
      </div>

    </div>
    </div>
    """

    def __init__(self, checkbox=True, *args, **kwargs):
        """初始化该实例

        :args multiple: 是否允许多个间隔的选择
        """
        self._check = checkbox

    def init_template(self, field, keys):
        values = {}
        for key in keys:
            try:
                values[key] = field.data.get(key)
            except:
                values[key] = ''

        checkbox_or_radio = {'check_or_radio': 'checkbox' if self._check else 'radio',
                             'label': field.label, 'name': field.name, 'id': field.name}

        checkbox_or_radio.update(values)

        return self.template % checkbox_or_radio

    def __call__(self, field, **kwargs):

        kwargs.setdefault('id', field.id)
        keys = ['value', 'max', 'min']

        return HTMLString(self.init_template(field, keys))


class SpecialIntervalInput(BasicIntervalInput):
    template = """
    <div id="%(id)s">
      <div class="row">

        <div class="col-md-1">
          <div class="checkbox">
            <div class="checker">
              <span class=""><input type="%(check_or_radio)s" name='%(name)s' class="check-group"></span>
            </div>
          </div>
        </div>

        <div class="col-md-3">
            <div class="input-icon">
                 <i class="fa fa-sliders"></i>
                 <input type="text" disabled="disabled" name="%(name)s-value" class="form-control" placeholder="基准" value="%(value)s">
            </div>
        </div>

        <div class="col-md-2">
          <select class="form-control" disabled="disabled" name="%(name)s-type" value="%(type)s">
            <option value="4">年</option>
            <option value="3">月</option>
            <option value="2">日</option>
          </select>
        </div>

        <div class="col-md-2">
          <div class="input-icon">
             <i class="fa fa-minus"></i>
             <input type="text" disabled="disabled" name="%(name)s-min" class="form-control" placeholder="下限" value="%(min)s">
          </div>
        </div>

        <div class="col-md-2">
          <div class="input-icon">
             <i class="fa fa-plus"></i>
             <input type="text" disabled="disabled" name="%(name)s-max" class="form-control" placeholder="上限" value="%(max)s">
          </div>
        </div>

        <div class="col-md-2">
          <select class="form-control" disabled="disabled" name="%(name)s-offsetType" value="%(offsetType)s">
            <option value="4">年</option>
            <option value="3">月</option>
            <option value="2">日</option>
          </select>
        </div>
      </div>
      </div>
      """

    def __call__(self, field, **kwargs):

        kwargs.setdefault('id', field.id)
        keys = ['value', 'max', 'min', 'type', 'offsetType']

        return HTMLString(self.init_template(field, keys))
