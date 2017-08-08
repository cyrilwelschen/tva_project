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
    def __init__(self, s=12*5):
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
        return re[0]


def rez_dic(rez):
    re = search(rez)
    rez_dic = {}
    for k, v in zip(look_for(), re):
        rez_dic[k] = v
    return rez_dic


rd = rez_dic(rez)


def re_name(rez_dic):
    return rez_dic['ReZ'].split()[0]+' '+rez_dic['ReZ'].split()[1]


"""
Model
"""


def techs():
    return ['h', 's', 'b', 'c']


def fan(ne=1):
    return (h_ob_fan + h_as_fan) / eff_b_fan * ne


def mcan(ne=1, t='ftts'):
    both = sb_ob_mcan
    if t == 'fttb':
        return (both + b_as_mcan + b_rla_mcan) / eff_b_mcan * ne
    elif t == 'ftts':
        return (both + s_as_mcan + s_rla_mcan + s_ob_mcan) / eff_b_mcan * ne


def agg(ne=1):
    return sb_ob_agg / eff_b_agg * ne


def can(ne=1):
    return (c_ob_can + c_as_can) / eff_b_can * ne


def h_opex(ne=1):
    return fan(ne) + ne * h_rla_ne


def s_opex(ne=1):
    return mcan(ne, 'ftts') + agg(ne)


def b_opex(ne=1):
    return mcan(ne, 'fttb') + agg(ne)


def c_opex(ne=1):
    return can(ne) + agg(ne)


def k2a(kosten, interval):
    return make_array(interval, horizon()) * kosten


def m_nb2i_ne(t, ne=1):
    return m2t(eval('k2a('+t+'_opex({}), 12)'.format(ne)) / ne)


"""
Plot
"""


def rn(t):
    if t == 'h':
        return 'FTTH'
    if t == 'b':
        return 'FTTB'
    if t == 's':
        return 'FTTS'
    if t == 'c':
        return 'FTTC'


def cap(t):
    if t == 'h':
        return rd['FTTHTotalproNE']
    if t == 'b':
        return rd['FTTSBTotalproNE']
    if t == 's':
        return rd['FTTSBTotalproNE']
    if t == 'c':
        return 0


def rev(t):
    n = 'PenetrationVerträgeRESWlineHSIanWETotal'
    if t == 'h':
        return 95.97 * (rd[n] + 0.011)
    if t == 'b':
        return 94.38 * (rd[n] + 0.007)
    if t == 's':
        return 94.38 * rd[n]
    if t == 'c':
        return 92.71 * rd[n]


class LineBuilderAx1:
    def __init__(self, line, ax, tit="OPEX"):
        self.line = line
        self.tit = tit
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
        self.ax.set_title(p_tit(event.xdata, self.tit))
        self.line.set_xdata(event.xdata)
        self.line.figure.canvas.draw()


