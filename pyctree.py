from pyctsqlapi import *
import time
import sys

if sys.version_info < (3,0,0):
    from exceptions import StopIteration
	
#import warnings

#warnings.warn('DB-API extension cursor.connection used')

__all__ = [
    'connect', 'Connection', 'Cursor'
    ]

apilevel    = '2.0'
threadsafety    = 1 # 1 Threads may share the module, but not connections.
paramstyle    = 'qmark'


class Cursor(object):
    """Cursor objects represent a database cursor, which is used to manage the context
of a fetch operation.  Cursors created from the same connection are not
isolated, i.e., any changes done to the database by a cursor are immediately
visible by the other cursors.  Cursors created from different connections are
isolated."""
    def __init__(self, _connection):
        self._cmd = None
        self._lastOperation = ''
        self._arraysize = 1
        self._affected = -1
        self._conn = _connection
        if _connection != None:
            self._cmd = CtreeSql.new_command(_connection._conn)
        else:
            raise InterfaceError(4,'internal error, invalid Connection instance in cursor constructor')
        CtreeSql.set_scrollable_cursor(self._cmd, 1)
        #CtreeSql.set_low_fetch_size(self._cmd,32)

    def __del__(self):
        if self._cmd != None :
            try:
                self._cmd.close()
            except:
                pass
        self._cmd = None

    def __str__(self):
        raise NotSupportedError('__str__ not yet supported for cursor')

    def __iter__(self):
        return self

    def next(self): # Python 3: def __next__(self)
        return self.__next__()

    def __next__(self):
        res = self.fetchone()
        if res is not None:
            return tuple(res)
        else:
            raise StopIteration

    def _check_validity(self, check_crsr = False):
        if self._cmd == None:
            raise ProgrammingError(5,'invalid Cursor instance')
        self._conn._check_validity();
        if check_crsr and not self._cmd.is_rs_open():
            raise ProgrammingError(6,'Closed Cursor instance')
        return True

    def _get_row_count(self):
        self._check_validity()
        if self._affected != -1 :
            return self._affected
        if self._lastOperation == '':
            return -1
        return CtreeSql.get_row_count(self._cmd)

    def _get_description(self):
        try :
            self._check_validity(True)
        except ProgrammingError :
            return None

        return self._cmd.get_description()

    def _get_arraysize(self):
        return self._arraysize
    
    def _set_arraysize(self, value):
        self._arraysize = value
        
    def _get_connection_obj(self):
        return self._conn
    
    def _get_query_timeout(self):
        self._check_validity()
        return CtreeSql.get_query_timeout(self._cmd)
        
    def _set_query_timeout(self, value):
        self._check_validity()
        return CtreeSql.set_query_timeout(self._cmd, value)
    
    description = property(_get_description,doc="""This read-only attribute is a sequence of 7-item sequences.  Each of these
sequences contains information describing one result column: (name, type_code,
display_size, internal_size, precision, scale, null_ok).
    
This attribute will be None for operations that do not return rows or if the
cursor has not had an operation invoked via the execute() method yet
    
The type_code can be interpreted by comparing it to the Type Objects defined in
the DB API and defined the pyctree module: Date, Time, Timestamp, Binary,
STRING, BINARY, NUMBER, and DATETIME.""")
    
    rowcount = property(_get_row_count,doc="""This read-only attribute specifies the number of rows the last statement
affected. """)
    
    #nextset #optional not supported
    
    arraysize = property(_get_arraysize,_set_arraysize,None,"""This read/write attribute specifies the number of rows to fetch at a time with
fetchmany(). It defaults to 1 meaning to fetch a single row at a time.""")
    
    connection = property(_get_connection_obj,doc="""This read-only attribute return a reference to the Connection
object on which the cursor was created.""")

    querytimeout = property(_get_query_timeout,_set_query_timeout,None,"""This read/write attribute specifies the query time-out in seconds. It defaults to 0 meaning no time-out.""")

    def close(self):
        """Close the cursor now (rather than whenever __del__ is called).  The cursor will 
be unusable from this point forward; a ProgrammingError exception will be 
raised if any operation is attempted with the cursor."""
        self._check_validity()
        self._cmd.close()
        self._cmd = None
        self._affected = -1
   
    def execute(self, operation, parameters=None):
        """Prepare and execute a database query or command.
Parameters can be provided as a sequence (as specified by the DB API):
cursor.execute(sql, (param1, param2))"""
        self._affected = -1
        self._check_validity()
        if self._cmd.is_rs_open() :
            self._cmd.close_rs()
            self._desc = None
            self._lastOperation = '' # this because we need to always prepare after a select
        
        if operation != self._lastOperation:
            CtreeSql.prepare(self._cmd, operation)
            self._lastOperation = operation

        CtreeSql.set_params(self._cmd, parameters)

        CtreeSql.execute(self._cmd)
   
    def callproc (self, procname, params=None):
        """Prepare and execute a database stored procedure.
Parameters can be provided as a sequence (as specified by the DB API):
cursor.callproc(procname, (param1, param2))"""
        if params != None :
            pl = len (params) - 1
            vals='?'
            while pl > 0 :
                vals = vals + ', ?'
                pl = pl - 1
        else:
            vals =''
        cmd = 'call '+procname+' ('+vals+')'
        self.execute(cmd,params)
        
    def executemany(self, operation, seq_of_parameters):
        """Prepare a database query or command and then execute it against all parameter
sequences found in the sequence seq_of_params."""           
        self._affected = -1
        self._check_validity()
        if self._cmd.is_rs_open() :
            self._cmd.close_rs()
            self._desc = None
            self._lastOperation = '' # this because we need to always prepare after a select
        
        if operation != self._lastOperation:
            CtreeSql.prepare_batch(self._cmd, operation, len(seq_of_parameters))
            self._lastOperation = operation

        for params in seq_of_parameters:
            CtreeSql.set_params(self._cmd, params)
            CtreeSql.next_batch_item(self._cmd)
            
        CtreeSql.execute(self._cmd)      
                    
    def setinputsizes(self, size):
        pass

    def setoutputsize(self, size, column = None):
        pass

    def fetchmany(self, size = None):
        """Fetch the next set of rows of a query result, returning a list of Row
instances. An empty list is returned when no more rows are available.

The number of rows to fetch per call is specified by the parameter.  If it is
not given, the cursor's arraysize determines the number of rows to be
fetched. The method tries to fetch as many rows as indicated by the size
parameter. If this is not possible due to the specified number of rows not
being available, fewer rows may be returned.

A ProgrammingError exception is raised if the previous call to execute() did
not produce any result set or no call was issued yet."""
        result = []
        self._check_validity(True)
        if size == None:
            size = self._arraysize
        while size > 0:
            size = size - 1
            tpl = CtreeSql.get_next_tuple(self._cmd)
            if tpl == None:
                break
            result.append(tpl)
        if self._affected == -1:
            self._affected = len(result)
        else:
            self._affected += len(result)
        return result
    
    def fetchall(self):
        """Fetch all remaining rows of a query result, returning them as a list of Rows.
An empty list is returned if there are no more rows.

A ProgrammingError exception is raised if the previous call to execute() did
not produce any result set or no call was issued yet."""
        result = []
        self._check_validity(True)
        while True:
            tpl = CtreeSql.get_next_tuple(self._cmd)
            if tpl == None:
                break
            result.append(tpl)
        if self._affected == -1:
            self._affected = len(result)
        else:
            self._affected += len(result)
        return result

    def fetchone(self):
        """Fetch the next row of a query result set, returning a single Row instance, or
None when no more data is available

A ProgrammingError exception is raised if the previous call to execute() did
not produce any result set or no call was issued yet."""
        self._check_validity(True)
        tpl = CtreeSql.get_next_tuple(self._cmd)
        if tpl is not None:
            if self._affected == -1:
                self._affected = 1
            else:
                self._affected += 1
        return tpl

    @property
    def lastrowid(self):
        """retrieve the last rowid used."""
        _int_cur = self._conn.cursor()
        _int_cur.execute("select last_ident()")
        last = _int_cur.fetchone()
        _int_cur.close()
        return last[0]

