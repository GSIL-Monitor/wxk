# encoding: utf-8
# 处理原维修客管理系统的飞行器信息

from __future__ import unicode_literals

from wtforms import form, fields
from flask_security import current_user

from util.fields import (
    DateTimeFieldInt, DateInt, RefreshAirportSelectField,
    RefreshFlyNatureSelectField, RefreshFormulaSelectField
)


class FlightLogForm(form.Form):

    id = fields.StringField('编号')
    aircraftId = fields.StringField('飞行器注册号')
    aircraftType = fields.HiddenField('机型信息', default='y5b')
    departureAirport = RefreshAirportSelectField('起飞机场')
    landingAirport = RefreshAirportSelectField('降落机场')
    flightDate = DateInt('飞行日期')
    captain = fields.StringField('正驾驶')
    copilot = fields.StringField('副驾驶')
    crew = fields.StringField('机组')
    passengers = fields.StringField('其他人员')
    departureTime = DateTimeFieldInt('起飞时间')
    landingTime = DateTimeFieldInt('着陆时间')
    landings = fields.IntegerField('起降次数')
    remark = fields.StringField('备注')
    etag = fields.HiddenField('etag')


class AS350FlightLogForm(FlightLogForm):
    tc = fields.FloatField('TC')
    ng = fields.FloatField('NG')
    nf = fields.FloatField('NF')


class Y5bForm(FlightLogForm):
    poweronTime = DateTimeFieldInt('开车时间')
    powerdownTime = DateTimeFieldInt('关车时间')
    stopTime = DateTimeFieldInt('停止时间')
    skidoffTime = DateTimeFieldInt('滑出时间')
    flightTime = fields.FloatField('飞行时间')
    missionType = fields.SelectField('任务性质', choices=[
        ('正常任务', '正常任务'),
        ('惯导任务', '惯导任务'),
    ])
    engineTime = fields.FloatField('发动机小时')
    flyProperty = RefreshFlyNatureSelectField('飞行性质')
    medicinePrescription = RefreshFormulaSelectField('药品配方')
    workArea = fields.StringField('作业区域')
    workAcres = fields.FloatField('作业亩数')
    formMaker = fields.HiddenField('制单人', default=current_user)
    formmakeTime = fields.HiddenField('制单时间')
    modifier = fields.HiddenField('修改人', default=current_user)
    modifyTime = fields.HiddenField('修改时间')
    # submitter = fields.StringField('提交人')
    # submitTime = DateTimeFieldInt('提交时间')
