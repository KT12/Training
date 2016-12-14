#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 18:11:29 2016

@author: ktt
"""

import sqlite3

def connect(sqlite_file):
    # connects to SQLIite db file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c
    
def close(conn):
    # closes conneciton to db
    conn.close()
    
def total_rows(c, table_name, print_out=False):
    # returns total number of rows in the db
    c.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = c.fetchall()
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]

def table_col_info(c, table_name, print_out=False):
    # returns list of tuples with col info
    c.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = c.fetchall()
    
    if print_out:
        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)
    return info

def values_in_col(c, table_name, print_out=True):
    # returns a dict with columns as keys and number of not_null entries
    # as associated values
    
    c.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = c.fetchall()
    col_dict = dict()
    for col in info:
        col_dict[col[1]] = 0
    for col in col_dict:
        c.execute('SELECT ({0}) FROM {1} WHERE {0} IS NOT NULL'.format(col, table_name))
        number_rows = len(c.fetchall())
        col_dict[col] = number_rows
    if print_out:
        print("\nNumber of entries per column:")
        for i in col_dict.items():
            print('{}: {}'.format(i[0], i[1]))
    return col_dict

if __name__ == '__main__':
    sqlite_file = 'my_first_db.sqlite'
    table_name = 'my_table_3'
    
    conn, c = connect(sqlite_file)
    total_rows(c, table_name, print_out=True)
    table_col_info(c, table_name, print_out=True)
    values_in_col(c, table_name, print_out=True)
    
    close(conn)