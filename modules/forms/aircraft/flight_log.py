# encoding: utf-8
# 处理原维修客管理系统的飞行器信息

from __future__ import unicode_literals

from wtforms import form, fields

from util.fields import DateField


class FlightLogForm(form.Form):

    id = fields.StringField('编号')
    aircraftId = fields.StringField('飞行器注册号')
    departureAirport = fields.StringField('起飞机场')
    landingAirport = fields.StringField('降落机场')
    flightDate = DateField('飞行日期')
    captain = fields.StringField('机长')
    copilot = fields.StringField('副机长')
    crew = fields.StringField('机组')
    passengers = fields.StringField('乘客')
    departureTime = DateField('起飞时间')
    landingTime = DateField('降落时间')
    flightTime = DateField('飞行时间')
    landings = fields.IntegerField('起落/循环次数')
    remark = fields.StringField('备注')
    logTime = DateField('日志录入时间')
    aircraftType = fields.StringField('机型信息')
