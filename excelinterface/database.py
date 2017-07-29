'__author__' == 'cyril'


import csv
import sqlite3
import os


def get_real_type(a, form='sql'):
    """
    Function that takes a single string and decides if that string is a
    float, integer or actual string. Used for database type declaration.
    :param a: the string to consider
    :param form: what form the return should have. Default is 'sql' returns
    on of ['TEXT', 'INTEGER', 'REAL'], otherwise returns one of
    [str, int, float]
    :return: the real_type of input string either as string e.g. 'REAL' or as
    instance of type class e.g. str
    """
    if form == 'sql':
        typ_form = ['TEXT', 'INTEGER', 'REAL']
    else:
        typ_form = [str, int, float]
    real_type = typ_form[0]
    try:
        float(a)
        real_type = typ_form[2]
        if '.' not in a:
            real_type = typ_form[1]
    except ValueError:
        real_type = typ_form[0]
    return real_type


def get_col_info(csv_file):
    """
    Analyses first two rows of csv file to 1) get list of column names needed
    to create db table and 2) get the type of the column values.
    WARNING: if a cell of row 2 is empty, determining the type of this column
    will fail! ToDo: read rows until all column types are determine.
    :param csv_file: absolute path to csv file to be considered
    :return: Dictionary containing keys 'col_names' (with whitespaces striped
    for db usage), 'types' of columns, 'col_num' number of columns in csv file.
    """
    col_names = []
    types = []
    col_num = 0
    with open(csv_file) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            i += 1
            if i == 1:
                col_names = [r.replace(' ', '') for r in row]
                col_num = len(row)
            elif i == 2:
                for r in row:
                    types.append(get_real_type(r))
                assert len(types) == col_num, "Not same amount of columns."
            else:
                break
    return {'col_names': col_names, 'types': types, 'col_num': col_num}


def create_table(db_file, table_name, name_list, type_list):
    """
    Function to create a db table in given (and existing?) db_file from
    lists of column names and respective types (have to have same size)
    :param db_file: abs path where db-table is created (probably has to exist)
    :param table_name: name of table to be created.
    :param name_list: list of column names to be created.
    :param type_list: list with same lenght with respective types (strings
    like 'TEXT' etz.)
    :return: no return
    """
    assert len(name_list) == len(type_list), "Provided lists don't \
            have same length: {} names but {} types provided".format(
                len(name_list), len(type_list))
    query = ''
    for n, t in zip(name_list, type_list):
        query += "'{}' {}, ".format(n, t)
    query = query[:-2]

    connection = sqlite3.connect(db_file)
    connection.execute("DROP TABLE IF EXISTS {}".format(table_name))
    connection.commit()

    try:
        connection.execute("CREATE TABLE {}(ID INTEGER PRIMARY \
                            KEY AUTOINCREMENT NOT NULL, {});".format(
                                table_name, query))
        connection.commit()
        print("Table {} successfully created.".format(table_name))
    except sqlite3.OperationalError as err:
        print("Table couldn't be created! Error: {}".format(err))


def incert_into_table(db_file, table_name, name_list, type_list, value_list):
    """
    Function to incert a row into a sqlite3 db-table.
    :param db_file: abs path to db file
    :param table_name: name of existing table were values should be incerted.
    :param name_list: column names of table 'table_name' (Could rerwrite
    function such that this is not needed. ToDo)
    :param value_list: list of values to be incerted.
    :return: no return
    """
    assert len(name_list) == len(value_list), "Not same amount of columns \
            ({}) and values ({})".format(len(name_list), len(value_list))
    names = ''
    values = ''
    for n, v, t in zip(name_list, value_list, type_list):
        names += "'{}', ".format(n)
        if t == 'TEXT':
            values += "'{}', ".format(v.replace("'", ""))
        else:
            if v != '':
                values += v+', '
            else:
                values += "'', "
    insert = "INSERT INTO {} ({}) VALUES ({})".format(table_name,
                                                      names[:-2], values[:-2])

    connection = sqlite3.connect(db_file)
    try:
        connection.execute(insert)
    except sqlite3.OperationalError as err:
        print("Error: {}!!\nFailed to incert query \n{}.".format(err, insert))
        assert False
    connection.commit()


def csv_to_db(csv_file, table_name='Table'):
    """
    Function to save csv_file data into a sqlite3 db. Creates *.db file
    at same path as csv_file and save its data in there. Overwrites db if
    already exists.
    :param csv_file: abs path to csv file.
    :param table_name: name of the db-table that is created. Default: 'Table'.
    :return: no return
    """
    info = get_col_info(csv_file)
    os.system("touch {}".format(csv_file[:-3]+'db'))
    db_file = csv_file[:-3]+'db'
    name_list = info['col_names']
    type_list = info['types']
    create_table(db_file, table_name, name_list, type_list)
    with open(csv_file) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            i += 1
            if i == 1:
                continue
            else:
                incert_into_table(db_file, table_name, name_list,
                                  type_list, row)


def get_column_names(db_file, table_name):
    """
    Wrapper of db query to get column names of table 'table_name' in db
    'db_file'.
    :param db_file: abs path to db file.
    :param table_name: name of table which column names are to be fetched.
    :return: list of tabel column names if found.
    """
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info({})".format(table_name))
    all_info = cursor.fetchall()
    return [(a[1], a[2]) for a in all_info]


def search_query(db_file, query):
    """
    Wrapper to perform sqlite3 db querys. (Table name is contained in 'query').
    :param db_file: abs path of db file to query.
    :param query: string of exact db query to be performed.
    :return: list containing query results.
    """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    result = []
    for r in cur.execute(query):
        result.append(r)
    return result