def p_tit(mts, tit="OPEX"):
    return "{} nach {} yr {} mt".format(tit, int(mts // 12), int(mts % 12))


def p_label(n, chf):
    return "{}: {} CHF".format(n, round(chf, 2))


def ax1_plot(ax1, sli, x):
    tit = "OPEX"
    for t in techs():
        y = m_nb2i_ne(t, get_ne())
        ax1.plot(x, y, label=p_label(rn(t), y[sli.v()]))
    ax1.set_title(p_tit(sli.v()))
    ax1.set_xlabel("Monate")
    ax1.set_ylabel(tit.split()[0]+" [CHF]")
    ax1.legend()
    vl = ax1.axvline(sli.v())
    LineBuilderAx1(vl, ax1)


def ax2_plot(ax, sli, x):
    tit = "Ertrag"
    for t in techs():
        y = m2t(k2a(rev(t), 1)) - m_nb2i_ne(t, get_ne()) - cap(t)
        ax.plot(x, y, label=p_label(rn(t), y[sli.v()]))
    ax.set_title(p_tit(sli.v(), tit=tit))
    ax.set_xlabel("Monate")
    ax.set_ylabel(tit.split()[0]+" [CHF]")
    ax.legend()
    vl = ax.axvline(sli.v())
    LineBuilderAx1(vl, ax, tit=tit)


def ax3_plot(ax, sli, x):
    tit = "Ertrag mit Budgetopportunität"
    for t in techs():
        y = m2t(k2a(rev(t), 1)) - m_nb2i_ne(t, get_ne()) - cap(t)- m2t(k2a(cap(t) * 0.01, 1))
        ax.plot(x, y, label=p_label(rn(t), y[sli.v()]))
    ax.set_title(p_tit(sli.v(), tit=tit))
    ax.set_xlabel("Monate")
    ax.set_ylabel(tit.split()[0]+" [CHF]")
    ax.legend()
    vl = ax.axvline(sli.v())
    LineBuilderAx1(vl, ax, tit=tit)


def opp_cap_plot(anz_ne, capex_diff):
    diff_h_sb = capex_diff * anz_ne # (cap_h -cap_sb) * ne_neubau [[Geld das in Budget bleibt]]
    opp_sb = diff_h_sb/1062
    opp_h = diff_h_sb/3842
    ch_h_anteil = 0.3
    ch_sb_anteil = 0.7
    ma = rd['PenetrationVerträgeRESWlineHSIanWETotal']
    opp_erwartung = ch_h_anteil*opp_h*ma*94 + ch_sb_anteil*opp_sb*ma*93
    return opp_erwartung/anz_ne


def t2m(monatsweise):
    monatsweise = np.array(monatsweise)
    month = [0]
    for i in np.arange(len(monatsweise)-1):
        if i < len(monatsweise):
            month.append(monatsweise[(i+1)] - monatsweise[i])
    return np.array(month)


def forma(h,s,t,i, p):
    n = []
    for i, vs, vh in zip(np.arange(len(s)), s, h):
        if i < t:
            n.append(vs)
        elif i == t:
            n.append(vs - i)
        else:
            n.append(vh*p + vs*(1-p))
    return np.array(n)


def ax4_plot(ax, x):
    from mpl_toolkits.mplot3d import axes3d
    le = len(x)
    X = np.array(le*list(x)).reshape(le, le)
    y = np.linspace(0,1,le)
    Y = np.array(le*list(y)).reshape(le, le).T
    Zs = []
    tim = 4*12 # index when ngPON happens # sprung
    ink_cap = 600 + rd['FTTHTotalproNE']/2
    h_y = m2t(k2a(rev('h'), 1)) - m_nb2i_ne('h', get_ne()) - cap('h') - m2t(k2a(cap('h') * 0.01, 1))
    s_y = m2t(k2a(rev('s'), 1)) - m_nb2i_ne('s', get_ne()) - cap('s') - m2t(k2a(cap('s') * 0.01, 1))
    h_ym = t2m(h_y)
    s_ym = t2m(s_y)
    z_data = []
    for p in y:
        z = np.array(m2t(forma(h_ym, s_ym, tim, ink_cap, p)))
        z_data.append(z)
    Z = np.array(list(z_data)).reshape(le, le)
    Zs.append(Z)
    for t in ['h']:
        z = m2t(k2a(rev(t), 1)) - m_nb2i_ne(t, get_ne()) - cap(t)- m2t(k2a(cap(t) * 0.01, 1))
        for i in x:
            z = m2t(k2a(rev(t), 1)) - m_nb2i_ne(t, get_ne()) - cap(t)- m2t(k2a(cap(t) * 0.01, 1))
            Z = np.array(le*list(z)).reshape(le, le)
        Zs.append(Z)
    for big_z, c in zip(Zs, ['orange', 'b']):
        ax.plot_wireframe(X, Y, big_z, rstride=10, cstride=30, color=c)


def plot_master(sli):
    from mpl_toolkits.mplot3d import Axes3D
    rez_d = rez_dic(rez)
    plt.close()
    # fig, (ax12, ax34) = plt.subplots(2, 2, figsize=(6, 6))
    fig = plt.figure(figsize=(4,4))
    # ax1, ax2 = ax12
    # ax3, ax4 = ax34
    ax1 = fig.add_subplot(2,2,1)
    ax2 = fig.add_subplot(2,2,2)
    ax3 = fig.add_subplot(2,2,3)
    ax4 = fig.add_subplot(2,2,4, projection='3d')
    fig.suptitle(re_name(rez_d), fontsize=16)
    x = np.arange(horizon())
    ax1_plot(ax1, sli, x)
    ax2_plot(ax2, sli, x)
    ax3_plot(ax3, sli, x)
    ax4_plot(ax4, x)
    plt.show()
    return 0


"""
Main
"""
if __name__ == '__main__':
    print(search_query(db_file, "SELECT Rez from RezTable WHERE ID < 6"))
    plot_master(Slider())
