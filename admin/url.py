#coding:utf8

from admin.view import MyView
from flask_admin.contrib.sqla import ModelView
from bayMax.sql_model import SymptomWords,DiseaseWords
from app_info import db

def admin_url(admin):

    admin.add_view(MyView(name=u'Hello'))

    ModelView.column_searchable_list=(SymptomWords.word,)
    admin.add_view(ModelView(SymptomWords,db.session))

    ModelView.column_searchable_list=(DiseaseWords.word,)
    admin.add_view(ModelView(DiseaseWords,db.session))