'__author__' == 'cyril'


from flask import Flask, request, render_template
import pickle
from tva_project.models.model import Model


app = Flask(__name__)


def generate_test_factors():
    slider_dics_list = []
    for i in range(20):
        sd = {'name': 'factor+i', 'min': 10+i, 'max': 20+i,
              'value': 15+i, 'step': 1}
        slider_dics_list.append(sd)
    return slider_dics_list


def initial_put():
    with open('dummy.txt', 'wb') as f:
        pickle.dump(load_defaults(), f)
    return load_defaults()


def dummy_db_put(req_form):
    db_dic = dummy_db_get()
    new_dic = []
    for f in db_dic:
        old_val = f['value']
        f_name = f['name']
        new_val = 0
        new_val1 = req_form[f_name+'f']
        new_val2 = req_form[f_name+'r']
        if old_val == new_val1:
            new_val = new_val2
        else:
            new_val = new_val1
        f['value'] = new_val
        new_dic.append(f)
    with open('dummy.txt', 'wb') as f:
        pickle.dump(new_dic, f)
    return new_dic


def blacklist():
    return ['rez']


def dummy_db_put_single(req_form):
    db_dic = dummy_db_get()
    new_dic = []
    for f in db_dic:
        f_name = f['name']
        if f_name not in blacklist():
            try:
                f['value'] = float(eval(req_form[f_name]))
            except SyntaxError as err:
                f['value'] = float(req_form[f_name])
        else:
            print("blacklist invoked")
            f['value'] = req_form[f_name]
        new_dic.append(f)
    with open('dummy.txt', 'wb') as f:
        pickle.dump(new_dic, f)
    return new_dic


def dummy_db_get():
    with open('dummy.txt', 'rb') as f:
        dic = pickle.load(f)
    return dic


"""
Web Interface Logic Handling
"""


@app.route('/', methods=['POST', 'GET'])
def value_brain():
    if request.method == 'POST':
        """
        ## For when use slider too
        factor_names = list(set([i[:-1] for i in request.form]))
        sliders = dummy_db_put(request.form)
        """
        sliders = dummy_db_put_single(request.form)
        Model(sliders).plot()
        cats = ["Input", "FTTH", "FTTSB", "FTTB", "FTTS"]
        # print(request.form)
        s_dic = {'factors': sliders, 'cats': cats}
        return render_template('main_slim.html',
                               sliders=s_dic)
    else:
        sliders = initial_put()
        Model(sliders).plot()
        cats = ["Input", "FTTH", "FTTSB", "FTTB", "FTTS"]
        s_dic = {'factors': sliders, 'cats': cats}
        return render_template('main_slim.html',
                               sliders=s_dic)


def load_defaults():
    return list([{'name': 'max_horizon', 'cat': 'plot', 'value': 8*12},
                 {'name': 'slider', 'cat': 'plot', 'value': 12},
                 # Input
                 {'name': 'rez', 'cat': 'Input', 'value': "2342-234"},
                 {'name': 'anzahl_ne', 'cat': 'Input', 'value': 10},
                 # FTTH
                 {'name': 'fan_wartung', 'cat': 'FTTH Betrieb', 'value': 521.7,
                  'desc': "Wartungskosten pro Jahr anfallend für INI-ON"},
                 {'name': 'fan_strom', 'cat': 'FTTH Betrieb', 'value': 1557.70},
                 {'name': 'fan_proacM', 'cat': 'FTTH Betrieb', 'value': 344.45},
                 {'name': 'fan_logistik', 'cat': 'FTTH Betrieb',
                  'value': 22.02},
                 {'name': 'fan_assurance', 'cat': 'FTTH Assurance',
                  'value': 22.02},
                 {'name': 'fan_eff_bel', 'cat': 'FTTH Betrieb', 'value': 300,
                  'desc': "Auf wie viele NE können die FAN Kosten aufgeteilt\
                           werden"},
                 # FTTS/B
                 {'name': 'mcan_wartung', 'cat': 'FTTSB', 'value': 25.47,
                  'desc': "Anteil an Wartungsvertrag HUAWEI für mCANs\
                           (proportional)"},
                 {'name': 'mcan_proacM', 'cat': 'FTTSB', 'value': 22.36},
                 {'name': 'mcan_logistik', 'cat': 'FTTSB', 'value': 4.63},
                 {'name': 'mcan_assurance_fixed', 'cat': 'FTTSB',
                  'value': 11.78,
                  'desc': "Anteil an Assurance fixed (380'000)"},
                 {'name': 'agg_strom', 'cat': 'FTTSB', 'value': 846.46},
                 {'name': 'agg_eff_bel', 'cat': 'FTTSB', 'value': 300,
                  'desc': "Auf wie viele NE können die Aggregator Stromkosten\
                           aufgeteilt werden"},
                 {'name': 'mcan_eff_bel', 'cat': 'FTTSB', 'value': 32},
                 # FTTB
                 {'name': 'mcan_assurance_fttb', 'cat': 'FTTB', 'value': 0.73},
                 # FTTS
                 {'name': 'mcan_assurance_ftts', 'cat': 'FTTS', 'value': 75.03},
                 ])


