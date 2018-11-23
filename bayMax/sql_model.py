#coding:utf8

from app_info import db

# class CemRecord(db.Model):
#     """
#     主诉,主观诊断,辅助治疗,医嘱(辅助治疗+回家后注意)
#     """
#     __bind_key__ = 'xiaonuan'
#     __tablename__ = 'cemrecord'
#
#     id         = db.Column(db.Integer,primary_key=True)
#     zhusu2     = db.Column(db.Text())   #主诉
#     mainsymtom = db.Column(db.Text())   #主观诊断
#     yjcontent2 = db.Column(db.Text())   #医嘱-辅助治疗
#     hjcontent2 = db.Column(db.Text())   #医嘱-回家后注意

class SymptomWords(db.Model):
    """
    症状词汇,用于统计症状的词汇表
    """
    __bind_key__ = 'knowladge_map'
    __tablename__ = 'ai_symptom_words'

    id  = db.Column(db.Integer,primary_key=True)
    word = db.Column(db.String(50))
    origin_id = db.Column(db.Integer)
    body_part = db.Column(db.String(50))

class SymptomHighWords(db.Model):
    __bind_key__ = 'knowladge_map'
    __tablename__ = 'ai_symptom_High_words'

    id = db.Column(db.Integer,primary_key=True)
    word = db.Column(db.String(50))
    count = db.Column(db.Integer)

class DiseaseWords(db.Model):
    """
    疾病词汇,用于统计疾病的词汇表
    """
    __bind_key__ = 'knowladge_map'
    __tablename__ = 'ai_disease_words'

    id = db.Column(db.Integer,primary_key=True)
    word = db.Column(db.String(50))
    origin_id = db.Column(db.Integer)
    level = db.Column(db.Integer)

class DiseaseHighWords(db.Model):
    __bind_key__ = 'knowladge_map'
    __tablename__ = 'ai_disease_High_words'

    id = db.Column(db.Integer,primary_key=True)
    word = db.Column(db.String(50))
    count = db.Column(db.Integer)




