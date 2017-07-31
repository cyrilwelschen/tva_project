'__author__' == 'cyril'


from flask import Flask, request, render_template
import pickle


app = Flask(__name__)


@app.route('/')
def home():
    return "Hello from TVA home"


@app.route('/projects/<project_name>', methods=['GET', 'POST'])
def mainpage(project_name='Default'):
    return "No project with name '{}' yet.".format(project_name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return "Login was correct."
        else:
            error = 'Invalid username/password. Please try again.'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


def valid_login(usrname, password):
    if usrname == 'cyril':
        return True
    else:
        return False


@app.route('/inout', methods=['POST', 'GET'])
def in_out_func(val=None):
    if request.method == 'POST':
        if request.form['input_value']:
            return render_template('value_in_out.html',
                                   val=request.form['input_value'])
    else:
        return render_template('value_in_out.html')


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


def delete():
    pass


@app.route('/sliders', methods=['POST', 'GET'])
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
