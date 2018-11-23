#coding:utf8

"""
脚本
三级病种数据录入数据库
"""

import xlrd,xlwt
from bayMax.sql_model import DiseaseWords
from app_info import db

con = xlrd.open_workbook('data/diseases.xlsx')
table = con.sheet_by_name('data')
nrows = table.nrows
ncols = table.ncols
for i in range(1,nrows):
    if table.cell(i,0).value:
        dis_1 = table.cell(i,0).value
        dis_1_instance = DiseaseWords(word=dis_1,origin_id=0)
        db.session.add(dis_1_instance)
        db.session.commit()
        dis_1_id = dis_1_instance.id
    if table.cell(i,1).value:
        dis_2 = table.cell(i,1).value
        dis_2_instance = DiseaseWords(word=dis_2,origin_id=dis_1_id)
        db.session.add(dis_2_instance)
        db.session.commit()
        dis_2_id = dis_2_instance.id
    dis_3 = table.cell(i,2).value
    dis_3_instance = DiseaseWords(word=dis_3,origin_id=dis_2_id)
    db.session.add(dis_3_instance)
    db.session.commit()







