'__author__' == 'cyril'


from matplotlib import pyplot as plt
import numpy as np
from model_helpers import make_array
from model_helpers import monatsweise_zu_total as m2t
import sys
home = '/home/cyril/Dropbox/arbeit/swisscom/'\
        + 'Projekt3_RLA/Programming_venv/Programming'
sys.path += [home]
from tva_project.excelinterface.database import search_query


db_file = '/home/cyril/Desktop/slim_csv_2017-04-Alle_Daten.db'


"""
Factors
"""


class Slider(object):
    def __init__(self, s=12*2):
        self.s = s

    def set_v(self, new):
        self.s = new

    def v(self):
        return self.s


rez = "598051-199322"
nutzungseinheiten = 1
hori = 12*20
h_ob_fan = 521.7 + 1557.7 + 344.45 + 22.02  # Fan
h_as_fan = 253.13  # Fan
eff_b_fan = 576*0.75
h_rla_ne = 1.54  # NE

sb_ob_mcan = 25.47 + 22.36 + 4.63 + 11.78  # mCan
sb_ob_agg = 846.46  # Agg
eff_b_agg = 300
b_as_mcan = 0.73  # mCan
b_rla_mcan = 1300*0.05 + 50  # mCan
s_as_mcan = 75.03  # mCan
s_rla_mcan = 1300*0.05 + 200  # mCan
s_ob_mcan = 138  # mCan Strom
eff_b_mcan = 31

c_ob_can = 100.22 + 44.0 + 349.99 + 1136.26
c_as_can = 82.93
eff_b_can = 560*0.4


def horizon():
    return hori


def get_ne():
    return nutzungseinheiten


def look_for():
    return ['ReZ', 'NENutzungseinheitenTotal', 'WEWohneinheitenTotal',
            'PenetrationVerträgeRESWlineHSIanWETotal',
            'FTTHTotalproNE', 'FTTSBTotalproNE', 'KupferleitungslängezumCO']


def query(li=look_for()):
    query = ''
    for s in li:
        query += s+', '
    return query[:-2]


def search(rez):
    re = search_query(db_file, "SELECT {} from RezTable WHERE \
                      Rez LIKE '%{}%'".format(query(), rez))
    if len(re) != 1:
        print("Found multiple rez fitting the description: {}\n\n \
              Taking first by default".format(re))
    else:
        print("REE:", re[0])
        return re[0]


def rez_dic(rez):
    re = search(rez)
    rez_dic = {}
    for k, v in zip(look_for(), re):
        rez_dic[k] = v
    return rez_dic


def re_name(rez_dic):
    return rez_dic['ReZ'].split()[0]+' '+rez_dic['ReZ'].split()[1]


"""
Model
"""


def fan(ne=1):
    return (h_ob_fan + h_as_fan) / eff_b_fan * ne


def h_opex(ne=1):
    return fan(ne) + ne * h_rla_ne


def can(ne=1):
    return (c_ob_can + c_as_can) / eff_b_can * ne


def c_opex(ne=1):
    return can(ne) + agg(ne)


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
    return ['h', 's', 'b', 'c']


"""
Plot
"""


def k2a(kosten, interval):
    return make_array(interval, horizon()) * kosten


def m_nb2i_ne(t, ne=1):
    return m2t(eval('k2a('+t+'_opex({}), 12)'.format(ne)) / ne)


def rn(t):
    if t == 'h':
        return 'FTTH'
    if t == 'b':
        return 'FTTB'
    if t == 's':
        return 'FTTS'
    if t == 'c':
        return 'FTTC'


class LineBuilder:
    def __init__(self, line, ax):
        self.line = line
        self.ax = ax
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes != self.line.axes:
            return
        hans, lebs = self.ax.get_legend_handles_labels()
        new_lebs = []
        for h, l in zip(hans, lebs):
            y_temp = h.get_ydata()
            t_temp = l[3].lower()
            new_lebs.append(p_label(rn(t_temp), y_temp[int(event.xdata)]))
        self.ax.legend(hans, new_lebs)
        self.ax.set_title(p_tit(event.xdata))
        self.line.set_xdata(event.xdata)
        self.line.figure.canvas.draw()


def p_tit(mts):
    return "OPEX nach {} yr {} mt".format(int(mts // 12), int(mts % 12))


def p_label(n, chf):
    return "{}: {} CHF".format(n, round(chf, 2))


def ax1_plot(ax1, sli, x):
    for t in techs():
        y = m_nb2i_ne(t, get_ne())
        ax1.plot(x, y, label=p_label(rn(t), y[sli.v()]))
    ax1.set_title(p_tit(sli.v()))
    ax1.legend()
    vl = ax1.axvline(sli.v())
    LineBuilder(vl, ax1)


def plot_master(sli):
    plt.close()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
    x = np.arange(horizon())
    ax1_plot(ax1, sli, x)
    plt.show()
    return 0


"""
Main
"""
if __name__ == '__main__':
    print(search_query(db_file, "SELECT Rez from RezTable WHERE ID < 6"))
    plot_master(Slider())
    print(rez_dic(rez))
