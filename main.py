# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import sys
import os
import mariadb

import articoli
import clienti
import commissione
import database

# The lines below enable the Windoes version of Python to correctly load
# the native libraries from the current working directory see:
# https://docs.python.org/3/whatsnew/3.8.html#bpo-36085-whatsnew
if os.name == 'nt':
    if sys.version_info >= (3, 6, 0):
        sys.path.append(os.getcwd())
    if sys.version_info >= (3, 8, 0):
        os.add_dll_directory(os.getcwd())

import pyctree

global conn
global cur
global mariadb_cur

def main():
    init()

    # clienti.exportClienti(cur, mariadb_cur)
    commissione.export(cur, mariadb_cur)
    commit()

    # select()
    #
    # manage()
    #
    #
    # if sys.version_info >= (3, 0, 0):
    #     input("Press <ENTER> key to exit . . .")
    # else:
    #     raw_input("Press <ENTER> key to exit . . .")

    return


def init():
    global conn
    global mariadb_conn
    global cur

    global mariadb_cur

    print('Init\n')
    print("\tLogon to server...")

    try:
        conn = pyctree.connect(user='ADMIN', password='ADMIN', database='test', host='127.0.0.1', port='6597')
        cur = conn.cursor()

        mariadb_conn = database.get_mysql_connection()
    except Exception as e:
        Handle_Exception(e)

    mariadb_cur = mariadb_conn.cursor()
    return

def commit():
    mariadb_conn.commit()
    return


def select():
    print("\tExecuting select...")

    cur.execute("SELECT admin.com.commessa, admin.com.data_commessa FROM admin.com")
    rows = cur.fetchall()
    for row in rows:
        ##print(row)
        print(row[0],row[1],convertDate(row[1]))

    return


def done():
    print('Done\n')

    if cur:
        cur.close()

    print("\tLogout...");
    if conn:
        conn.close()

    return;

def Handle_Exception(e):
    if e.args[0] == -20005:
        return
    else:
        print("error", e)
        if e.args[0] == -20212:
            print("Perhaps your c-tree server is not running?")
        print("*** Execution aborted *** \nPress <ENTER> key to exit...")
        sys.exit(1)


main()

