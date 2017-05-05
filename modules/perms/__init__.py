# coding: utf-8

from __future__ import unicode_literals

from collections import namedtuple

from flask_principal import Permission


"""该模块定义了通用的权限设置。"""

# 注意，该ActionNeed和默认的Flask-Principal所提供的ActionNeed语义不同
ActionNeed = namedtuple('ActionNeed', ['model', 'action'])
"""对于该应用的多数细粒度权限，使用该ActionNeed来标识。\
`model`为模型的名称，`action`为对应的操作。`action`通常为增删改查等，此外还可能包含\
有关流程操作的内容。"""


class ActionNeedPermission(Permission):

    def __init__(self, model, action):
        need = ActionNeed(model, action)
        super(ActionNeedPermission, self).__init__(need)


def _on_identity_loaded(sender, identity):
    # 当用户加载后，需要根据用户角色中配置的操作来初始化其权限上下文
    for role in identity.user.roles:
        # 把不同模型允许的操作开关项相应地设置进去
        for action in role.actions:
            for attr in dir(action):
                if getattr(action, attr, False):
                    identity.provides.add(ActionNeed(action.model, attr))
