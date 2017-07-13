'__author__' == 'cyril'


import os
import xlrd
from openpyxl.workbook import Workbook
from openpyxl.reader.excel import load_workbook, InvalidFileException

DATAPATH = "/home/cyril/Desktop/data_bix/"


def list_files(path=None, **kwargs):
    """
    List available datafiles. By default relative to DATAPATH.
    :param path: relative path wrt DATAPATH
    :param relative: set to False to use absolute paths
    """
    path = analyse_path(path, **kwargs)
    file_list = os.listdir(path)
    file_list.sort()
    return file_list


def analyse_path(path, relative=True):
    if not path:
        path = DATAPATH
    elif relative:
        path = DATAPATH+path
    return path


def list_excels(path=None, convert=True, **kwargs):
    all_files = list_files(path=path, **kwargs)
    xls = []
    for fl in all_files:
        if (fl[-3:] == "xls") and convert:
            pwd = os.getcwd()
            path = analyse_path(path, relative=False)
            os.chdir(path)
            os.system("libreoffice --convert-to xlsx "+fl+" --headless")
            os.chdir(pwd)
            print("libreoffice --convert-to xlsx "+fl+" --headless")
            xls.append(fl[:-3]+"xlsx")
        if "xlxs" in fl:
            xls.append(fl)
    return xls


def excels_by_regex(path):
    pass


def open_xls_as_xlsx(filename):
    # first open using xlrd
    book = xlrd.open_workbook(filename)
    index = 0
    nrows, ncols = 0, 0
    while nrows * ncols == 0:
        sheet = book.sheet_by_index(index)
        nrows = sheet.nrows
        ncols = sheet.ncols
        index += 1
    # prepare a xlsx sheet
    book1 = Workbook()
    sheet1 = book1.get_active_sheet()
    for row in range(0, nrows):
        for col in range(0, ncols):
            sheet1.cell(row=row, column=col).value = sheet.cell_value(row, col)
    return book1


def convert_xls_to_xlsx(path_to_file, keep_original=True):
    filename = path_to_file
    # first open using xlrd
    book = xlrd.open_workbook(filename)
    index = 0
    nrows, ncols = 0, 0
    while nrows * ncols == 0:
        sheet = book.sheet_by_index(index)
        nrows = sheet.nrows
        ncols = sheet.ncols
        index += 1
    # prepare a xlsx sheet
    book1 = Workbook()
    sheet1 = book1.get_active_sheet()
    for row in range(0, nrows):
        for col in range(0, ncols):
            sheet1.cell(row=row, column=col).value = sheet.cell_value(row, col)
    return book1
