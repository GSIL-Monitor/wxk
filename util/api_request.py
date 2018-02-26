# encoding: utf-8

from __future__ import unicode_literals
from functools import partial

import requests

from .exception import BackendServiceError, TokenNeedRefreshError
from .cache import CacheProxy


def update_token(config, user_cache, username, password):
    # 不论怎样，直接获取新token
    base_url = config['PLATFORM_API_BASE']
    auth_url = base_url + '/auth'
    resp = requests.post(auth_url, json=dict(login=username, password=password))

    if resp.status_code != 200:
        raise BackendServiceError('The configured credenthial is not correct.')

    data = resp.json()
    user_cache.set("api_token", data['accessToken'])
    # 返回值为是否支持该访问权限
    return config['WXK_ACCESS_ROLE'] in data['roles']


def check_token_wrapper(config, user_cache, username, password, url, f, *args, **kwargs):
    """wrapper实现，封装真正调用所需的token"""

    token = user_cache.get("api_token")
    base_url = config['PLATFORM_API_BASE']
    wxk_api_url = config['WXK_API_BASE']

    def check_role():
        # 如果token为None且没有对应权限
        if token is None:
            if not update_token(config, user_cache, username, password):
                raise BackendServiceError('Configured credenthial has no rights to access wxk platform.')
            return True

        # TODO: 如果有更好的认证解决方案后，可以不用每次检查权限，原因如下
        # 现在之所以不用，是因为目前的认证实现有问题，当设置的超时过后，这里保存的token
        # 将会出错，虽然逻辑上还是正确的token

        # WUJG: 正常情况下，这里的return是不应该使用，而是使用下面注释掉的代码
        # 这样，可以避免在某些情况下，由于通航云管理平台授权发生变化而可以及时检测到，但由于
        # 所担心的情形可能性极小，所以直接忽略了；另一个原因，由于目前开发和测试平台配置的
        # 平台API使用了自定义的域名（hf-it.org），访问速度很慢，使用下面的语句会导致加载极慢，
        # 部署到产品级环境会好很多？
        # return True

        # 检查token对应的用户是否有权限
        role_url = base_url + '/has-role?type=%s' % (config[
            'WXK_ACCESS_ROLE'],)
        resp = requests.get(role_url, headers={
            'Authorization': 'JWT %s' % (token,)
        })
        if resp.status_code == 200:
            return True
        # 可能因为失效引起，继续认证
        if resp.status_code == 401:
            return update_token(config, user_cache, username, password)

        # 其他错误的话，我们认为有问题
        return False

    if not check_role():
        raise BackendServiceError('You dont have the rights to do so.')

    if token is None:
        token = user_cache.get('api_token')

    # 包装的函数，需要token信息
    return f(wxk_api_url + url, {
        'Authorization': 'JWT %s' % (token,)
    }, *args, **kwargs)


class WXKAPIProxy:
    "符合维修REST API特定调用要求的代理实现。"

    def __init__(self, config=None, base_url=None):
        if config is not None:
            self.config = config
            self.username = config['WXK_USERNAME']
            self.password = config['WXK_PASSWORD']

    def init_app(self, flask_app):
        "提供与Flask相兼容的实现"

        self.config = flask_app.config
        self.user_cache = CacheProxy(flask_app)
        self.username = self.config['WXK_USERNAME']
        self.password = self.config['WXK_PASSWORD']

        return self.user_cache

    def _rest_api_verb(self, verb, url, json_data=None, etag=None):

        # 目前仅支持下面的动作
        allowed_method = dict(
            get=requests.get,
            post=requests.post,
            update=requests.put,
            delete=requests.delete,
        )

        def wrapper(url, headers, *args, **kwargs):

            def get_resp(headers):
                if etag:
                    headers = headers.copy()
                    headers.update({
                        'If-Match': etag,
                    })

                rsp = allowed_method[verb](
                    url=url,
                    headers=headers,
                    json=json_data
                )
                return rsp

            resp = get_resp(headers)

            if resp.status_code == 401:
                if update_token(self.config, self.user_cache, self.username, self.password):
                    resp = get_resp(headers)
                if resp.status_code == 401:
                    raise TokenNeedRefreshError('Just need to refresh the web browser.')

            if resp.status_code == 404:
                raise BackendServiceError('The request url is not correct.')

            if resp.status_code in [503, 500, 502, 504]:
                raise BackendServiceError('The wxk platform api may not be started.')

            if resp.status_code not in [200, 201, 204]:
                resp_json = resp.json()
                if 'message' in resp_json:
                    raise BackendServiceError(resp_json['message'])
                raise BackendServiceError(resp_json['error'])

            return resp


        return partial(check_token_wrapper,
                       self.config,
                       self.user_cache,
                       self.username,
                       self.password,
                       url,
                       wrapper)()

    def create(self, json_data, url):
        return self._rest_api_verb('post', url, json_data)

    def update(self, data, etag, url):
        return self._rest_api_verb('update', url, data, etag)

    def delete(self, etag, url):
        return self._rest_api_verb('delete', url=url, etag=etag)

    def delete_with_data(self, data, url, etag):
        return self._rest_api_verb('delete', url, data, etag)

    def get(self, url):
        return self._rest_api_verb('get', url=url)