class Connection(object):
    """Connection objects handle connections to the database."""
    
    #define here class variables shared by all instances

    def __init__(self, user='guest', password='', host='127.0.0.1', database='ctreeSQL', port ='6597', ssl = None):
        #define here instance variables
        self._conn = None
        if (not isinstance(port, STRING)):
             port = str(port)

        self._conn = CtreeSql.new_connection(port + '@' + host + ':' + database, user, password, ssl )

    def __del__(self):
        if self._conn != None:
            CtreeSql.free_connection(self._conn)
        self._conn = None

    def __str__(self):
        return str(self._conn)

    def _check_validity(self):
        if self._conn == None:
            raise ProgrammingError(2,'invalid/closed Connect instance')
    
    def _set_autocommit(self, value):
        self._check_validity()
        CtreeSql.setautocommit(self._conn, value)
    
    def _get_autocommit(self):
        self._check_validity()
        return CtreeSql.getautocommit(self._conn)
        
    autocommit = property(_get_autocommit, _set_autocommit, doc="""Read/write attribute: if True, transactions are handled by the driver and every statement is immediately committed; if False transactions need to be explicitly handled.""")
    
    def close(self):
        """  Close the connection now (rather than whenever __del__ is called).
The connection will be unusable from this point forward and a ProgrammingError
will be raised if any operation is attempted with the connection.  The same
applies to all cursor objects trying to use the connection.
    """
        self._check_validity()
        CtreeSql.free_connection(self._conn)
        self._conn = None
        
    def cursor(self):
        """Return a new Cursor object using the connection."""
        self._check_validity()
        return Cursor(self)

    def commit(self):
        """Commit any pending transaction to the database."""
        self._check_validity()
        CtreeSql.commit(self._conn)
        
    def rollback(self):
        """Causes the the database to roll back any pending transaction."""
        self._check_validity()
        CtreeSql.abort(self._conn)

    def set_isolation(self, value):
        self._check_validity()
        CtreeSql.set_isolation_level(self._conn, value)
    
    def get_isolation(self):
        self._check_validity()
        return CtreeSql.get_isolation_level(self._conn)
    
def connect(**kw_args):
    """Constructor for creating a connection to the database.
Returns a Connection Object. It takes parameters 
as keyword parameters for more intuitive use as
follow:
user     User name as string (optional default guest)
password Password as string (optional default None)
host     Hostname (optional default 127.0.0.1)
database Database name (optional default ctreeSQL)
port     TCP/IP port number (optional default 6597)
ssl      None: no SSL, (optional default None)
         'BASIC': SSL without certificate checking, 
         '<certificate file name>': SSL with certificate checking, certificate file as specified,
         '': SSL with certificate checking, certificate in current working dir named ctsrvr.pem.
"""
    return Connection(**kw_args)

################################################################################
    
def DateFromTicks(ticks=None):
    if ticks == None: 
        ticks = time.time()
    return Date(*time.localtime(ticks)[:3])

def TimeFromTicks(ticks=None):
    if ticks == None: 
        ticks = time.time()
    return Time(*time.localtime(ticks)[3:6])

def TimestampFromTicks(ticks=None):
    if ticks == None: 
        ticks = time.time()
    return Timestamp(*time.localtime(ticks)[:6])
################################################################################