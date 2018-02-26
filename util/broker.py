# coding: utf-8

from __future__ import unicode_literals
from flask import current_app
import json

from tonghangyun_common.broker import block_rabbitmq_channel


def rabbitmq(data=None, exchange=None, routing_key=None):
    with block_rabbitmq_channel(
        current_app.config['MQ_HOST'],
        current_app.config['MQ_USERNAME'],
        current_app.config['MQ_PASSWORD'],
        current_app.config['MQ_EXCHANGE'],
    ) as channel:

        channel.basic_publish(
            body=data,
            exchange=exchange if exchange else current_app.config['MQ_EXCHANGE'],
            routing_key=routing_key if routing_key else current_app.config['FILE_ROUTING_KEY']
        )


def file_remove(key, name, file_type=''):

    data = json.dumps({
        'type': file_type,
        'name': name,
        'key': key
    })

    rabbitmq(data=data)


def file_move(source, target, operation='move'):

    data = json.dumps({
        'operation': operation,
        'source': source.encode('utf-8'),
        'target': target.encode('utf-8'),
    })

    rabbitmq(data=data)
