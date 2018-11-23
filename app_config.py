#!/usr/bin/env python
# -*- coding: utf-8 -*-

#是否开启调试模式
DEBUG = True
#SQL配置
SQLALCHEMY_BINDS = {
    'knowladge_map': "mysql://%s:%s@%s/%s" % ('root', 'xxxxx', 'localhost', 'knowladge_map_test'),
}
# SQLALCHEMY_POOL_SIZE = 100
# SQLALCHEMY_POOL_TIMEOUT = 100
# SQLALCHEMY_POOL_RECYCLE = 5
# SQLALCHEMY_TRACK_MODIFICATIONS = False
BABEL_DEFAULT_LOCALE = 'zh_CN'

CSRF_ENABLED = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'