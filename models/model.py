'__author__' == 'cyril'


import numpy as np
from matplotlib import pyplot as plt
from tva_project.models.model_helpers import make_array, monatsweise_zu_total


class Model(object):
    """
    Class describing modelling of total SC revenue over time
    """

    def __init__(self, sl):
        """
        Only parameter is a list of dictionaries: the factor dictionaries.
        """
        s = self
        for d in sl:
            setattr(s, d['name'], d['value'])

    def __getattr__(s, attr):
        print("WARNING: No value for {} found!!\
              Taking it to be 0.".format(attr))
        return 0

    """
    Tests
    """

    def factors(s):
        return vars(s)

    def test_two(s, a):
        return 2*a

    def test_plot(s):
        return s.test_two(s.f1) + s.f2 + s.f3

    def plot_test(s):
        """
        Create main Plot
        """
        x = np.arange(50)
        plt.plot(x, 2*x)
        plt.show()

    """
    H
    """

    def h_ob(s):
        return (s.fan_wartung + s.fan_strom
                + s.fan_proacM + s.fan_logistik + s.fan_assurance)\
                / s.fan_eff_bel * s.anzahl_ne * make_array(12, s.max_horizon)

    def mcan_ob(s):
        return (s.mcan_wartung + s.mcan_proacM
                + s.mcan_logistik + s.mcan_assurance_fixed) / s.mcan_eff_bel\
                * s.anzahl_ne * make_array(12, s.max_horizon)

    def mcan_ass(s, t):
        if t == 'b':
            return make_array(12, s.max_horizon) * s.mcan_assurance_fttb\
                   / s.mcan_eff_bel * s.anzahl_ne
        elif t == 's':
            return make_array(12, s.max_horizon) * s.mcan_assurance_ftts\
                   / s.mcan_eff_bel * s.anzahl_ne
        else:
            return 0 * make_array(12, s.max_horizon)

    def agg_ob(s):
        return make_array(12, s.max_horizon) * s.agg_strom / s.agg_eff_bel\
               * s.anzahl_ne

    """
    Plot
    """

# TODO: do factor class :-(
    def update_dependend_facs(s):
        if s.max_horizon < s.slider:
            s.slider = s.max_horizon

    def sum_mw(s):
        h_mw = s.h_ob()
        b_mw = s.mcan_ob() + s.agg_ob() + s.mcan_ass('b')
        s_mw = s.mcan_ob() + s.agg_ob() + s.mcan_ass('s')
        return {'FTTH': h_mw, 'FTTB': b_mw, 'FTTS': s_mw}

    def tot(s):
        mws = s.sum_mw()
        for t, val in zip(mws.keys(), mws.values()):
            mws[t] = monatsweise_zu_total(val) / s.anzahl_ne
        return mws

    def plot(s):
        """
        Create main Plot
        """
        s.update_dependend_facs()
        x = np.arange(s.max_horizon)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5))
        tot_d = s.tot()
        ymin, ymax = 0, 0
        for k, v in zip(tot_d.keys(), tot_d.values()):
            if v.min() < ymin:
                ymin = v.min()
            if v.max() > ymax:
                ymax = v.max()
            ax1.plot(x, v, label=k)
        print(ymin, ymax)
        ax1.vlines(s.slider, ymin, ymax)
        ax1.legend(loc="upper left")
        plt.savefig("../flaskinterface/static/plot.png")
