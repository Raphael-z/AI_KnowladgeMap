#coding:utf-8

from flask import render_template,request
from flask.views import View
from app_info import db,graph
from sql_model import SymptomWords,DiseaseWords

class IndexView(View):

    methods = ['GET','POST']

    def dispatch_request(self):
        """
        bayMax辅助诊疗基础应用,初始页面
        根据症状给出疾病机率
        :return:
        """
        if request.method == 'GET':
            return render_template('bayMax/index.html')

def diagnose(symp_list):
    """
    诊断说明
    :param symp_list: 症状词语
    :return: 疾病结果
    """
    symp_source_dict = {}
    possible_list = []

    for i in symp_list:
        symp_source_dict[i] = {}
        symptom = graph.find_one(label='SymptomOgm',property_key='word',property_value=i)
        disease_list = []
        for sr in graph.match(start_node=symptom,rel_type='SYMPTOM_TO'):
            disease_word = sr.end_node()['word']
            disease_list.append(disease_word)
            symp_source_dict[i][disease_word] = sr.get('count')

        possible_list.append(disease_list)
    result_list = []
    for dis_list in possible_list:
        if result_list:
            result_list = list(set(result_list) & set(dis_list))
        else:
            result_list = dis_list

    #计算发生机率
    final_list = []
    for i in symp_source_dict.keys():
        symp_source_dict[i]['all'] = 0
        for j in symp_source_dict[i].keys():
            symp_source_dict[i]['all'] += int(symp_source_dict[i][j])

    for i in result_list:
        dis_dict = {}
        dis_dict['word'] = i
        prop = 1
        for j in symp_list:
            prop *= float(symp_source_dict[j][i])/symp_source_dict[j]['all'] if symp_source_dict[j]['all']!=0 else 0
        dis_dict['proportion'] = prop
        final_list.append(dis_dict)
    sum_prop = 0
    for i in final_list:
        sum_prop += i['proportion']
    print 'sum_prop====',sum_prop
    new_list = []
    for i in final_list:
        i['proportion'] = round(i['proportion']/sum_prop,4)*100
        if i['proportion'] > 1:
            new_list.append(i)

    for i in new_list:
        dis_word = i['word']
        disease = graph.find_one(label='DiseaseOgm',property_key='word',property_value=dis_word)
        symp_list = []
        for sr in graph.match(end_node=disease,rel_type='SYMPTOM_TO'):
            symp_dict = {}
            symp_dict['word']  = sr.start_node()['word']
            symp_dict['count'] = sr.get('count')
            symp_list.append(symp_dict)
        symp_list.sort(key=lambda x:(-x['count']))
        i['symps'] = symp_list[0:6] if len(symp_list)>6 else symp_list



    # for dis in result_list:
    #     dis_dict = {}
    #     dis_dict['word'] = dis
    #     disease = graph.find_one(label='DiseaseOgm',property_key='word',property_value=dis)
    #     all_num = 0
    #     hold_num = 0
    #
    #     for st in graph.match(end_node=disease,rel_type='SYMPTOM_TO'):
    #         symp_word = st.start_node()['word']
    #         count = st.get('count')
    #         print 'symp_word===',symp_word
    #         print 'count======',count
    #         if int(count) > 20:
    #             all_num += int(count)
    #             if symp_word in symp_list:
    #                 print 'symp in symp_list'
    #                 hold_num += int(count)
    #     dis_dict['proportion'] = round(float(hold_num)/all_num,3)*100 if all_num != 0 else 0
    #     if dis_dict['proportion'] > 0:
    #         final_list.append(dis_dict)
    new_list.sort(key=lambda x:(-x['proportion']))
    return new_list

class DiagnoseView(View):

    methods = ['GET','POST']

    def dispatch_request(self):
        """
        bayMax诊断前四结果
        :return:
        """
        if request.method == 'GET':
            symp = request.args.get('symp')
            symp_list = []
            symp_querys = db.session.query(SymptomWords).all()
            for i in symp_querys:
                symp_word = i.word
                if symp_word in symp:
                    symp_list.append(symp_word)
            symp_list = list(set(symp_list))
            if len(symp_list) == 0 :
                return render_template('bayMax/diagnose.html',
                                   symp=symp,
                                   result_list=[],
                                   )
            else:
                final_list = diagnose(symp_list)
                return render_template('bayMax/diagnose.html',
                                   symp=symp,
                                   result_list=final_list[0:4],
                                   )
class DiagnoseAllView(View):

    methods = ['GET','POST']

    def dispatch_request(self):
        """
        bayMax诊断全部结果
        :return:
        """
        if request.method == 'GET':
            symp = request.args.get('symp')
            symp_list = []
            symp_querys = db.session.query(SymptomWords).all()
            for i in symp_querys:
                symp_word = i.word
                if symp_word in symp:
                    symp_list.append(symp_word)
            symp_list = list(set(symp_list))
            if len(symp_list) == 0 :
                return render_template('bayMax/diagnose_all.html',
                                   symp=symp,
                                   result_list=[],
                                   )
            else:
                final_list = diagnose(symp_list)
                return render_template('bayMax/diagnose_all.html',
                                   symp=symp,
                                   result_list=final_list,
                                   )


class DiagnoseDetailView(View):

    methods = ['GET','POST']

    def dispatch_request(self):
        """
        bayMax诊断结果
        :return:
        """
        if request.method == 'GET':
            return render_template('bayMax/diagnose_detail.html')


class SymptomsView(View):

    methods = ['GET','POST']

    def dispatch_request(self):
        """
        所有症状统计
        :return:
        """
        if request.method == 'GET':
            symp_querys = db.session.query(SymptomWords).all()
            symp_dict = {}
            for i in symp_querys:
                if i.body_part not in symp_dict.keys():
                    symp_dict[i.body_part] = []
                    symp_dict[i.body_part].append(i.word)
                else:
                    symp_dict[i.body_part].append(i.word)
            return render_template('bayMax/symptoms.html',
                                   symp_dict=symp_dict,
                                   )

class DiseasesView(View):

    methods = ['GET','POST']

    def dispatch_request(self):
        """
        所有疾病统计
        :return:
        """
        if request.method == 'GET':
            page_num = 1
            page_size = 10
            disease_items = DiseaseWords.query.filter_by(level=2).paginate(int(page_num),int(page_size),False).items
            data_list = []
            for i in disease_items:
                dis_dict = {}
                dis_name = i.word
                sec_id = i.origin_id
                sec_item = db.session.query(DiseaseWords).filter_by(id=sec_id).first()
                sec_name = sec_item.word
                fir_id = sec_item.origin_id
                fir_name = db.session.query(DiseaseWords).filter_by(id=fir_id).first().word
                dis_dict['dis_name'] = dis_name
                dis_dict['sec_name'] = sec_name
                dis_dict['fir_name'] = fir_name
                data_list.append(dis_dict)
            disease_all = db.session.query(DiseaseWords).filter_by(level=2).all()
            disease_num = len(disease_all)
            print '1=======',disease_num
            all_page_num = disease_num/10
            if disease_num % 10 != 0:
                all_page_num += 1
            print '2=======',all_page_num
            all_page_num += 1

            all_page_num = 7
            return render_template('bayMax/diseases.html',data_list=data_list,all_page_num=all_page_num)