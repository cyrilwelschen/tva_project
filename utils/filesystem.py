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


def convert_xls_to_xlsx(path_to_xls, overwrite=False):
    """
    Converts an xls file to a xlsx file using liberaoffice and places its
    in same directory as original one. Original one not deleted.
    :param path_to_xls: absolute path to xls filename
    :param overwrite: if True converts file again. Default: converts only if
    no matching .xlsx file in same folder found.
    """
    abs_path, filename = strip_file_of_path(path_to_xls)
    files = list_xlsx(abs_path)
    if (not overwrite) and (filename[:-3]+"xlsx" in files):
        print("File {} already converted. Pass!".format(filename))
    else:
        from time import time as ti
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


def convert_all_xls_to_xlsx(path=None, **kwargs):
    """
    converts all xls files in a directory to xlsx files
    :param path: abs or rel path or none.
    """
    basepath = analysed_path(path)
    for xls in list_xls(path):
        convert_xls_to_xlsx(basepath+"/"+xls, **kwargs)
    pass


def datapath():
    """
    Info about default datapath
    :return string of default datapath
    """
    return DATAPATH


def all_excels(filetype='xlsx'):
    """
    List all xlsx files ready for read in directories below 'datapath'
    :param filetype: Default xlsx. Other options: 'xls' or 'both'
    :return list of absolute path of all xlsx files in directorytree
    relative to 'datapath'
    """
    all_dirs = [x[0] for x in os.walk(DATAPATH)]
    list_of_all = []
    for dir in all_dirs:
        if filetype == 'xlsx':
            in_dir_list = list_xlsx(dir)
        elif filetype == 'xls':
            in_dir_list = list_xls(dir)
        else:
            in_dir_list = list_all_excels(dir)
        for f in in_dir_list:
            list_of_all.append(dir+"/"+f)
    return list_of_all


def find_by_regex(regex, from_list=None, real_regex=False, filetype='xlsx'):
    """
    Make a new list of files that match a regex of an original list of files.
    :param regex: the regex or part of the filename to look for, also list of
    filename parts is possible.
    :param from_list: original list of files, default is all excels below
    datapath base directory.
    :param real_regex: If param 'regex' is a real regular expression or just
    a part of the filename. Default is False, i.e. just a substring.
    :param filetype: Default xlsx. Other options: 'xls' or 'both'
    :return list of paths to files that match regex.
    """
    all = from_list or all_excels(filetype)
    found_reg = []
    for f in all:
        if isinstance(regex, str):
            if regex in f:
                found_reg.append(f)
        elif isinstance(regex, list):
            found = True
            for r in regex:
                if r not in f:
                    found = False
            if found:
                found_reg.append(f)
        else:
            print("Unsupported 'regex' parameter type")
    return found_reg
