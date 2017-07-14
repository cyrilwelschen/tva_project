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
