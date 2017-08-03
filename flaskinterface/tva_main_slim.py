'__author__' == 'cyril'


from flask import Flask, request, render_template
import pickle


app = Flask(__name__)


def generate_test_factors():
    slider_dics_list = []
    for i in range(20):
        sd = {'name': 'factor+i', 'min': 10+i, 'max': 20+i,
              'value': 15+i, 'step': 1}
        slider_dics_list.append(sd)
    return slider_dics_list


def default_slider():
    default = load_defaults()
    sd = {'name': 'dummy factor', 'min': 0, 'max': 100,
          'value': 50, 'step': 10}
    sd1 = {'name': 'dummy fac', 'min': 0, 'max': 200,
           'value': 50, 'step': 10}
    sd2 = {'name': 'dummy fac3', 'min': 0, 'max': 200,
           'value': 150, 'step': 10}
    return default + [sd, sd1, sd2]


def initial_put():
    with open('dummy.txt', 'wb') as f:
        pickle.dump(default_slider(), f)
    return default_slider()


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


def dummy_db_put_single(req_form):
    db_dic = dummy_db_get()
    new_dic = []
    for f in db_dic:
        f_name = f['name']
        f['value'] = req_form[f_name+'f']
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
        return render_template('main_slim.html', sliders=sliders)
    else:
        sliders = initial_put()
        return render_template('main_slim.html', sliders=sliders)


def load_defaults():
    return list([{'name': 'max_horizon', 'min': 12, 'max':  360,
                 'step': 4, 'value': 8*12},
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
