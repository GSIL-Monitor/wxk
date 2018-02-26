# encoding: utf-8

from __future__ import unicode_literals

from flask import Flask
from flask_testing import TestCase

from util.api_request import WXKAPIProxy


# 测试配置
config = {
    'TESTING': True,
    'PLATFORM_API_BASE': 'http://dev.hf-it.org/platform',
    'WXK_ACCESS_ROLE': 'wxk-platform-access',
    'WXK_API_BASE': 'http://192.168.100.204',
    'WXK_USERNAME': 'zhongrui',
    'WXK_PASSWORD': 'zhongrui123',
}


class WXKAPIProxyTestCase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        self.app = app

        return app

    def setUp(self):
        self.proxy = WXKAPIProxy(config)
        self.url = '/v1/da40d/aircraft/'

    def test_all_verb(self):
        # 尝试新增一个飞机
        resp = self.proxy.create({
            'id': 'B-Test119',
            'planeType': 'da40d',
            'importedDate': 100000,
            'manufactureDate': 99999,
            'flightTime': 20,
            'landTimes': 10,
        }, url=self.url)

        resp_json = resp.json()
        assert 'etag' in resp_json
        assert resp_json['flightTime'] == 20

        resp = self.proxy.update({
            'id': 'B-Test119',
            'planeType': 'da40d',
            'flightTime': 30,
        }, etag=resp_json['etag'], url=self.url)

        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json['flightTime'] == 30

        resp_json = resp.json()
        resp = self.proxy.delete(
            url='/v1/aircraft/', etag=resp_json['etag'],
        )

        assert resp.status_code == 204
