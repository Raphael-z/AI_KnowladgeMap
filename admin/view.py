#coding:utf8

from flask_admin import BaseView,expose

class MyView(BaseView):

    @expose('/')
    def index(self):
        return self.render('admin/index.html')

