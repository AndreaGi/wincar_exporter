# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import sys
import os
import mariadb
import clienti


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
    clienti.exportClienti(cur, mariadb_cur)
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

        mariadb_conn = mariadb.connect(
            user="root",
            password="6qzlkE3B6hm&",
            host="167.235.53.57",
            port=3306,
            database="officina_dev"
        )
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


def convertDate(byte):
    date = ""
    print(byte[0])
    print(byte[1])
    print(byte[2])
    match byte[0]:
        case 153:
            date = "1999"
        case 160:
            date = "2000"
        case 161:
            date = "2001"
        case 162:
            date = "2002"
        case 163:
            date = "2003"
        case 164:
            date = "2004"
        case 165:
            date = "2005"
        case 166:
            date = "2006"
        case 167:
            date = "2007"
        case 168:
            date = "2008"
        case 169:
            date = "2009"
        case 176:
            date = "2010"
        case 177:
            date = "2011"
        case 178:
            date = "2012"
        case 179:
            date = "2013"
        case 180:
            date = "2014"
        case 181:
            date = "2015"
        case 182:
            date = "2016"
        case 183:
            date = "2017"
        case 184:
            date = "2018"
        case 185:
            date = "2019"
        case 192:
            date = "2020"
        case 193:
            date = "2021"
        case 194:
            date = "2022"
        case 195:
            date = "2023"

    match byte[1]:
        case 1:
            date = date + "/01/"
        case 2:
            date = date + "/02/"
        case 3:
            date = date + "/03/"
        case 4:
            date = date + "/04/"
        case 5:
            date = date + "/05/"
        case 6:
            date = date + "/06/"
        case 7:
            date = date + "/07/"
        case 8:
            date = date + "/08/"
        case 9:
            date = date + "/09/"
        case 16:
            date = date + "/10/"
        case 17:
            date = date + "/11/"
        case 18:
            date = date + "/12/"

    match byte[2]:
        case 1:
            date = date + "01"
        case 2:
            date = date + "02"
        case 3:
            date = date + "03"
        case 4:
            date = date + "04"
        case 5:
            date = date + "05"
        case 6:
            date = date + "06"
        case 7:
            date = date + "07"
        case 8:
            date = date + "08"
        case 9:
            date = date + "09"
        case 16:
            date = date + "10"
        case 17:
            date = date + "11"
        case 18:
            date = date + "12"
        case 19:
            date = date + "13"
        case 20:
            date = date + "14"
        case 21:
            date = date + "15"
        case 22:
            date = date + "16"
        case 23:
            date = date + "17"
        case 24:
            date = date + "18"
        case 25:
            date = date + "19"
        case 32:
            date = date + "20"
        case 33:
            date = date + "21"
        case 34:
            date = date + "22"
        case 35:
            date = date + "23"
        case 36:
            date = date + "24"
        case 37:
            date = date + "25"
        case 38:
            date = date + "26"
        case 39:
            date = date + "27"
        case 40:
            date = date + "28"
        case 41:
            date = date + "29"
        case 48:
            date = date + "30"
        case 49:
            date = date + "31"

    return date



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

