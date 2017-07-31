'__author__' == 'cyril'


from flask import Flask, request, render_template
import pickle
import os
import sqlite3


app = Flask(__name__)


"""
DB stuff
"""


DB_FILE = "factor_db.db"


def create_table_if_unexists(db_f=None):
    """
    Checks if factor db exists and creates it if it doesn't
    """
    if not db_f:
        db_f = DB_FILE
    if not os.path.exists(db_f):
        os.system("touch "+db_f)
        conn = sqlite3.connect(db_f)
        conn.execute("CREATE TABLE factors(ID INTEGER PRIMARY KEY \
                     AUTOINCREMENT NOT NULL, project TEXT, factor TEXT, \
                     min FLOAT, max FLOAT, value FLOAT, step FLOAT, \
                     description TEXT, \
                     usage TEXT);")
        conn.commit()


def create_new_factor(f):
    """
    Creates a new factor (new row in db)
    """
    assert isinstance(f, list), "Should be a list"
    ins = ''
    for i in f:
        ins += f+', '
    ins = ins[:-2]
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO factors (project, factor, min, max, value, \
                 step, description, usage) VALUES ({})".format(ins))


def update_factor():
    """
    Updates certain value of existing factor.
    """
    pass


def lookup_factor():
    """
    Get all values of a factor
    """
    pass


def save_all_info_as_project():
    """
    Save all factors and other stuff (idea: perspective of one person)
    """
    pass


"""
Test dummy stuff
"""


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
    return sd


def initial_put():
    with open('dummy.txt', 'wb') as f:
        pickle.dump(default_slider(), f)
    return default_slider()


def dummy_db_put(new_val1, new_val2):
    db_dic = dummy_db_get()
    old_val = db_dic['value']
    new_val = 0
    if old_val == new_val1:
        new_val = new_val2
    else:
        new_val = new_val1
    db_dic['value'] = new_val
    with open('dummy.txt', 'wb') as f:
        pickle.dump(db_dic, f)
    return db_dic


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
        print(request.form)
        print(request.form['in_val_range'])
        print(request.form['in_val_form'])
        slider_dic = dummy_db_put(request.form['in_val_form'],
                                  request.form['in_val_range'])
        print("NEW:  ", slider_dic['value'])
        return render_template('range_auto_test.html', slider_dic=slider_dic)
    else:
        slider_dic = initial_put()
        return render_template('range_auto_test.html', slider_dic=slider_dic)
