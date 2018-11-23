# coding:utf8

import json
import jieba
from flask_restful import Resource
from flask import request

from app_info import db,graph
from sql_model  import SymptomWords,DiseaseWords,SymptomHighWords,DiseaseHighWords
from neo_model import SymptomOgm,CemrecordOgm,DiseaseOgm

def is_same_symp(source_data,new_data):
    pass

def is_same_sort(source_data,new_data):
    """
    判断描述是否一致
    :param source_data:
    :param new_data:
    :return:
    """
    if len(source_data) == 0 :
        return 0
    else:
        proportion = round(float(len(set(source_data) & set(new_data))) / float(len(source_data)),2)
        if proportion >= 0.6:
            return 1
        else:
            return 0

def jieba_app(word):
    """
    用于疾病分类
    :param word:
    :return:
    """
    pass_word = ['疾病','性','病','症','和','发性','不良','综合','综合征']
    seg_list = jieba.cut(word)
    category_str = " ".join(seg_list)
    category_list = category_str.encode('utf8').split(' ')
    new_category_list = []
    for category in category_list:
        if category and category not in new_category_list:
            if  category not in pass_word:
                new_category_list.append(category)
    return new_category_list

def jieba_app_symp(word):
    """
    生成症状高频词
    :param word:
    :return:
    """
    seg_list = jieba.cut(word,cut_all=True)
    category_str = " ".join(seg_list)
    category_list = category_str.encode('utf8').split(' ')
    new_category_list = []
    print 'category_list==',category_list
    for category in category_list:
        if category and category not in new_category_list:
            is_high = db.session.query(SymptomHighWords).filter_by(word=category).first()
            if is_high:
                pass
            else:
                new_category_list.append(category)
    return new_category_list

def jieba_app_disease(word):
    """
    生成疾病高频词
    :param word:
    :return:
    """
    pass_word = ['疾病','性','病','症','和','发性','不良','综合','综合征']
    seg_list = jieba.cut(word,cut_all=True)
    category_str = " ".join(seg_list)
    category_list = category_str.encode('utf8').split(' ')
    new_category_list = []
    for category in category_list:

        if category and category not in new_category_list:
            if  category not in pass_word:
                is_high = db.session.query(DiseaseHighWords).filter_by(word=category).first()
                if is_high:
                    pass
                else:
                    new_category_list.append(category)
    return new_category_list

def sort_symp():
    """
    症状分类动作
    :return:
    """
    #1.去症状表中的重复项
    # symp_words = db.session.query(SymptomWords).all()
    # symp_list = []
    # for symp in symp_words:
    #     symp_word = symp.word
    #     if symp_word in symp_list:
    #         db.session.delete(symp)
    #         db.session.commit()
    #     else:
    #         symp_list.append(symp_word)

    # symp_querys = db.session.query(SymptomWords).all()
    # symp_category = []
    # all_words = []
    # for symp in symp_querys:
    #     word = symp.word
    #     new_category_list = jieba_app_symp(word)
    #     all_words += new_category_list
    # all_words_set = list(set(all_words))
    # for i in all_words_set:
    #     symp_obj = SymptomHighWords(
    #         word = i,
    #         count = all_words.count(i),
    #     )
    #     db.session.add(symp_obj)
    #     db.session.commit()

        # symp_category.append(new_category_list)

    symp_querys = db.session.query(SymptomWords).all()
    symp_all_word = []
    for symp in symp_querys:
        word = symp.word
        symp_all_word.append(word)

    # 开始分类,提取高频词
    with open('data/cem.json') as f:
        cem_data = json.load(f)
    all_words = []
    num = 0

    for cem in cem_data:

        id = cem[u'id']
        zhusu2      = cem[u'zhusu2']
        mainsymptom = cem[u'mainsymptom']
        yjcontent2  = cem[u'yjcontent2']
        hjcontent2  = cem[u'hjcontent2']

        for word in symp_all_word:
            if word in zhusu2:
                num += 1
                print num

        # new_category_list = jieba_app(zhusu2)
    #     all_words += new_category_list
    # all_words_set = list(set(all_words))
    # num = 0
    # for i in all_words_set:
    #     num += 1
    #     print 'new_num ========= ',num
    #     try:
    #         symp_obj = SymptomHighWords(
    #             word = i,
    #             count = all_words.count(i),
    #         )
    #         db.session.add(symp_obj)
    #         db.session.commit()
    #     except:
    #         continue
    #     zhusu2_category.append(new_category_list)
    #     for symp in symp_category:
    #         is_same = is_same_sort(symp,new_category_list)
    #         if is_same == 1:
    #             num += 1
    #             print num



