'__author__' == 'cyril'


import os

DATAPATH = "/home/cyril/Desktop/data_bix/"


def list_files(path=None, relative=True):
    """
    List available datafiles. By default relative to DATAPATH.
    :param path: relative path wrt DATAPATH
    :param relative: set to False to use absolute paths
    """
    if not path:
        path = DATAPATH
    elif relative:
        path = DATAPATH+path
    return os.listdir(path)


def list_excels(path=None, **kwargs):
    all_files = list_files(path=path, **kwargs)
    xls = []
    for fl in all_files:
        if ("xls" in fl) or ("xlxs" in fl):
            xls.append(fl)
    return xls


def excels_by_regex(path):
    pass
