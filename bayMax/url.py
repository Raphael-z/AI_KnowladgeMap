from api_view import PreSymptomWords,PreDiseaseWords,InsertCemrecordNeo,SearchDemo,SortData
from view import IndexView,DiagnoseView,DiagnoseDetailView,DiagnoseAllView,SymptomsView,DiseasesView

def app_url(app):
    app.add_url_rule('/baymax/index','baymax_index',IndexView.as_view('baymax_index'))
    app.add_url_rule('/baymax/diagnose','baymax_diagnose',DiagnoseView.as_view('baymax_diagnose'))
    app.add_url_rule('/baymax/diagnose_all','baymax_diagnose_all',DiagnoseAllView.as_view('baymax_diagnose_all'))
    app.add_url_rule('/baymax/diagnose_detail','baymax_diagnose_detail',DiagnoseDetailView.as_view('baymax_diagnose_detail'))
    app.add_url_rule('/baymax/symptoms','baymax_diagnose_symptoms',SymptomsView.as_view('baymax_diagnose_symptoms'))
    app.add_url_rule('/baymax/diseases','baymax_diagnose_diseases',DiseasesView.as_view('baymax_diagnose_diseases'))

root_url = '/baymax/api/'

def api_url(api):

    api.add_resource(PreSymptomWords,root_url+'pre_symptom')
    api.add_resource(PreDiseaseWords,root_url+'pre_disease')
    api.add_resource(InsertCemrecordNeo,root_url+'insert_cem')
    api.add_resource(SearchDemo,root_url+'search')
    api.add_resource(SortData,root_url+'sort_data')