def sort_disease():
    """
    疾病分类症状
    :return:
    """
    symp_querys = db.session.query(DiseaseWords).filter_by(level=2).all()
    symp_category = []
    all_words = []
    for symp in symp_querys:
        word = symp.word
        new_category_list = jieba_app(word)
        all_words += new_category_list
    # all_words_set = list(set(all_words))
    # for i in all_words_set:
    #     symp_obj = DiseaseHighWords(
    #         word = i,
    #         count = all_words.count(i),
    #     )
    #     db.session.add(symp_obj)
    #     db.session.commit()

        symp_category.append(new_category_list)
    #开始分类
    with open('data/cem.json') as f:
        cem_data = json.load(f)
    num = 0
    count = 0
    for cem in cem_data:
        id = cem[u'id']
        zhusu2      = cem[u'zhusu2']
        mainsymptom = cem[u'mainsymptom']
        yjcontent2  = cem[u'yjcontent2']
        hjcontent2  = cem[u'hjcontent2']
        count += 1
        print 'count====',count,num
        new_category_list = jieba_app(mainsymptom)
        for symp in symp_category:
            is_same = is_same_sort(symp,new_category_list)
            if is_same == 1:
                num += 1
                print 'num====',num
        if count >5000:
            break
    # return symp,new_category_list

def insert_neo():
    dis_querys = db.session.query(DiseaseWords).filter_by(level=2).all()
    symp_querys = db.session.query(SymptomWords).all()
    #开始分类
    with open('data/cem.json') as f:
        cem_data = json.load(f)
    num = 0
    for cem in cem_data:
        id = cem[u'id']
        zhusu2      = cem[u'zhusu2']
        mainsymptom = cem[u'mainsymptom']
        yjcontent2  = cem[u'yjcontent2']
        hjcontent2  = cem[u'hjcontent2']
        # zhusu2_list = jieba_app(zhusu2)
        mainsymptom_list = jieba_app(mainsymptom)
        num += 1
        print 'num===========',num

        temp_dict = {}
        for symp in symp_querys:
            symp_id = symp.id
            symp_word = symp.word
            # symp_word_list = jieba_app(symp.word)
            # symp_is_same = is_same_sort(symp_word_list,zhusu2_list)
            if symp_word in zhusu2:
                for dis in dis_querys:
                    dis_id = dis.id
                    dis_word = dis.word
                    dis_word_list = jieba_app(dis.word)
                    dis_is_same = is_same_sort(dis_word_list,mainsymptom_list)
                    if dis_is_same == 1:
                        # dis_key = str(symp_id) + '_' + str(dis_id)
                        # if dis_key in temp_dict.keys():
                        #     temp_dict[dis_key] += 1
                        # else:
                        #     temp_dict[dis_key] = 1
                        #可以录入到neo4j 建立症状和疾病的关联关系
                        symptom = graph.find_one(label='SymptomOgm',property_key='word',property_value=symp_word)
                        disease = graph.find_one(label='DiseaseOgm',property_key='word',property_value=dis_word)
                        relation = graph.match_one(start_node=symptom,end_node=disease,rel_type='SYMPTOM_TO')
                        # relations = graph.match(start_node=symptom,end_node=disease,rel_type='SYMPTOM_TO')
                        # n = 0
                        # for i in relations:
                        #     print n
                        #     n+=1
                        count = 1
                        if relation:
                            count = relation.get('count') + 1
                        symptom = SymptomOgm.select(graph,symp_word).first()
                        disease = DiseaseOgm.select(graph,dis_word).first()
                        symptom.symptom_to.add(disease,{'count':count})
                        graph.push(symptom)

class SortData(Resource):
    """
    分类算法:
    1.症状类别特征提取,疾病类别特征提取
    2.病历主诉特征提取,并根据症状类特征值分类
    3.病历诊断特征提取,并根据疾病类特征值分类
    4.症状-病历ID-疾病录入关系型数据库,之后再计算权重值并录入到Neo4j建立知识图谱
    关注重点:
    1.分类的准确度
    2.症状类别丰富度,准确度
    3.疾病类别丰富度,准确度
    """
    def get(self):
        """
        sourt_symp

        :return:
        """
        # with open('data/cem.json') as f:
        #     cem_data = json.load(f)
        # for cem in cem_data:
        #     id = cem[u'id']
        #     zhusu2      = cem[u'zhusu2']
        #     mainsymptom = cem[u'mainsymptom']
        #     yjcontent2  = cem[u'yjcontent2']
        #     hjcontent2  = cem[u'hjcontent2']
        sort_symp()
        # sort_disease()
        # result = is_same_sort(symp,mainsymptom)
        # high_symp = db.session.query(SymptomHighWords).all()
        # high_dis = db.session.query(DiseaseHighWords).all()
        return {'error_no':0,'msg':'sss'},200

