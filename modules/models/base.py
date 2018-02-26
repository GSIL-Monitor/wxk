# coding: utf-8

from __future__ import unicode_literals

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 全局模型的基础继承
Model = db.Model
