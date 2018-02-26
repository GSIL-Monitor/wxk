# coding: utf-8

from __future__ import unicode_literals

from tonghangyun_common import init_cache


class CacheProxy(object):

    def __init__(self, app):
        self._app = app
        self._user_cache = init_cache(app.config['REDIS_HOST'], app.config['REDIS_PORT'], app.config['REDIS_USER_DBID'])

    def _unique_key_in_cache(self):
        # 为redis缓存统一设置key的入口
        return '/'.join(['wxk', self._app.config['WXK_GROUP'], self._app.config['WXK_USERNAME']])

    def set(self, key, value, expiration=None):
        # 在缓存中设置数据
        self._user_cache.hmset(self._unique_key_in_cache(), {key: value})
        # TODO: EXPIRATION 现在不起作用

    def get(self, key):
        # 从缓存中获取数据
        return self._user_cache.hmget(self._unique_key_in_cache(), key)[0]
