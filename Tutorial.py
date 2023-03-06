import datetime
import sys
import os

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

'''
    tutorial2.py

    Public domain Python SQL example

    FairCom Corporation, 6300 West Sugar Creek Drive, Columbia, MO 65203 USA

    The goal of this tutorial is to introduce the most basic Python SQL commands
    to accomplish creating and manipulating a table through the ctreeServer

    Functionally, this application will perform the following:
     1.  Create a database
     2.  Create 4 tables each with an index
     3.  Populate each table with a few records
     4.  Build a query utilizing the advantage of indexes
     5.  Output the results of the query
'''

'''
  Main()

  The main() function implements the concept of "init, define, manage
  and you're done... '
'''


def main():
    init()

    define()

    manage()

    done()

    if sys.version_info >= (3, 0, 0):
        input("Press <ENTER> key to exit . . .")
    else:
        raw_input("Press <ENTER> key to exit . . .")

    return;


'''
   Initialize()

   Perform the minimum requirement of logging onto the c-tree Server
'''


def init():
    global conn
    global cur

    print('Init\n')
    print("\tLogon to server...")

    try:
        conn = pyctree.connect(user='ADMIN', password='ADMIN', database='ctreeSQL', host='127.0.0.1', port='6597')
        cur = conn.cursor()
    except Exception as e:
        Handle_Exception(e)

    return;


'''
   Define()

   Create the table for containing a list of existing customers
'''


def define():
    print('Define\n')

    try:
        print("\tDropping ordritem")
        cur.execute("DROP TABLE ordritem")
    except Exception as e:
        Handle_Exception(e)

    try:
        print("\tDropping custordr")
        cur.execute("DROP TABLE custordr")
    except Exception as e:
        Handle_Exception(e)

    try:
        print("\tDropping itemmast")
        cur.execute("DROP TABLE itemmast")
    except Exception as e:
        Handle_Exception(e)

    try:
        print("\tDropping custmast")
        cur.execute("DROP TABLE custmast")
    except Exception as e:
        Handle_Exception(e)

    try:
        ''' create CustomerMaster table '''
        print("\tCreate CustomerMaster table...")
        cur.execute("CREATE TABLE custmast (" +
                    "cm_custnumb CHAR(4), " +
                    "cm_custzipc CHAR(9), " +
                    "cm_custstat CHAR(2), " +
                    "cm_custrtng CHAR(1), " +
                    "cm_custname VARCHAR(47), " +
                    "cm_custaddr VARCHAR(47), " +
                    "cm_custcity VARCHAR(47))"
                    )
        cur.execute("CREATE UNIQUE INDEX cm_custnumb_idx ON custmast (cm_custnumb)")

        ''' create CustomerOrders table '''
        print("\tCreate CustomerOrders table...")
        cur.execute("CREATE TABLE custordr (" +
                    "co_ordrdate DATE, " +
                    "co_promdate DATE, " +
                    "co_ordrnumb CHAR(6), " +
                    "co_custnumb CHAR(4))"
                    )
        cur.execute("CREATE UNIQUE INDEX co_ordrnumb_idx ON custordr (co_ordrnumb)")
        cur.execute("CREATE INDEX co_custnumb_idx ON custordr (co_custnumb)")

        ''' create OrderItems table '''
        print("\tCreate OrderItems table...")
        cur.execute("CREATE TABLE ordritem (" +
                    "oi_sequnumb SMALLINT, " +
                    "oi_quantity SMALLINT, " +
                    "oi_ordrnumb CHAR(6), " +
                    "oi_itemnumb CHAR(5))"
                    )
        cur.execute("CREATE UNIQUE INDEX oi_ordrnumb_idx ON ordritem (oi_ordrnumb, oi_sequnumb)")
        cur.execute("CREATE INDEX oi_itemnumb_idx ON ordritem (oi_itemnumb)")

        ''' create ItemMaster table '''
        print("\tCreate ItemMaster table...")
        cur.execute("CREATE TABLE itemmast (" +
                    "im_itemwght INTEGER, " +
                    "im_itempric MONEY, " +
                    "im_itemnumb CHAR(5), " +
                    "im_itemdesc VARCHAR(47))"
                    )
        cur.execute("CREATE UNIQUE INDEX im_itemnumb_idx ON itemmast (im_itemnumb)")

        conn.commit()
    except Exception as e:
        Handle_Exception(e)

    return;


'''
   Manage()

   This function performs simple record functions of add, delete and gets
'''


def manage():
    print("Manage\n")

    add_records()

    display_records()

    return;


'''
    add_records()

    This function adds records to a table in the database from an
    array of strings
'''


def add_records():
    print("\tAdd records...")

    try:
        data = [
            "('1000','92867','CA','1','Bryan Williams','2999 Regency','Orange')",
            "('1001','61434','CT','1','Michael Jordan','13 Main','Harford')",
            "('1002','73677','GA','1','Joshua Brown','4356 Cambridge','Atlanta')",
            "('1003','10034','MO','1','Keyon Dooling','19771 Park Avenue','Columbia')"
        ]
        ''' add one record at time to table '''
        for row in data:
            cur.execute("INSERT INTO custmast VALUES " + row)

        data = [
            "('09/01/2002', '09/05/2002', '1', '1001')",
            "('09/02/2002', '09/06/2002', '2', '1002')"
        ]
        ''' add one record at time to table '''
        for row in data:
            cur.execute("INSERT INTO custordr VALUES " + row)

        data = [
            "(1, 2, '1', '1')",
            "(2, 1, '1', '2')",
            "(3, 1, '1', '3')",
            "(1, 3, '2', '3')"
        ]
        ''' add one record at time to table '''
        for row in data:
            cur.execute("INSERT INTO ordritem VALUES " + row)

        data = [
            "(10, 19.95,  '1', 'Hammer')",
            "(3,   9.99,  '2', 'Wrench')",
            "(4,  16.59,  '3', 'Saw')",
            "(1,   3.98,  '4', 'Pliers')"
        ]
        ''' add one record at time to table '''
        for row in data:
            cur.execute("INSERT INTO itemmast VALUES " + row)

    except Exception as e:
        Handle_Exception(e);

    conn.commit()
    return;


'''
   display()

   This function displays the contents of a table.
'''


def display_records():
    print("\tDisplay records...");
    try:
        ''' execute a query statement '''
        cur.execute("SELECT cm_custname 'Name', SUM(im_itempric * oi_quantity) 'Total' " +
                    "FROM custmast, custordr, ordritem, itemmast " +
                    "WHERE co_custnumb = cm_custnumb AND co_ordrnumb = oi_ordrnumb AND oi_itemnumb = im_itemnumb " +
                    "GROUP BY co_ordrnumb, cm_custname"
                    );
        rows = cur.fetchall()

        ''' fetch and display each individual record '''
        print("\n\tName\t\tTotal")
        for row in rows:
            print("\t{0}\t{1}".format(row[0], row[1]))

    except Exception as e:
        Handle_Exception(e)

    conn.commit()
    return;


'''
   Done()

   This function handles the housekeeping of closing, freeing,
   disconnecting and logging out of the database
'''


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