class SearchDemo(Resource):

    def get(self):
        """
        模拟查询程序1.0
        :return:
        """
        describe = request.args.get('describe')
        symp_querys = db.session.query(SymptomWords).all()
        symp_list = []
        for symp in symp_querys:
            symp_word = symp.word
            origin_word = symp_word

            if symp_word in describe:
                print 'symp_word=====',symp_word
                symp_list.append(origin_word)
        symp_list = list(set(symp_list))

        possible_list = []
        for symp in symp_list:

            symptom = graph.find_one(label='SymptomOgm',property_key='word',property_value=symp)
            disease_list = []

            for sr in graph.match(start_node=symptom,rel_type='SYMPTOM_TO'):
                disease = sr.end_node()['word']
                disease_list.append(disease)
            possible_list.append(disease_list)
        result_list = []
        for dis_list in possible_list:
            if result_list:
                result_list = list(set(result_list) & set(dis_list))
            else:
                result_list = dis_list

        return {'error_no':0,'msg':result_list},200

class InsertCemrecordNeo(Resource):

    def get(self):
        """
        各种数据录入neo4j形成知识网络1.0
        :return:
        """
        # 录入neo4j数据库
        insert_neo()

        # 1.基础症状和疾病名称录入系统,无关联关系
        # symp_querys = db.session.query(SymptomWords).all()
        # for symp in symp_querys:
        #     symptom = SymptomOgm()
        #     symptom.word = symp.word
        #     graph.create(symptom)
        # dis_querys = db.session.query(DiseaseWords).filter_by(origin_id=0).all()
        # for dis in dis_querys:
        #     id = dis.id
        #
        #     # dis.level = 0
        #     # db.session.commit()
        #     child_querys = db.session.query(DiseaseWords).filter_by(origin_id=id).all()
        #     for child in child_querys:
        #         child_id = child.id
        #         # child.level = 1
        #         # db.session.commit()
        #         grand_child_querys = db.session.query(DiseaseWords).filter_by(origin_id=child_id).all()
        #         for grand_child in grand_child_querys:
        #             origin_id = child_id
        #             word = grand_child.word
        #             # grand_child.level = 2
        #             # db.session.commit()
        #             disease = DiseaseOgm()
        #             disease.word = word
        #             disease.origin_id = origin_id
        #             graph.create(disease)

            #3.创建三层疾病系统时使用
            # disease = DiseaseOgm.select(graph,word).first()
            # print '1111==============',dir(disease.diseases)
            # child_querys = db.session.query(DiseaseWords).filter_by(origin_id=id).all()
            # for child in child_querys:
            #     child_id = child.id
            #     child_word = child.word
            #     child_disease = DiseaseOgm()
            #     child_disease.word = child_word
            #     graph.create(child_disease)
            #
            #     child_disease = DiseaseOgm.select(graph,child_word).first()
            #     disease.diseases.add(child_disease)
            #     graph.push(child_disease)
            #
            #     grandchild_querys = db.session.query(DiseaseWords).filter_by(origin_id=child_id).all()
            #     for grandchild in grandchild_querys:
            #
            #         grandchild_word = child.word
            #         grandchild_disease = DiseaseOgm()
            #         grandchild_disease.word = grandchild_word
            #         graph.create(grandchild_disease)
            #
            #         grandchild_disease = DiseaseOgm.select(graph,grandchild_word).first()
            #         child_disease.diseases.add(grandchild_disease)
            #         graph.push(grandchild_disease)




        # symp_querys = db.session.query(SymptomWords).all()
        # dis_querys = db.session.query(DiseaseWords).all()
        # with open('data/cem.json') as f:
        #     cem_data = json.load(f)
        # for cem in cem_data:
        #     id = cem[u'id']
        #     zhusu2      = cem[u'zhusu2']
        #     mainsymptom = cem[u'mainsymptom']
        #     yjcontent2  = cem[u'yjcontent2']
        #     hjcontent2  = cem[u'hjcontent2']
        #     cemrecord   = CemrecordOgm()
        #     cemrecord.id = id
        #     cemrecord.zhusu2 = zhusu2
        #     cemrecord.mainsymptom = mainsymptom
        #     cemrecord.yjcontent2 = yjcontent2
        #     cemrecord.hjcontent2 = hjcontent2
        #     graph.create(cemrecord)
        #     symp_list = []
        #     for symp in symp_querys:
        #         symp_word = symp.word
        #         origin_id = symp.origin_id
        #         if origin_id == 0:
        #             origin_word = symp_word
        #         else:
        #             origin_word = db.session.query(SymptomWords).filter_by(id=origin_id).first().word
        #         if symp_word in zhusu2:
        #             symp_list.append(origin_word)
        #     symp_list = list(set(symp_list))
        #     for symp in symp_list:
        #         symptom = SymptomOgm.select(graph,symp).first()
        #         cemrecord = CemrecordOgm.select(graph,id).first()
        #         symptom.symptom_in_cem.add(cemrecord)
        #         graph.push(symptom)
        #     dis_list = []
        #     for dis in dis_querys:
        #         dis_word = dis.word
        #         origin_id = dis.origin_id
        #         if origin_id == 0:
        #             origin_word = dis_word
        #         else:
        #             origin_word = db.session.query(DiseaseWords).filter_by(id=origin_id).first().word
        #         if dis_word in mainsymptom:
        #             dis_list.append(origin_word)
        #     dis_list = list(set(dis_list))
        #     for dis in dis_list:
        #         disease = DiseaseOgm.select(graph,dis).first()
        #         cemrecord = CemrecordOgm.select(graph,id).first()
        #         disease.disease_in_cem.add(cemrecord)
        #         graph.push(disease)
        #节点关系录入系统


        return {'error_no':0,'msg':'success'},200

