#coding:utf-8
from app_info import ogm


class CemrecordOgm(ogm.GraphObject):
    __primarykey__ = "id"

    id          = ogm.Property()
    zhusu2      = ogm.Property()
    mainsymptom = ogm.Property()
    yjcontent2  = ogm.Property()
    hjcontent2  = ogm.Property()

    symptoms = ogm.RelatedFrom("SymptomOgm","SYMPTOM_IN_CEM")
    diseases = ogm.RelatedFrom("DiseaseOgm","DISEASE_IN_CEM")


class DiseaseOgm(ogm.GraphObject):
    __primarykey__ = "word"

    word = ogm.Property()
    origin_id = ogm.Property()
    disease_in_cem = ogm.RelatedTo(CemrecordOgm)
    symptoms = ogm.RelatedFrom("SymptomOgm","SYMPTOM_TO")

class SymptomOgm(ogm.GraphObject):
    __primarykey__ = "word"

    word = ogm.Property()
    symptom_in_cem = ogm.RelatedTo(CemrecordOgm)
    symptom_to = ogm.RelatedTo(DiseaseOgm)
