#coding:utf8
from flask import Flask

from app_info import app,api,admin
from url_manage import UrlManage
#注册URL

UrlManage.register_app_url(app)
UrlManage.register_api_url(api)
UrlManage.register_admin_url(admin)
if __name__ == '__main__':

    app.run()