def insert_symptom(word,origin_id):
    new_word = SymptomWords(
        word=word,
        origin_id=origin_id,
    )
    db.session.add(new_word)
    db.session.commit()
    return new_word.id

def insert_disease(word,origin_id):

    new_word = DiseaseWords(
        word=word,
        origin_id=origin_id,
    )
    db.session.add(new_word)
    db.session.commit()
    return new_word.id

class PreSymptomWords(Resource):

    def get(self):
        word_dict = [
            {'origin':u'驱虫','others':[u'驱',u'虫']},
            {'origin':u'免疫','others':[u'疫',u'疫苗',u'苗']},
            {'origin':u'检查','others':[u'检',u'查']},
            {'origin':u'绝育','others':[u'绝',u'育']},
            {'origin':u'怀孕','others':[u'妊娠',u'胎儿',u'胎心']},
            {'origin':u'食欲','others':[u'厌食',u'不吃',u'下降']},
            {'origin':u'皮肤','others':[u'红疹',u'痒',u'过敏',u'皮',u'屑']},
            {'origin':u'毛发','others':[u'毛',u'发']},
            {'origin':u'精神','others':[u'不振',u'状态']},
            {'origin':u'呕吐','others':[u'呕',u'吐']},
            {'origin':u'喷嚏','others':[]},
            {'origin':u'鼻涕','others':[]},
            {'origin':u'咳嗽','others':[u'咳']},
            {'origin':u'分泌物','others':[u'分泌']},
            {'origin':u'外伤','others':[u'手术',u'伤',u'咬']},
            {'origin':u'进食','others':[u'吃',u'食',u'喝']},
            {'origin':u'眼睛','others':[u'眼',u'泪']},
            {'origin':u'瘟','others':[]},
            {'origin':u'拉肚子','others':[u'拉',u'肚子',u'脱水',u'便',u'秘']},
            {'origin':u'牙齿','others':[u'牙',u'齿']},
            {'origin':u'安乐死','others':[u'安乐',u'死']},
            {'origin':u'肾','others':[u'肾衰竭']},
            {'origin':u'血虫','others':[]},
        ]
        for i in word_dict:
            origin = i['origin']
            others = i['others']
            origin_id = insert_symptom(origin,0)
            for j in others:
                word = j
                insert_symptom(word,origin_id)

        return {'error_no':0,'msg':'success'},200

class PreDiseaseWords(Resource):

    def get(self):

        word_dict = [
            {'origin':u'绝育','others':[u'育']},
            {'origin':u'免疫','others':[u'疫苗',u'疫']},
            {'origin':u'感染','others':[u'染',u'病毒',u'菌',u'虫']},
            {'origin':u'炎症','others':[u'炎']},
            {'origin':u'过敏','others':[u'敏']},
            {'origin':u'肿瘤','others':[u'瘤']},
            {'origin':u'外伤','others':[u'手术',u'伤',u'咬']},
            {'origin':u'感冒','others':[]},
            {'origin':u'误食','others':[]},
        ]
        for i in word_dict:
            origin = i['origin']
            others = i['others']
            origin_id = insert_disease(origin,0)
            for j in others:
                word = j
                insert_disease(word,origin_id)

        return {'error_no':0,'msg':'success'},200
