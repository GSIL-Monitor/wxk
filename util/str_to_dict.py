# encoding: utf-8

from __future__ import unicode_literals

from flask import current_app
import base64
import time


def updateFileStr(file_obj, file_type, unrelateDoc=False):

    url = base64.urlsafe_b64decode(file_obj.get('key').encode('utf-8')).decode('utf-8').split('/')[1:]
    source = '/'.join(url)
    if not unrelateDoc:
        target = '/'.join([file_type, str(int(time.time())), url[-1]])
    else:
        target = '/'.join([url[0], file_type, str(int(time.time())), url[-1]])
    save_target = base64.urlsafe_b64encode('{}/{}'.encode('utf-8').format(
                                           current_app.config['WXK_GROUP'],
                                           target.encode('utf-8')))
    update = {'name': file_obj.get('name'),
              'key': save_target}

    return {'source': source,
            'target': target,
            'update': update}
