'__author__' == 'cyril'


import os

DATAPATH = "/home/cyril/Desktop/data_bix/"


def list_files(path=None):
    """
    List files and directories of path.
    :param path: path to directory for display
    :return list of directories and files sorted alphabetically.
    """
    path = analysed_path(path)
    file_list = os.listdir(path)
    file_list.sort()
    return file_list


def analysed_path(path):
    """
    Analyse if path is provided, and if so if its relative or not
    :param path: absolute or relative path or None
    :return usable absolute path
    """
    if not path:
        return DATAPATH
    elif path[:5] == "/home":
        return path
    else:
        return DATAPATH+path


def list_filetype(ending, path=None):
    """
    List files of specific type (i.e. ending) in directory.
    :param ending: string of ending with variable length. E.g. 'xls'
    :param path: absolute or relative path or None
    :return list of files with that endng.
    """
    all_files = list_files(path)
    xls = []
    for fl in all_files:
        if ending == fl[-len(ending):]:
            xls.append(fl)
    return xls


def list_xls(path=None):
    """
    List all excel files of old type.
    :param path: absolute, relative or None
    :return: list of xls files
    """
    return list_filetype("xls", path)


def list_xlsx(path=None):
    """
    List all excel files of new type.
    :param path: absolute, relative or None
    :return: list of xlsx files
    """
    return list_filetype("xlsx", path)


def list_all_excels(path=None, merge=True):
    """
    List(s) all excel files, old and new type.
    :param path: absolute, relative or None
    :param merge: whether to return old and new type excels in sparate list.
    Defaulte is returning a single list.
    :return: list or two lists of xls and xlsx files
    """
    if merge:
        return list_xls(path) + list_xlsx(path)
    else:
        return list_xls(path),  list_xlsx(path)


def strip_file_of_path(path_to_file):
    """
    Strip the file (last part) off of the absolute path.
    :param path_to_file: absolute path to a file e.g /home/cyril/test.png
    :return absolute path and file separatly e.g. /home/cyril/,  test.png
    """
    filename = os.path.basename(path_to_file)
    return path_to_file[:-len(filename)], filename


def convert_xls_to_xlsx(path_to_xls):
    from time import time as ti
    abs_path, filename = strip_file_of_path(path_to_xls)
    print("Converting {} to xlsx format...".format(filename), end="")
    t0 = ti()
    pwd = os.getcwd()
    os.chdir(abs_path)
    os.system("libreoffice --convert-to xlsx "+path_to_xls+" --headless")
    os.chdir(pwd)
    t1 = ti()
    print("Done ({} sec.)".format(round(t1-t0, 2)))
    xlsx_exist = os.path.exists(path_to_xls[:-3]+"xlsx")
    assert xlsx_exist, "Conversion of file {} failed".format(path_to_xls)


def convert_all_xls_to_xlsx(path=None):
    """
    converts all xls files in a directory to xlsx files
    :param path: abs or rel path or none.
    """
    basepath = analysed_path(path)
    for xls in list_xls(path):
        convert_xls_to_xlsx(basepath+"/"+xls)
    pass


def excels_by_regex(path):
    pass
