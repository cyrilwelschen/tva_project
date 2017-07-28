'__author__' == 'cyril'


import numpy as np
import corner
from tva_project.excelinterface import read_excels as re


def example():
    ndim, nsamples = 5, 10000
    samples = np.random.randn(ndim * nsamples).reshape([nsamples, ndim])
    # figure = corner.corner(samples)
    # figure.savefig("corner.png")
    return corner.corner(samples, bins=100, plot_contours=False)


def analyse(filename, regex_list, nr=20):
    data = []
    labels = []
    for col_name in regex_list:
        vals = re.values_of(filename, col_name, nr=nr)
        data.append([0 if v is None else v for v in vals[1:]])
        labels.append(vals[0])
    return corner.corner(np.array(data).T, plot_contours=False, bins=40,
                         labels=labels)
