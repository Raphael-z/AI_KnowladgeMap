#coding:utf8

"""
脚本
症状正则匹配,并录入symptom数据库中
"""

import re
from bayMax.sql_model import SymptomWords
from app_info import db

f = open('data/symptoms.txt')
lines = f.readlines()
for line in lines:
    # regex_str = r"\d\.\d\.\d\s"+".*?([\u4E00-\u9FA5])"
    a = re.match(r'\d\.\d\.\d',line)
    if a:
        symptom = line.split(" ")[1]
        symp = SymptomWords(word=symptom,origin_id=0)
        db.session.add(symp)
        db.session.commit()


