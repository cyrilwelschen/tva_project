'__author__' == 'cyril'


from flask import Flask, request, render_template
import pickle
import os


app = Flask(__name__)



def generate_test_factors():
    slider_dics_list = []
    for i in range(20):
        sd = {'name': 'factor+i', 'min': 10+i, 'max': 20+i,
              'value': 15+i, 'step': 1}
        slider_dics_list.append(sd)
    return slider_dics_list


def default_slider():
    sd = {'name': 'dummy factor', 'min': 0, 'max': 100,
          'value': 50, 'step': 10}
    sd1 = {'name': 'dummy fac', 'min': 0, 'max': 200,
          'value': 50, 'step': 10}
    sd2 = {'name': 'dummy fac3', 'min': 0, 'max': 200,
          'value': 150, 'step': 10}
    return [sd, sd1, sd2]


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
        factor_names = list(set([i[:-1] for i in request.form]))
        print(factor_names)
        sliders = dummy_db_put(request.form)
        return render_template('main_slim.html', sliders=sliders)
    else:
        sliders = initial_put()
        return render_template('main_slim.html', sliders=sliders)
