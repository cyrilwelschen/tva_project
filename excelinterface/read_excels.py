'__author__' == 'cyril'


from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

from tva_project.utils import filesystem as fs


def datapath():
    """
    Info about default datapath
    :return string of default datapath
    """
    return fs.datapath()


def load_wb(filename):
    """
    Get list of worksheet names of an xlsx file.
    :param filename: path to file
    :return list of filenames
    """
    try:
        wb = load_workbook(filename, read_only=True)
    except FileNotFoundError:
        print("File {} not found.".format(filename))
    except:
        print("Faild to load file {}".format(filename))
        raise
    else:
        return wb


def get_sheetnames(workbook):
    """
    List of worksheets found for workbook.
    :param workbook: openpyxl workbook instance
    :return list of found worksheet names
    """
    return workbook.get_sheet_names()


def default_ws_names():
    return ["ReZ-ReZType", "All_Data_ReZ"]


def try_find_column_names(filename, overwrite_ws_name=None):
    """
    Try to find relevant worksheet colunm names.
    :param filename: path to filename.
    :param overwrite_ws_name: Optional name of worksheet to use instead of
    default list: default_ws_names()
    :return list of proposed column names.
    """
    wb = load_wb(filename)
    name_proposal = overwrite_ws_name or default_ws_names()
    wb_sheet_names = get_sheetnames(wb)
    name = None
    if isinstance(name_proposal, str):
        if name_proposal in wb_sheet_names:
            name = name_proposal
    else:
        print("else")
        for name_prop in name_proposal:
            if name_prop in wb_sheet_names:
                name = name_prop
    try:
        ws = wb[name]
    except NameError:
        print("Couldn't find worksheet {}. Found {}".format(name,\
                                                            get_sheetnames(wb)))
    else:
        return [c.value for c in ws[1]]
