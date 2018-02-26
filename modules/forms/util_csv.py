# encoding: utf-8

from __future__ import unicode_literals
import csv
import logging

from flask import current_app


def read_file(cfg_file, read_datas, skip_first=False):
    datas = []
    count = 0
    with open(cfg_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if skip_first:
                skip_first = False
                continue
            data = read_datas(row)
            if data:
                datas.append(data)
            count += 1
    if len(datas) != count:
        return []
    return datas


def read_datas(row):
    data = {}
    return data


def reset_datas(cfg_file, col_name, read_datas=read_datas,
                skip_first=False, clean=True):

    conn = current_app.mongodb
    datas = read_file(cfg_file, read_datas, skip_first)

    count = 0
    if len(datas):
        # 清空数据
        if clean == "true":
            conn[col_name].delete_many({})
        for data in datas:
            try:
                conn[col_name].insert_one(data)
                count += 1
            except Exception as e:
                logging.warn(e)

    return count
