# encoding: utf-8

from __future__ import unicode_literals

from flask import current_app, g
import requests


class APIRequest:

    def __init__(self, api_url):
        self.url = '{}{}'.format(current_app.config['API_BASEURL'], api_url)
        self.headers = {
            'Authorization': current_app.config['API_AUTHORIZATION'],
            'Content-Type': current_app.config['API_CONTENT_TPYE']}

    def post_request(self, json_data):
        resp = requests.post(url=self.url, headers=self.headers,
                             json=json_data)
        if resp.status_code != 201 and resp.status_code != 200:
            raise ValueError(resp.json()['message'])
        if resp.status_code == 401:
            g.token = get_api_token()
        return resp

    def put_request(self, data, etag):
        headers = self.headers.copy()
        headers.update({
            'If-Match': etag,
        })
        resp = requests.put(url=self.url, headers=headers, json=data)
        if resp.status_code != 200:
            raise Exception(resp.text)
        if resp.status_code == 401:
            g.token = get_api_token()
        return resp

    def delete_request(self, etag):
        headers = self.headers.copy()
        headers.update({
            'If-Match': etag,
        })
        resp = requests.delete(url=self.url, headers=headers)
        if resp.status_code != 204 and resp.status_code != 200:
            raise Exception(resp.text)
        if resp.status_code == 401:
            g.token = get_api_token()
        return resp


def get_api_token():
    url = current_app.config['API_AUTH_URL']
    headers = {'Content-Type': current_app.config['API_CONTENT_TPYE']}
    json_data = current_app.config['API_AUTH_USER']
    resp = requests.post(url=url, headers=headers, json=json_data)
    jsons = resp.json()
    return 'Bearer {}'.format(jsons.get('accessToken'))
