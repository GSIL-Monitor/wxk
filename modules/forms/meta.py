# coding: utf-8

from __future__ import unicode_literals


def scheduled_source(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string.')

    basic = [
        ('AMM', 'AMM'),
        ('AD/SB', 'AD/SB'),
        ('EMM', 'EMM'),
        ('其他', '其他')]

    plane_type = plane_type.lower()
    if plane_type in ['as350']:
        basic.insert(-2, ('ALS', 'ALS'))
    elif plane_type in ['bell206', 'bell407', 'bell429']:
        basic = [
            ('MM', 'MM'),
            ('OMM', 'OMM'),
            ('MMS', 'MMS'),
            ('CD', 'CD'),
            ('AD/SB', 'AD/SB'),
            ('其他', '其他')]
    elif plane_type in ['da40d', 'r22', 'r44', 'swz269c1']:
        pass
    else:
        raise ValueError('please check the plane type')
    return basic


def environment_category(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string.')

    basic = [('正常环境', '正常环境'),
             ('热带及潮湿环境', '热带及潮湿环境'),
             ('盐雾环境', '盐雾环境'),
             ('沙尘和/或灰尘环境', '沙尘和/或灰尘环境'),
             ('寒冰或极寒天气', '寒冰或极寒天气')]

    if plane_type in ['as350']:
        pass
    else:
        raise ValueError('please check the plane type')

    return basic


def parking_category(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string')

    basic = [('<1个月', '<1个月'), ('1~6个月', '1~6个月'), ('>6个月', '>6个月')]

    if plane_type in ['as350']:
        pass
    else:
        raise ValueError('please check the plane type')

    return basic


def unscheduled_category(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string')
    basic = [('发动机', '发动机'), ('机体', '机体')]

    if plane_type in ['as350']:
        pass
    elif plane_type in ['bell206', 'bell407', 'bell429']:
        basic = [
            ('重着陆', '重着陆'),
            ('发动机停车或运转时，主旋翼突然停转', '发动机停车或运转时，主旋翼突然停转'),
            ('发动机停车或运转时，尾桨突然停转', '发动机停车或运转时，尾桨突然停转'),
            ('主旋翼超速', '主旋翼超速'),
            ('超扭矩', '超扭矩'),
            ('压气机失速或喘振', '压气机失速或喘振'),
            ('雷击后', '雷击后')]
    elif plane_type in ['da40d']:
        basic = [('重着陆', '重着陆'), ('螺旋桨撞击', '螺旋桨撞击'),
                 ('发动机失火', '发动机失火'), ('雷击', '雷击'), ('其他', '其他')]
    else:
        raise ValueError('please check the plane type')

    return basic


def flight_line_category(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string')

    basic = [('航前检查', '航前检查'),
             ('航后检查', '航后检查'),
             ('短停检查', '短停检查')]

    if plane_type in ['as350', 'bell206', 'bell407', 'bell429']:
        pass
    elif plane_type in ['da40d']:
        basic.remove(('短停检查', '短停检查'))
        basic.append(('过站检查', '过站检查'))
    else:
        raise ValueError('please check the plane type')

    return basic


def normal_check_category(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string')

    basic = [('航前检查', '航前检查'),
             ('视情检查', '视情检查'), ('航后检查', '航后检查')]

    if plane_type in ['r22', 'r44', 'swz269c1']:
        pass
    else:
        raise ValueError('please check the plane type')

    return basic


def special_check_category(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string')

    basic = [('尾撬检查', '尾撬检查'),
             ('尾桨撞击', '尾桨撞击'), ('旋翼检查', '旋翼检查'),
             ('发动机超速', '旋翼/发动机超速'), ('硬着陆', '硬着陆'),
             ('C020上钢管机架检查', 'C020上钢,管机架检查'),
             ('挡风玻璃检查', '挡风玻璃检查'),
             ('上、下离合器制动器轴承检查', '上、下离合器制动器轴承检查'),
             ('C181下制动器轴承检查', 'C181下制动器轴承检查'),
             ('C184上制动器轴承检查', 'C184上制动器轴承检查'),
             ('三角皮带检查', '三角皮带检查'),
             ('下皮带轮三角皮带磨损形式检查', '下皮带轮三角皮带磨损形式检查')]

    if plane_type in ['r22', 'r44', 'swz269c1']:
        pass
    else:
        raise ValueError('please check the plane type')

    return basic


def scheduled_area(plane_type=None):
    if not isinstance(plane_type.encode('utf-8'), str):
        raise ValueError('plane type should be string')

    basic = [('发动机舱', '发动机舱'),
             ('前机身', '前机身'), ('驾驶舱', '驾驶舱'), ('中部机身', '中部机身'),
             ('后机身', '后机身'), ('尾部', '尾部'), ('大翼', '大翼'), ('总检', '总检')]

    if plane_type in ['da40d']:
        pass
    else:
        raise ValueError('please check the plane type')

    return basic
