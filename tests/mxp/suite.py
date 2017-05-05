# encoding: utf-8

from __future__ import unicode_literals

import os

from flask import url_for
import unittest
from bs4 import BeautifulSoup

# from app import app
from local_admin import create_app, mongodb, mysqldb
from modules.models import user_datastore
from modules.roles import (init_builtin_roles, super_admin, Role,
                           FlightManager, MaintenanceVicePresident)


os.environ['THY_SETTINGS'] = ''


class MxpTestCase(unittest.TestCase):

    def init_db(self):
        mysqldb.drop_all()
        mysqldb.create_all()
        roles = init_builtin_roles()
        mysqldb.session.add_all(roles)
        user_datastore.create_user(
            email='admin@hfga.com.cn',
            password='hfgahfga%',
            roles=[super_admin(mysqldb.session),
                   Role(name=FlightManager, description='机务部经理'),
                   Role(name=MaintenanceVicePresident, description='维修副总')]
        )
        mysqldb.session.commit()

    def setUp(self):
        self.app = create_app()
        self.app.config['SERVER_NAME'] = 'localhost'
        self.app.config['DEBUG'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        # with self.app_context:
        #     self.init_db()
        self.mongodb = mongodb
        # self.mongodb = self.app.mongodb
        self.app_context.push()

        self.coll = []
        self.login()

    def tearDown(self):
        self._clean_resource()
        # mysqldb.drop_all()
        self.app_context.pop()

    def _get_coll_name(self, view):
        coll_name = view.keywords.get('coll_name')
        return coll_name

    def _get_url(self, view):
        coll_name = self._get_coll_name(view)
        return '{}view'.format(coll_name)

    def _get_create_url(self, view):
        return '{}.create_view'.format(self._get_url(view))

    def _get_edit_url(self, view):
        return '{}.edit_view'.format(self._get_url(view))

    def _get_delete_url(self, view):
        return '{}.delete_view'.format(self._get_url(view))

    def _clean_resource(self):
        if self.coll:
            for coll in self.coll:
                # self.app.mongodb[coll].delete_one({'id': 'wcg2000'})
                self.mongodb[coll].delete_one({'id': 'wcg2000'})

    def _create_view(self, test_value, view):
        create_url = url_for(self._get_create_url(view))
        rv = self.client.post(create_url, data=test_value,
                              follow_redirects=True)
        self.coll.append(self._get_coll_name(view))
        return rv.data

    def _edit_view(self, test_value, view):
        coll_name = self._get_coll_name(view)
        test_id = self._get_test_value_id(test_value, view)
        edit_url = url_for(self._get_edit_url(view),
                           url='/admin/{}view/'.format(coll_name),
                           id=test_id)
        test_value['remark'] = 'new {}'.format(test_value['remark'])
        test_value['etag'] = self.mongodb[coll_name].find_one({'id': 'wcg2000'}).get('etag')
        rv = self.client.post(edit_url, data=test_value,
                              follow_redirects=True)
        return rv.data

    def _delete_view(self, test_value, view):
        coll_name = self._get_coll_name(view)
        test_id = self._get_test_value_id(test_value, view)
        delete_url = url_for(self._get_delete_url(view))
        url = '/admin/{}view/'.format(coll_name)
        data = {'id': test_id, 'url': url}
        rv = self.client.post(delete_url, data=data,
                              follow_redirects=True)
        self.coll.remove(coll_name)
        return rv.data

    def login(self):
        rv = self.client.get('/admin/login/', follow_redirects=True)
        login_html = rv.data
        login_bs = BeautifulSoup(login_html, "html5lib")
        csrf_token = login_bs.find(id='csrf_token')['value']
        login_user = {'email': 'admin@hfga.com.cn',
                      'password': 'hfgahfga%', 'csrf_token': csrf_token}
        self.client.post('/admin/login/', data=login_user,
                         follow_redirects=True)

    def _get_test_value_id(self, test_value, view):
        coll_name = self._get_coll_name(view)
        test_doc = self.mongodb[coll_name].find_one({'id': 'wcg2000'})
        if not test_doc:
            self._create_view(test_value, view)
            test_doc = self.mongodb[coll_name].find_one({'id': 'wcg2000'})
        test_id = str(test_doc.get('_id'))
        return test_id
