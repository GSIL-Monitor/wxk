# coding: utf-8

from __future__ import unicode_literals


class BackendServiceError(ValueError):
    pass


class TokenNeedRefreshError(ValueError):
    # 发生该错误时，仅需重新刷新一次浏览器即可
    pass


class QiNiuServiceError(ValueError):
    pass
