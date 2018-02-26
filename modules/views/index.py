# encoding: utf-8

from __future__ import unicode_literals

from flask import redirect, url_for, request, abort, current_app
from flask_security import current_user, logout_user
from flask_admin import AdminIndexView, expose
import json

from modules.views.perms import models
from modules.flows.states import (
    REVIEWING, APPROVING, Sented, Receiving, SecApproving)
from modules.flows.operations import View
from modules.proxy import proxy
from modules.views.warning_level import warning_level, get_predict_level
from modules.helper import (
    get_aircraft_info, get_mx_item_info, can_view_aircraft)
from pending import pending_list
from util.jinja_filter import timestamp_to_date
from modules.perms import ActionNeedPermission
from modules.models.notification.announcement import Announcement


# 按到期日期排序为第一排序，预警等级为第二排序
def list_compare_max(x, y):
    if x['earliest'] > y['earliest']:
        return 1
    elif x['earliest'] < y['earliest']:
        return -1
    else:
        level_x = list(warning_level.keys())[list(
            warning_level.values()).index(x['level'])]
        level_y = list(warning_level.keys())[list(
            warning_level.values()).index(y['level'])]
        if level_x == 0:
            return 1
        elif level_y == 0:
            return -1
        elif level_x < level_y:
            return 1
        elif level_x > level_y:
            return -1
        return 0


# y5b 到期列表排序方法
def list_level_compare_max(x, y):
    level_x = list(warning_level.keys())[list(
        warning_level.values()).index(x['level'])]
    level_y = list(warning_level.keys())[list(
        warning_level.values()).index(y['level'])]
    if level_x == 0 and level_y != 0:
        return 1
    elif level_x != 0 and level_y == 0:
        return -1
    elif level_x < level_y:
        return -1
    elif level_x > level_y:
        return 1
    else:
        if get_higher_level_interval_type(x['intervaltype'])[0] >\
                get_higher_level_interval_type(y['intervaltype'])[0]:
            return -1
        elif get_higher_level_interval_type(x['intervaltype'])[0] <\
                get_higher_level_interval_type(y['intervaltype'])[0]:
            return 1
        else:
            if get_higher_level_interval_type(x['intervaltype'])[1] <\
                    get_higher_level_interval_type(y['intervaltype'])[1]:
                return -1
            else:
                return 1


# 飞行时间(0)、发动机时间(9)、架次(1)、日历时间(2,3,4) 从中获取其级别
# 上面的顺序为优先级降序 所以返回（4, left)(3, left),(2, left),(1, left）
# 来代表其的级别高低(4, left)为最高，依次降低left为剩余量
# 如果没有在这几种interval里面，为了用户体验返回一个不影响排序的值（0，0）
def get_higher_level_interval_type(interval_type):
    if 0 in interval_type.keys():
        return (4, interval_type[0])
    elif 9 in interval_type.keys():
        return (3, interval_type[9])
    elif 1 in interval_type.keys():
        return (2, interval_type[1])
    elif 2 in interval_type.keys():
        return (1, interval_type[2])
    elif 3 in interval_type.keys():
        return (1, interval_type[3])
    elif 4 in interval_type.keys():
        return (1, interval_type[4])
    else:
        return (0, 0)


class IndexView(AdminIndexView):

    @property
    def can_aircraft(self):
        perm = ActionNeedPermission(
            'aircraft', View)
        return perm.can()

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                logout_user()
                return abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

    def get_perms(self):

        duelist_perms = False
        airmaterial_perms = False

        return {
            'duelist_perms': duelist_perms,
            'airmaterial_perms': airmaterial_perms
        }

    def get_todo_list(self, max_count=None):
        return pending_list(models, max_count=max_count)

    def get_predict_items(self, max_count=None):
        # 下面的接口可以获得到期推算的内容
        resp = proxy.get('/v1/mxm/ptime/?ascend=1')
        if resp.status_code == 200:
            predict_items = resp.json()['items']
            if predict_items is None:
                return []
            show_list = []
            exist_plane = {}
            # 第一遍遍历
            for item in predict_items:
                timestamp = 0
                plane_id = item['planeId']
                if plane_id not in exist_plane:
                    exist_plane[plane_id] = get_aircraft_info(plane_id)
                plane_info = exist_plane[plane_id]
                mx_item = get_mx_item_info(plane_info['id'], plane_info['planeType'], item['boundedId'])
                if mx_item is None:
                    continue
                ret = {
                    'warningLevel': item['warningLevel'],
                    'err': item['itempredictTime']['errorMessage'],
                    'earliest': item['itempredictTime']['earlisetpredictTime'],
                    'best': item['itempredictTime']['bestpredictTime'],
                    'latest': item['itempredictTime']['latestpredictTime'],
                    'mxType': mx_item.mx_type,
                }

                interval_type = {}
                ret['intervalTimes'] = []
                for temp in item['intervalspredictTime']:
                    ori = {
                        'err': temp['errorMessage'],
                        'earliest': temp['earlisetpredictTime'],
                        'best': temp['bestpredictTime'],
                        'latest': temp['latestpredictTime'],
                        'left': temp['left'],
                        'type': temp['intervalType'],
                    }
                    ret['intervalTimes'].append(ori)
                    interval_type[temp['intervalType']] = temp['left']
                level = get_predict_level(ret)
                if item['itempredictTime']['earlisetpredictTime']:
                    timestamp = item['itempredictTime']['earlisetpredictTime']
                if timestamp == 0 and level == 0:
                    level = 4

                show_list.append({
                    'role': self.can_aircraft,
                    'id': str(plane_info['_id']),
                    'mxId': mx_item.id,
                    'mxType': mx_item.mx_type,
                    'description': mx_item.description,
                    'planeId': plane_info['id'],
                    'level': level,
                    'earliest': timestamp_to_date(timestamp),
                    'intervaltype': interval_type,
                })
            show_list.sort(list_level_compare_max)
            if max_count and isinstance(max_count, int):
                if len(show_list) <= max_count:
                    return show_list
                return show_list[:max_count]
            return show_list
        return []

    def get_anno_list(self, max_count=None):
        perm = ActionNeedPermission(Announcement.__name__.lower(), View)
        if perm.can():
            items = Announcement.query.filter_by(statusName=Sented).order_by('sendTime desc').limit(max_count).all()
        else:
            items = None
        return items

    def get_predict_items_from_redis(self, max_count=None):
        cache = current_app.redis_cache
        predict_items = cache._user_cache.get('warning')
        if not predict_items:
            return []
        predict_items = json.loads(predict_items)
        if max_count and isinstance(max_count, int):
            if len(predict_items) <= max_count:
                return predict_items
            return predict_items[:max_count]
        return predict_items

    @expose()
    def index(self):

        max_count = current_app.config.get('HOMEPAGE_MAX_COUNT', 6)

        self._template_args.update(self.get_perms())
        self._template_args.update({
            'todo_list': self.get_todo_list(max_count),
            'predicts': self.get_predict_items_from_redis(max_count),
            'anno_list': self.get_anno_list(max_count),
            'can_view_aircraft': can_view_aircraft(),
            'status_related_action': {
                # 状态应该对应的视图动作
                APPROVING: 'approve',
                REVIEWING: 'review',
                Receiving: 'receive',
                SecApproving: 'second_approved',

            },
        })
        return super(IndexView, self).index()
