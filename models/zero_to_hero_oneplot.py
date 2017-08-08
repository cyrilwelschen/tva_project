'__author__' == 'cyril'


from matplotlib import pyplot as plt
import numpy as np
from model_helpers import make_array
from model_helpers import monatsweise_zu_total as m2t
import sys
sys.path.append("../.")
from tva_project.excelinterface.database import search_query

db_file = '/home/cyril/Desktop/slim_csv_2017-04-Alle_Daten.db'


"""
Factors
"""
rez = "asdf"
nutzungseinheiten = 1
hori = 12*20
h_ob_fan = 521.7 + 1557.7 + 344.45 + 22.02  # Fan
h_as_fan = 253.13  # Fan
eff_b_fan = 432
h_rla_ne = 1.54  # NE

sb_ob_mcan = 25.47 + 22.36 + 4.63 + 11.78  # mCan
sb_ob_agg = 846.46  # Agg
eff_b_agg = 300
b_as_mcan = 0.73  # mCan
b_rla_mcan = 1300*0.05 + 50  # mCan
s_as_mcan = 75.03  # mCan
s_rla_mcan = 1300*0.05 + 200  # mCan
s_ob_mcan = 138  # mCan Strom
eff_b_mcan = 32


def horizon():
    return hori


def get_ne():
    return nutzungseinheiten


"""
Model
"""


def fan(ne=1):
    return (h_ob_fan + h_as_fan) / eff_b_fan * ne


def h_opex(ne=1):
    return fan(ne) + ne * h_rla_ne


def mcan(ne=1, t='ftts'):
    both = sb_ob_mcan
    if t == 'fttb':
        return (both + b_as_mcan + b_rla_mcan) / eff_b_mcan * ne
    elif t == 'ftts':
        return (both + s_as_mcan + s_rla_mcan + s_ob_mcan) / eff_b_mcan * ne


def agg(ne=1):
    return sb_ob_agg / eff_b_agg * ne


def s_opex(ne=1):
    return mcan(ne, 'ftts') + agg(ne)


def b_opex(ne=1):
    return mcan(ne, 'fttb') + agg(ne)


def techs():
    return ['h', 's', 'b']


"""
Plot
"""


def k2a(kosten, interval):
    return make_array(interval, horizon()) * kosten


def m_nb2i_ne(t, ne=1):
    return m2t(eval('k2a('+t+'_opex({}), 12)'.format(ne)) / ne)


def plot():
    plt.close()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
    x = np.arange(horizon())
    for t in techs():
        y = m_nb2i_ne(t, get_ne())
        ax1.plot(x, y, label=t)
    plt.show()
    return 0


"""
Main
"""
if __name__ == '__main__':
    print(search_query(db_file, "SELECT Rez from RezTable WHERE ID < 6"))
    for t in techs():
        print("ftt{}".format(t), eval(t+'_opex()'))
    plot()
