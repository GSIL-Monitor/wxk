# encoding: utf-8

from __future__ import unicode_literals
import logging

from sqlalchemy_continuum import version_class

from modules.forms.util_csv import read_file, read_datas
from .base import db


def reset_datas(cfg_file, col_name, read_datas=read_datas,
                skip_first=False, clean=True):

    datas = read_file(cfg_file, read_datas, skip_first)

    count = 0
    length = len(datas)
    if len(datas):
        # 清空数据
        if clean == "true":
            db.session.query(col_name).delete()
            version = version_class(col_name)
            db.session.query(version).delete()
            db.session.commit()
        for data in datas:
            try:

                inst = col_name(**data)
                db.session.add(inst)
                count += 1
            except Exception as e:
                logging.warn(e)
        if length != count:
            logging.warn("not all the datas can import")
            return
        try:
            db.session.commit()
        except Exception as e:
            logging.warn(e)
            db.session.rollback()
    return count
