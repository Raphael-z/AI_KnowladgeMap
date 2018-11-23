#coding:utf8

from TEST.url import app_url as test_app_url
from TEST.url import api_url as test_api_url
from bayMax.url import app_url as pd_app_url
from bayMax.url import api_url as pd_api_url
from admin.url import admin_url

class UrlManage(object):

    @classmethod
    def register_app_url(self,app):
        """
        注册app url
        :param app:
        :return:
        """
        test_app_url(app)
        pd_app_url(app)

    @classmethod
    def register_api_url(self,api):
        """
        注册api url
        :param app:
        :return:
        """
        test_api_url(api)
        pd_api_url(api)

    @classmethod
    def register_admin_url(self,admin):
        """

        :param admin:
        :return:
        """
        admin_url(admin)
