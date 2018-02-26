# coding: utf-8

from __future__ import unicode_literals

from flask_security import current_user

from modules.flows.operations import all_actions


class Mixin(object):

    view_accept_roles = None

    def is_accessible(self):

        if not current_user.is_active or not current_user.is_authenticated:
            return False

        # 简化权限对应视图的可视逻辑
        # 即，只要用户拥有对应模型的操作（即有操作为True的情形），就可见
        # 否则不可见。这样一来，角色和视图间没有必然联系

        # 如果有配置级的权限和视图可视设置，优先级要高
        if self.__class__.view_accept_roles is not None:
            view_name = self._get_view_name()
            allowed_roles = self.__class__.view_accept_roles.get(view_name)
            if allowed_roles:
                for role in allowed_roles:
                    if current_user.has_role(role):
                        return True

        # 由于管理员可能在不同的角色里配置相同视图的不同操作，所以这里使用列表
        model_name = self._get_model_name()
        relevant_action = []
        for role in current_user.roles:
            actions = role.actions
            for configed_action in actions:
                if configed_action.model == model_name:
                    relevant_action.append(configed_action)

        # 虽然配置了当前视图，我们仍要判断对该视图是否有可执行的操作
        for action in relevant_action:
            for verb_name in all_actions:
                if getattr(action, verb_name, False):
                    return True

        return False

    def _get_view_name(self):
        return self.name

    def _get_model_name(self):
        return self.model.__name__.lower()
