'__author__' == 'cyril'


import numpy as np


def monatsweise_zu_total(monatsweise):
    month = []
    for i, m in enumerate(monatsweise):
        month.append(monatsweise[:(i+1)].sum())
    return np.array(month)


def max_of_all(*args):
    maxx = 0
    for arg in args:
        m = arg.max()
        if m > maxx:
            maxx = m
    return maxx


def best_tech(f, s, b):
    m = max(f, s, b)
    if f == m:
        return 'FTTH'
    if s == m:
        return 'FTTS'
    if b == m:
        return 'FTTB'


def make_int(x):
    return int(x)


def make_array(inter_months, total_months):
    n_func = np.vectorize(make_int)
    t = np.arange(total_months+1)
    return n_func(t % inter_months == 0)[1:]
