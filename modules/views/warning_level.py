# coding: utf-8

from __future__ import unicode_literals
import json

from jinja2 import Markup
from flask import current_app

from modules.models.basic_data.early_warning import EarlyWarning


warning_level = {
    -1: Markup('严重超时'),
    0: Markup('正常'),
    1: Markup('3级预警'),
    2: Markup('2级预警'),
    3: Markup('1级预警'),
    4: Markup('未知'),
}


def get_relate_type_cfg(interval_type, mx_type):
    return get_fixed_relate_type_cfg(interval_type, mx_type) or\
        get_relate_cfg_from_redis(interval_type)


def get_relate_cfg_from_redis(interval_type):
    cache = current_app.redis_cache

    predicts_cfg = getattr(current_app, 'predicts_cfg,', None)
    if predicts_cfg is None:
        predicts_cfg = cache.get(EarlyWarning.key)
        if not predicts_cfg:
            # 使用默认的
            return None
        # 直接放到进程里，减少更新
        predicts_cfg = current_app.predicts_cfg = json.loads(predicts_cfg)
    related_type_cfg = predicts_cfg.get(str(interval_type))
    if related_type_cfg is None:
        return None
    l1, l2, l3 = related_type_cfg.get('lv1'), related_type_cfg.get(
        'lv2'), related_type_cfg.get('lv3')
    return (l1, l2, l3)


def get_fixed_relate_type_cfg(interval_type, mx_type):
    if mx_type == 'scheduled' and (interval_type in [0, 9]):
        return (20, 10, 5)
    elif mx_type == 'scheduled' and (interval_type in [2, 3, 4]):
        return(90, 60, 30)
    else:
        return None


def get_predict_level(predict_info, name='warningLevel', cfg_getter=get_relate_type_cfg):
    level = predict_info[name]

    if level == -1:
        return warning_level[level]

    def get_user_defined_level():
        basic_level = 0
        for interval in predict_info['intervalTimes']:
            # 如果有错，以传来的数据为主
            if interval['err'] != '':
                return 4

            left = interval['left']
            relate_type_cfg = cfg_getter(
                interval['type'], predict_info['mxType'])
            if relate_type_cfg is None:
                return None
            l1, l2, l3 = relate_type_cfg[0],\
                relate_type_cfg[1], relate_type_cfg[2]
            # 判断区间, 注意，返回的数字，与实际的等级是反的
            # 这里要返回 1，2，3中最小的一个，为0返回0
            if left > l1:
                # 超过1级预警的剩余量，提示正常
                basic_level = max(basic_level, 0)
            elif 0 == basic_level:
                basic_level = 3
            if left <= l1 and left > l2:
                basic_level = min(basic_level, 3)
            elif left <= l2 and left > l3:
                basic_level = min(basic_level, 2)
            elif left <= l3:
                basic_level = min(basic_level, 1)

        return basic_level

    level = get_user_defined_level()
    if level is not None:
        return warning_level[level]

    level = predict_info[name]
    # 有预警直接显示默认预警
    if level != 0:
        return warning_level[level]

    for interval in predict_info['intervalTimes']:
        if interval['err'] != '':
            break
        else:
            # 如果为0，且对应的具体类别中没有错误，就是正常
            return warning_level[0]

    return warning_level[4]
