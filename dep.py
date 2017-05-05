# coding: utf-8

from app import create_app, app
from uwsgidecorators import postfork


# 方便uwsgi启动该应用程序
@postfork
def conn_db():
    create_app()
