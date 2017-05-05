# encoding: utf-8
# 处理原维修客管理系统的飞行器信息

from __future__ import unicode_literals

from wtforms import form, fields
# from flask_admin.model.fields import InlineFormField

from util.fields import DateField


class UtilizationForm(form.Form):
    """飞行器利用率的相关信息。"""
    hours = fields.FloatField('小时/月')
    times = fields.IntegerField('起落次数/月')


class AircraftInformationForm(form.Form):

    id = fields.StringField('飞行器注册号')
    # TODO: 这个应该是选择列表
    planeType = fields.StringField('机型')
    sn = fields.StringField('飞行器串号')
    # TODO: 如何将这些日期字段在存储时变更为整型数值
    importedDate = DateField('引进日期')
    manufacture = fields.StringField('制造商')
    acn = fields.StringField('适航证编号')
    sln = fields.StringField('电台执照编号')
    nrn = fields.StringField('国籍登记证编号')
    manufactureDate = DateField('执照日期')
    permanentAirport = fields.StringField('常驻机场')
    flightTime = fields.StringField('初始飞行时间')
    landTimes = fields.StringField('初始起落次数')
    remark = fields.StringField('备注')
    # boundedMxp = fields.StringField('绑定的机型维修方案')
    imageUrl = fields.StringField('飞机图片')
    # ad = fields.IntegerField('适航指令的预警数量')
    # sb = fields.IntegerField('服务通告的预警数量')
    # totalHours = fields.FloatField('总飞行时间信息')
    # totalTimes = fields.IntegerField('总起落次数信息')
    engineNumber = fields.StringField('发动机序号')
    acnDeadline = DateField('适航证编号到期时间')
    slnDeadline = DateField('国籍登记编号到期时间')
    nrnDeadline = DateField('电台执照编号到期时间')

    # utilInfo = InlineFormField(UtilizationForm, '利用率信息')