def load_defaults_old():
    return list([{'name': 'max_horizon', 'min': 12, 'max':  360,
                 'step': 4, 'value': 8*12},
                {'name': 'h_ob_fan_wartung', 'min': 0, 'max':  300,
                 'step': 1, 'value': 15},
                {'name': 'anzahl_ne', 'min': 0, 'max':  300,
                 'step': 1, 'value': 15},
                {'name': 'feeder_m', 'min': 0, 'max':  5000,
                 'step': 5, 'value': 600},
                {'name': 'drop_m', 'min': 0, 'max':  5000,
                 'step': 5, 'value': 20},
                {'name': 'h_capex', 'min': 0, 'max':  15000,
                 'step': 200, 'value': 2600},
                {'name': 'h_ob_omdf', 'min': 0, 'max':  10000,
                 'step': 200, 'value': 0},
                {'name': 'h_ob_fan', 'min': 0, 'max':  3000,
                 'step': 50, 'value': 300},
                {'name': 'h_ob_omdf_zi_mt', 'min': 0, 'max':  12,
                 'step': 1, 'value': 1},
                {'name': 'h_ob_fan_zi_mt', 'min': 0, 'max':  12,
                 'step': 1, 'value': 12},
                {'name': 'h_ob_omdf_beleg', 'min': 0, 'max':  1,
                 'step': 0.05, 'value': 0.8},
                {'name': 'h_ob_fan_beleg', 'min': 0, 'max':  1,
                 'step': 0.05, 'value': 0.8},
                {'name': 'h_ab_omdf_fr_yr', 'min': 0, 'max':  0.3,
                 'step': 0.02, 'value': 0.01},
                {'name': 'h_ab_omdf_fr_kosten', 'min': 0, 'max':  8000,
                 'step': 200, 'value': 20},
                {'name': 'h_ab_fan_fr_yr', 'min': 0, 'max':  1.0,
                 'step': 0.05, 'value': 0.04},
                {'name': 'h_ab_fan_fr_kosten', 'min': 0, 'max':  8000,
                 'step': 200, 'value': 200},
                {'name': 'h_ab_m1_fr_yr', 'min': 0, 'max':  0.3,
                 'step': 0.02, 'value': 0.01},
                {'name': 'h_ab_m1_fr_kosten', 'min': 0, 'max':  8000,
                 'step': 100, 'value': 10},
                {'name': 'h_ab_muffe_fr_yr', 'min': 0, 'max':  0.3,
                 'step': 0.02, 'value': 0.01},
                {'name': 'h_ab_muffe_fr_kosten', 'min': 0, 'max':  8000,
                 'step': 100, 'value': 100},
                {'name': 'h_e_omdf_kosten', 'min': 0, 'max':  80000,
                 'step': 2000, 'value': 50000},
                {'name': 'h_e_omdf_zi_mt', 'min': 0, 'max':  360,
                 'step': 6, 'value': 15*12},
                {'name': 'h_e_fan_kosten', 'min': 0, 'max':  80000,
                 'step': 2000, 'value': 4000},
                {'name': 'h_e_fan_zi_mt', 'min': 0, 'max':  360,
                 'step': 6, 'value': 15*12},
                {'name': 'h_e_m1_kosten_pm', 'min': 0, 'max':  200,
                 'step': 5, 'value': 15},
                {'name': 'h_e_m1_zi_mt', 'min': 0, 'max':  360,
                 'step': 6, 'value': 20*12},
                {'name': 'h_e_muffe_kosten', 'min': 0, 'max':  4000,
                 'step': 250, 'value': 1500},
                {'name': 'h_e_muffe_zi_mt', 'min': 0, 'max':  360,
                 'step': 6, 'value': 15*12},
                {'name': 'sb_capex', 'min': 0, 'max':  8000,
                 'step': 200, 'value': 800},
                {'name': 'sb_ob_strom_zi_mt', 'min': 1, 'max':  3,
                 'step': 1, 'value': 1},
                {'name': 'sb_ob_mcan', 'min': 0, 'max':  1000,
                 'step': 50, 'value': 25},
                {'name': 'sb_ob_mcan_zi_mt', 'min': 0, 'max':  12,
                 'step': 1, 'value': 12},
                {'name': 's_ab_mcan_fr_yr', 'min': 0, 'max':  3,
                 'step': 0.03, 'value': 0.03},
                {'name': 's_ab_mcan_fr_kosten', 'min': 0, 'max':  2000,
                 'step': 20, 'value': 1415},
                {'name': 's_ab_rpu_fr_yr', 'min': 0, 'max':  3,
                 'step': 0.03, 'value': 0.05},
                {'name': 's_ab_rpu_fr_kosten', 'min': 0, 'max':  2000,
                 'step': 20, 'value': 1500},
                {'name': 's_e_rpu_zi_mt', 'min': 0, 'max':  360,
                 'step': 1, 'value': 12*10},
                {'name': 's_e_rpu_kosten_pm', 'min': 0, 'max':  200,
                 'step': 5, 'value': 15},
                {'name': 'b_ab_mcan_fr_yr', 'min': 0, 'max':  1,
                 'step': 0.05, 'value': 0.0012},
                {'name': 'b_ab_mcan_fr_kosten', 'min': 0, 'max':  1000,
                 'step': 20, 'value': 660},
                {'name': 'kr_arpu_mt', 'min': 0, 'max':  200,
                 'step': 2, 'value': 80},
                {'name': 'kr_marktanteil', 'min': 0.1, 'max':  1,
                 'step': 0.01, 'value': 0.25},
                {'name': 'slider', 'min': 0, 'max':  360,
                 'step': 3, 'value': 60}])
