import ctypes 
import sys
import binascii
import datetime
import platform

__all__ = [
    'CtreeSql', 'Error', 'InterfaceError', 'Warning',
    'DatabaseError', 'InternalError', 'OperationalError', 
    'ProgrammingError', 'IntegrityError', 'DataError', 'NotSupportedError',
    'Date', 'Time', 'Timestamp', 'Binary', 'ROWID', 'STRING', 'NUMBER', 
    'BINARY', 'DATETIME'
    ]

if sys.version_info > (3,0,0):
    long = int
    StandardError = Exception

    def to_Cstring(s):
        """
        Convert Python str to ctsqlapi expected string format
        """
        if s is None:
            return None
        if _isunicode: 
            if type(s) is bytes: 
                return str(s);
            return s
        if type(s) is bytes: 
            return s
        return str(s).encode()

    def from_Cstring(s):
        """
        Convert ctsqlapi string format to Python str
        """
        if s is None: return None
        if _isunicode: return s
        return _conv_from_MBSstring(s)

    def _conv_from_MBSstring(s):
        """
        Convert C MBS string to Python str
        """
        if s is None: return None
        decodedString = ''
        try:
            decodedString = s.decode()
        except:
            return decodedString
        return decodedString

    def _conv_from_Bytes(s):
        """
        Convert C MBS string to Python str
        """
        if s is None: return None
        return s

    def _conv_to_MBSstring(s):
        """
        Convert Python str to C MBS string
        """
        if s is None: return None
        return str(s).encode()
    
    def _conv_to_Wstring(s):
        """
        Convert Python str to C Wstring
        """
        return s
    
    def _conv_from_Wstring(s):
        """
        Convert  C Wstring to Python str
        """
        return s

else:
    import exceptions
    import unicodedata
    StandardError = exceptions.StandardError

    def to_Cstring(s):
        """
        Convert Python str to ctsqlapi expected string format
        """
        if s is None: 
            return None
        if _isunicode: 
            return ctypes.create_unicode_buffer(s)
        return s

    def from_Cstring(s):
        """
        Convert ctsqlapi string format to Python str
        """
        if s is None: return None
        if _isunicode: return unicodedata.normalize('NFKD', s).encode('ascii','ignore')
        return s

    def _conv_from_MBSstring(s):
        return s

    def _conv_to_MBSstring(s):
        if type(s) is unicode: 
            return unicodedata.normalize('NFKD', s).encode('ascii','ignore')
        return s

    def _conv_to_Wstring(s):
        return ctypes.create_unicode_buffer(s)

    def _conv_from_Wstring(s):
        return unicodedata.normalize('NFKD', s).encode('ascii','ignore')

if sys.version_info > (3,3,0):
    from decimal import Decimal
else:
    try:
        from cdecimal import Decimal
    except ImportError:
        from decimal import Decimal

connectionHandle = ctypes.c_void_p
commandHandle = ctypes.c_void_p
cursorHandle = ctypes.c_void_p
ctsqlret = ctypes.c_int32
ctsqltype = ctypes.c_int16
_integer = ctypes.c_int32
_uinteger = ctypes.c_uint32
_smallint = ctypes.c_int16

class Error(StandardError):
    pass

class Warning(StandardError):
    pass

class InterfaceError(Error):
    pass

class DatabaseError(Error):
    pass

class InternalError(DatabaseError):
    pass

class OperationalError(DatabaseError):
    pass

class ProgrammingError(DatabaseError):
    pass

class IntegrityError(DatabaseError):
    pass

class DataError(DatabaseError):
    pass

class NotSupportedError(DatabaseError):
    pass

class _bigint(ctypes.Structure):
    _fields_ = [('ll',_uinteger),('hl',_integer)]
    def __init__ (self):
        self.hl = 0
        self.ll = 0
        
    def get_long (self):
        return ((self.hl << 32) + self.ll)
    
    def set_long (self, val):
        self.hl = val >> 32
        self.ll = val & ((2**32)-1) 
        assert ((self.hl << 32) + self.ll) == val


class _sqldate(ctypes.Structure): 
    _fields_ = [('year', ctypes.c_short),
                ('month', ctypes.c_ubyte),
                ('day', ctypes.c_ubyte)]
    def get_date (self):
        return Date(self.year,self.month,self.day)
    
    def set_date (self, val):
        self.year = val.year
        self.month = val.month
        self.day = val.day

class _sqltime(ctypes.Structure): 
    _fields_ = [('hours', ctypes.c_ubyte),
                ('mins', ctypes.c_ubyte),
                ('secs', ctypes.c_ubyte),
                ('msecs', ctypes.c_ushort)]
    def get_time (self):
        return Time(self.hours,self.mins,self.secs,self.msecs*1000)
    
    def set_time (self, val):
        self.hours = val.hour
        self.mins = val.minute
        self.secs = val.second
        self.msecs = int(val.microsecond / 1000)

class _sqltimestamp(ctypes.Structure): 
    _fields_ = [('ts_date', _sqldate),
                ('ts_time', _sqltime)]
    
    def get_timestamp (self):
        return Timestamp(self.ts_date.year, self.ts_date.month, self.ts_date.day, \
                        self.ts_time.hours, self.ts_time.mins,self.ts_time.secs, \
                        self.ts_time.msecs*1000)
        
    def set_timestamp (self, val):
        self.ts_date.set_date(val.date())
        self.ts_time.set_time(val.time())

shortpl = platform.system()
if shortpl == 'Windows':
    _ctsql = ctypes.CDLL("./ctsqlapi")
elif shortpl == 'Darwin':
    _ctsql = ctypes.CDLL("libctsqlapi.dylib")
else:
    _ctsql = ctypes.CDLL("libctsqlapi.so")

_ctsql.ctsqlIsUnicodeLib.restype = ctypes.c_byte
_ctsql.ctsqlIsUnicodeLib.argtypes = []

if _ctsql.ctsqlIsUnicodeLib() == 1:
    _string_t = ctypes.c_wchar_p
    _isunicode = True
else:
    _string_t = ctypes.c_char_p
    _isunicode = False

_ctsql.ctsqlNewConnection.restype = connectionHandle
_ctsql.ctsqlNewConnection.argtypes = []

_ctsql.ctsqlFreeConnection.restype = None
_ctsql.ctsqlFreeConnection.argtypes = [connectionHandle]

_ctsql.ctsqlConnect.restype= ctsqlret
_ctsql.ctsqlConnect.argtypes =[connectionHandle, _string_t, _string_t, _string_t]

_ctsql.ctsqlDisconnect.restype= ctsqlret
_ctsql.ctsqlDisconnect.argtypes =[connectionHandle]

_ctsql.ctsqlIsActiveConn.restype= ctypes.c_byte
_ctsql.ctsqlIsActiveConn.argtypes =[connectionHandle]

_ctsql.ctsqlCommit.restype= ctsqlret
_ctsql.ctsqlCommit.argtypes = [connectionHandle]

_ctsql.ctsqlAbort.restype= ctsqlret
_ctsql.ctsqlAbort.argtypes = [connectionHandle]

_ctsql.ctsqlGetAutoCommit.restype = ctypes.c_byte
_ctsql.ctsqlGetAutoCommit.argtypes = [connectionHandle]

_ctsql.ctsqlSetAutoCommit.restype = _integer
_ctsql.ctsqlSetAutoCommit.argtypes = [connectionHandle, ctypes.c_byte]

_ctsql.ctsqlGetErrorMessage.restype= _string_t
_ctsql.ctsqlGetErrorMessage.argtypes = [connectionHandle]

#cursor
_ctsql.ctsqlNewCommand.restype = commandHandle
_ctsql.ctsqlNewCommand.argtypes = [connectionHandle]

_ctsql.ctsqlFreeCommand.restype = None
_ctsql.ctsqlFreeCommand.argtypes = [commandHandle]

_ctsql.ctsqlPrepare.restype = ctsqlret
_ctsql.ctsqlPrepare.argtypes = [commandHandle, _string_t]

_ctsql.ctsqlSetTupleCount.restype = ctsqlret
_ctsql.ctsqlSetTupleCount.argtypes = [commandHandle, _integer]

_ctsql.ctsqlExecute.restype = ctsqlret
_ctsql.ctsqlExecute.argtypes = [commandHandle, ctypes.POINTER(cursorHandle)]

_ctsql.ctsqlAffectedRows.restype = _integer
_ctsql.ctsqlAffectedRows.argtypes = [commandHandle]

_ctsql.ctsqlSetParameter.restype = ctsqlret
_ctsql.ctsqlSetParameter.argtypes = [commandHandle, _integer, ctsqltype, _integer, ctypes.c_byte, ctypes.c_void_p]

_ctsql.ctsqlSetCharParameter.restype = ctsqlret
_ctsql.ctsqlSetCharParameter.argtypes = [commandHandle, _integer, ctsqltype, ctypes.c_byte, ctypes.c_char_p, _integer ]

_ctsql.ctsqlSetNCharParameter.restype = ctsqlret
_ctsql.ctsqlSetNCharParameter.argtypes = [commandHandle, _integer, ctsqltype, ctypes.c_byte, ctypes.c_wchar_p, _integer ]

_ctsql.ctsqlSetBigIntParameter.restype = ctsqlret
_ctsql.ctsqlSetBigIntParameter.argtypes = [commandHandle, _integer, ctypes.c_byte, ctypes.POINTER(_bigint)]

_ctsql.ctsqlSetIntegerParameter.restype = ctsqlret
_ctsql.ctsqlSetIntegerParameter.argtypes = [commandHandle, _integer, ctsqltype, ctypes.c_byte, _integer]

_ctsql.ctsqlSetFloatParameter.restype = ctsqlret
_ctsql.ctsqlSetFloatParameter.argtypes = [commandHandle, _integer, ctsqltype, ctypes.c_byte, ctypes.c_double]

_ctsql.ctsqlSetNumericParameterAsString.restype = ctsqlret
_ctsql.ctsqlSetNumericParameterAsString.argtypes = [commandHandle, _integer, ctsqltype, ctypes.c_byte, _string_t]

_ctsql.ctsqlSetTimeStampParameter.restype = ctsqlret
_ctsql.ctsqlSetTimeStampParameter.argtypes = [commandHandle, _integer, ctypes.c_byte, ctypes.POINTER(_sqltimestamp)]

_ctsql.ctsqlSetDateParameter.restype = ctsqlret
_ctsql.ctsqlSetDateParameter.argtypes = [commandHandle, _integer, ctypes.c_byte, ctypes.POINTER(_sqldate)]

_ctsql.ctsqlSetTimeParameter.restype = ctsqlret
_ctsql.ctsqlSetTimeParameter.argtypes = [commandHandle, _integer, ctypes.c_byte, ctypes.POINTER(_sqltime)]

_ctsql.ctsqlSetBinaryParameter.restype = ctsqlret
_ctsql.ctsqlSetBinaryParameter.argtypes = [commandHandle, _integer, ctypes.c_byte, ctypes.c_void_p, _integer]


_ctsql.ctsqlGetParameterCount.restype = ctsqlret
_ctsql.ctsqlGetParameterCount.argtypes = [commandHandle]

_ctsql.ctsqlGetParameterType.restype = ctsqltype
_ctsql.ctsqlGetParameterType.argtypes = [commandHandle, _integer]

_ctsql.ctsqlGetParameterLength.restype = _integer
_ctsql.ctsqlGetParameterLength.argtypes = [commandHandle, _integer]

_ctsql.ctsqlFreeCursor.restype = None
_ctsql.ctsqlFreeCursor.argtypes = [cursorHandle]

_ctsql.ctsqlGetColumnCount.restype = _integer
_ctsql.ctsqlGetColumnCount.argtypes = [cursorHandle]

_ctsql.ctsqlGetColumnTitle.restype = ctsqlret
_ctsql.ctsqlGetColumnTitle.argtypes = [cursorHandle, _integer, _string_t, _integer]

_ctsql.ctsqlGetTableName.restype = ctsqlret
_ctsql.ctsqlGetTableName.argtypes = [cursorHandle, _integer, _string_t, _integer]

_ctsql.ctsqlGetColumnType.restype = ctsqltype
_ctsql.ctsqlGetColumnType.argtypes = [cursorHandle, _integer]

_ctsql.ctsqlGetColumnLength.restype = _integer
_ctsql.ctsqlGetColumnLength.argtypes = [cursorHandle, _integer]

_ctsql.ctsqlGetColumnPrecisionX.restype = _integer
_ctsql.ctsqlGetColumnPrecisionX.argtypes = [cursorHandle, _integer]

_ctsql.ctsqlGetColumnScale.restype = _smallint
_ctsql.ctsqlGetColumnScale.argtypes = [cursorHandle, _integer]

_ctsql.ctsqlIsNullable.restype = _integer
_ctsql.ctsqlIsNullable.argtypes = [cursorHandle, _integer]

_ctsql.ctsqlNext.restype = ctsqlret
_ctsql.ctsqlNext.argtypes = [cursorHandle]

_ctsql.ctsqlIsColumnNull.restype = ctypes.c_ubyte
_ctsql.ctsqlIsColumnNull.argtypes = [cursorHandle, _integer]

_ctsql.ctsqlGetChar.restype = ctsqlret
_ctsql.ctsqlGetChar.argtypes = [cursorHandle, _integer, ctypes.c_char_p]

_ctsql.ctsqlGetNChar.restype = ctsqlret
_ctsql.ctsqlGetNChar.argtypes = [cursorHandle, _integer, ctypes.c_wchar_p]

_ctsql.ctsqlGetTinyInt.restype = ctsqlret
_ctsql.ctsqlGetTinyInt.argtypes = [cursorHandle, _integer,  ctypes.POINTER(ctypes.c_byte)]

_ctsql.ctsqlGetSmallInt.restype = ctsqlret
_ctsql.ctsqlGetSmallInt.argtypes = [cursorHandle, _integer,  ctypes.POINTER(ctypes.c_short)]

_ctsql.ctsqlGetInteger.restype = ctsqlret
_ctsql.ctsqlGetInteger.argtypes = [cursorHandle, _integer,  ctypes.POINTER(_integer)]

_ctsql.ctsqlGetBigInt.restype = ctsqlret
_ctsql.ctsqlGetBigInt.argtypes = [cursorHandle, _integer,  ctypes.POINTER(_bigint)]

_ctsql.ctsqlGetNumericAsString.restype = ctsqlret
_ctsql.ctsqlGetNumericAsString.argtypes = [cursorHandle, _integer, _string_t, _integer]

_ctsql.ctsqlGetReal.restype = ctsqlret
_ctsql.ctsqlGetReal.argtypes = [cursorHandle, _integer,  ctypes.POINTER(ctypes.c_float)]

_ctsql.ctsqlGetFloat.restype = ctsqlret
_ctsql.ctsqlGetFloat.argtypes = [cursorHandle, _integer,  ctypes.POINTER(ctypes.c_double)]

_ctsql.ctsqlGetDate.restype = ctsqlret
_ctsql.ctsqlGetDate.argtypes = [cursorHandle, _integer,  ctypes.POINTER(_sqldate)]

_ctsql.ctsqlGetTime.restype = ctsqlret
_ctsql.ctsqlGetTime.argtypes = [cursorHandle, _integer,  ctypes.POINTER(_sqltime)]

_ctsql.ctsqlGetTimeStamp.restype = ctsqlret
_ctsql.ctsqlGetTimeStamp.argtypes = [cursorHandle, _integer,  ctypes.POINTER(_sqltimestamp)]

_ctsql.ctsqlGetBytes.restype = ctsqlret
_ctsql.ctsqlGetBytes.argtypes = [cursorHandle, _integer,  ctypes.c_char_p, _integer]

_ctsql.ctsqlSetTimeout.restype = ctsqlret
_ctsql.ctsqlSetTimeout.argtypes = [commandHandle, _integer]

_ctsql.ctsqlGetTimeout.restype = _integer
_ctsql.ctsqlGetTimeout.argtypes = [commandHandle]

_ctsql.ctsqlPrepareBatch.restype = ctsqlret
_ctsql.ctsqlPrepareBatch.argtypes = [commandHandle, _string_t, ctypes.c_int32]

_ctsql.ctsqlNextBatchItem.restype = ctypes.c_int32
_ctsql.ctsqlNextBatchItem.argtypes = [commandHandle]

_ctsql.ctsqlSetScrollableCursor.restype = ctsqlret
_ctsql.ctsqlSetScrollableCursor.argtypes = [commandHandle, ctypes.c_byte]

_ctsql.ctsqlSetSSL.restype = ctsqlret
_ctsql.ctsqlSetSSL.argtypes = [commandHandle, _string_t]

_ctsql.ctsqlSetIsolationLevel.restype = ctypes.c_int32
_ctsql.ctsqlSetIsolationLevel.argtypes =  [commandHandle, ctypes.c_int32]

_ctsql.ctsqlGetIsolationLevel.restype = ctypes.c_int32
_ctsql.ctsqlGetIsolationLevel.argtypes = [commandHandle]


class BaseType_:
    def __init__(self):
        self.value = None
        
    def __cmp__(self, other):
        if other :
            return cmp(self.value, other.value)
        else :
            return 1
    def __eq__(self, other):
        if other :
            return self.value == other.value
        else :
            return 0
    def __ne__(self, other):
        if other :
            return self.value != other.value
        else :
            return 1
    def __lt__(self, other):
        if other :
            return self.value < other.value
        else :
            return 0
    def __le__(self, other):
        if other :
            return self.value <= other.value
        else :
            return 1
    def __gt__(self, other):
        if other :
            return self.value > other.value
        else :
            return 1
    def __ge__(self, other):
        if other :
            return self.value >= other.value
        else :
            return 1

class Binary(BaseType_):
    def __init__(self, s):
        self.value = s

    def __repr__(self):
        return '<Binary len: %d>' % len(self.value)

    def __str__(self):
        return str(self.value)
    
    def __len__(self):
        return len(self.value)

    def get_HEX_value(self): 
        """returns the Hexadecimal representation of Binary data."""
        return binascii.b2a_hex(self.value)
    
    def set_HEX_value (self, hexstr):
        """set the Binary data from its hexadecimal representation."""
        self.value = binascii.a2b_hex(hexstr)
    
    def getbytes(self):
        if type(self.value) == bytes:
            return self.value
        else:
            return bytes(str(self.value))

Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime

DATETIME = Timestamp
BINARY = Binary
ROWID = str
STRING = str
NUMBER = Decimal

################################################################################
class CommandHelper :
    def __init__(self, _conn, _cmd):
        self._cmd = _cmd
        self._conn = _conn
        self._crsr = None
        self._desc = None
        self._sqldesc = None
        self.fldbuffer = ctypes.create_string_buffer(8200) #should be large enough

    def __del__(self):
        if self._cmd != None :
            _ctsql.ctsqlFreeCommand(self._cmd)
        if self._crsr != None :
            _ctsql.ctsqlFreeCursor(self._crsr)

    def close (self):
        _ctsql.ctsqlFreeCommand(self._cmd)
        self._cmd = None
        if self._crsr != None :
            _ctsql.ctsqlFreeCursor(self._crsr)
        self._crsr = None

    def get_command_handle(self):
        return self._cmd

    def get_connection_handle(self):
        return self._conn

    def get_cursor_handle(self):
        return self._crsr

    def set_cursor_handle(self, _crsr):
        if self._crsr != None :
            raise Error (-20000,'cursor already open')
        self._crsr = _crsr
    
    def is_rs_open(self):
        return self._crsr != None

    def close_rs(self):
        if self._crsr != None:
            _ctsql.ctsqlFreeCursor(self._crsr)
        self._crsr = None
        self._desc = None
        self._sqldesc = None

    def get_description(self):
        if self._crsr == None:
            return None #????

        if self._desc == None:
            self._desc = []
            cols = CtreeSql.get_column_count(self)
            for n in range ( 0, cols):
                coldesc = CtreeSql.get_column_description(self, n, False)
                self._desc.append(coldesc)
        return self._desc
    
    def _get_sqldescription(self):
        if self._crsr == None:
            return None #????

        if self._sqldesc == None:
            self._sqldesc = []
            cols = CtreeSql.get_column_count(self)
            for n in range ( 0, cols):
                coldesc = CtreeSql.get_column_description(self, n, True)
                # print(coldesc)
                self._sqldesc.append(coldesc)
        return self._sqldesc

class CtreeSql :
    CTSQL_CHAR = 1
    CTSQL_NUMERIC = 2
    CTSQL_SMALLINT = 3
    CTSQL_INTEGER = 4
    CTSQL_REAL = 5
    CTSQL_FLOAT = 6
    CTSQL_DATE = 7
    CTSQL_MONEY = 8
    CTSQL_TIME = 9
    CTSQL_TIMESTAMP = 10
    CTSQL_TINYINT = 11
    CTSQL_BINARY = 12
    CTSQL_BIT = 13
    CTSQL_LVC = 14
    CTSQL_LVB = 15
    CTSQL_BIGINT = 16
    CTSQL_NCHAR = 17
    CTSQL_NVARCHAR = 18
    CTSQL_NCHAR_CS = 19
    CTSQL_NVARCHAR_CS = 20
    CTSQL_VARCHAR = 21
    CTSQL_BLOB = 22
    CTSQL_CLOB = 23
    CTSQL_NLVC = 24
    CTSQL_NCLOB = 25
    CTSQL_VARBINARY = 26

    PythonTypeFromSqlType = {CTSQL_CHAR : STRING,
                             CTSQL_NUMERIC : NUMBER,
                             CTSQL_SMALLINT : int,
                             CTSQL_INTEGER : int,
                             CTSQL_REAL : float,
                             CTSQL_FLOAT : float,
                             CTSQL_DATE : Date,
                             CTSQL_MONEY : NUMBER,
                             CTSQL_TIME : Time,
                             CTSQL_TIMESTAMP : Timestamp,
                             CTSQL_TINYINT : int,
                             CTSQL_BINARY : Binary,
                             CTSQL_BIT : int,
#                             CTSQL_LVC : STRING,
#                             CTSQL_LVB : Binary,
                             CTSQL_BIGINT : long,
                             CTSQL_NCHAR : STRING,
                             CTSQL_NVARCHAR : STRING,
#                             CTSQL_NCHAR_CS : STRING
#                             CTSQL_NVARCHAR_CS : STRING
                             CTSQL_VARCHAR : STRING,
#                             CTSQL_BLOB : 22
#                             CTSQL_CLOB : 23
#                             CTSQL_NLVC : 24
#                             CTSQL_NCLOB : 25
                             CTSQL_VARBINARY : Binary
}

    
    @staticmethod
    def get_error_message(conn):
        # make a of the string
        errmsg = _ctsql.ctsqlGetErrorMessage(conn)[:] 
        return from_Cstring(errmsg)

    # connection class low-level methods
    @staticmethod
    def new_connection(connstr, user, password, ssl = None):
        conn = _ctsql.ctsqlNewConnection()
        if conn == None:
            raise InterfaceError(1,'Cannot allocate connection')
        retcode = _ctsql.ctsqlSetSSL(conn, to_Cstring(ssl));
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(conn)
            _ctsql.ctsqlFreeConnection(conn)
            raise DatabaseError(retcode, errmsg)
        retcode = _ctsql.ctsqlConnect(conn, to_Cstring(connstr), to_Cstring(user), to_Cstring(password))
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(conn)
            _ctsql.ctsqlFreeConnection(conn)
            raise DatabaseError(retcode, errmsg)
        return conn

    @staticmethod
    def free_connection(conn):
        return _ctsql.ctsqlFreeConnection(conn)

    @staticmethod
    def commit(conn):
        retcode = _ctsql.ctsqlCommit(conn)
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(conn)
            raise DatabaseError(retcode, errmsg)

    @staticmethod
    def abort(conn):  
        retcode = _ctsql.ctsqlAbort(conn)
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(conn)
            raise DatabaseError(retcode, errmsg)
    
    @staticmethod
    def setautocommit(conn, value):  
        retcode = _ctsql.ctsqlSetAutoCommit(conn, value)
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(conn)
            raise DatabaseError(retcode, errmsg)
        
    @staticmethod
    def getautocommit(conn):  
        return (_ctsql.ctsqlGetAutoCommit(conn) == 1)
    
    @staticmethod
    def set_isolation_level(conn, level):
        return _ctsql.ctsqlSetIsolationLevel(conn, level)

    @staticmethod
    def get_isolation_level(conn):
        return _ctsql.ctsqlGetIsolationLevel(conn)

    # cursor class low-level methods     
    @staticmethod
    def new_command(conn):
        cmd = _ctsql.ctsqlNewCommand(conn)
        if cmd == None:
            raise InterfaceError(1,'Cannot allocate cursor')
        return CommandHelper(conn, cmd)
    
    @staticmethod
    def prepare(cmd, stmt):
        retcode = _ctsql.ctsqlPrepare(cmd.get_command_handle(), to_Cstring(stmt))
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(cmd.get_connection_handle())
            raise DatabaseError(retcode, errmsg)    
        
    @staticmethod
    def set_params(cmd, parameters):
        n = 0;
        if (parameters != None):
            n = len (parameters)
        
        if n != _ctsql.ctsqlGetParameterCount(cmd.get_command_handle()) :
            raise DatabaseError(-20014, 'Missing input parameters')
        
        if n == 0:
            return;
        
        cmd_hdl = cmd.get_command_handle()
        n = 0
        for p in parameters:
            param_sql = _ctsql.ctsqlGetParameterType(cmd_hdl, n)
            if (p == None):
                param_len = _ctsql.ctsqlGetParameterLength(cmd_hdl, n)
                retcode = _ctsql.ctsqlSetParameter(cmd_hdl, n, param_sql, param_len, 1, None)
            else:
                retcode = -1
                if (isinstance(p,STRING)):
                    if param_sql == CtreeSql.CTSQL_NUMERIC or param_sql == CtreeSql.CTSQL_MONEY:
                        retcode = _ctsql.ctsqlSetNumericParameterAsString(cmd_hdl, n, param_sql, 0, to_Cstring(p))
                    elif param_sql == CtreeSql.CTSQL_NCHAR or param_sql == CtreeSql.CTSQL_NVARCHAR:
                        retcode = _ctsql.ctsqlSetNCharParameter(cmd_hdl, n, param_sql, 0,
                                                               _conv_to_Wstring(p), (len(p)+1)*ctypes.sizeof(ctypes.c_wchar)) # C string terminator 
                    else:
                        retcode = _ctsql.ctsqlSetCharParameter(cmd_hdl, n, param_sql, 0,
                                                               _conv_to_MBSstring(p), len(p)+1) # C string terminator 
                elif (isinstance(p,int)):
                    if param_sql == CtreeSql.CTSQL_BIGINT :
                        big = _bigint()
                        big.set_long(p)
                        retcode = _ctsql.ctsqlSetBigIntParameter(cmd_hdl, n, 0, ctypes.byref(big))
                    else:
                        retcode = _ctsql.ctsqlSetIntegerParameter(cmd_hdl, n, param_sql, 0,
                                                              p)
                elif (isinstance(p,long)):
                    if param_sql == CtreeSql.CTSQL_BIGINT :
                        big = _bigint()
                        big.set_long(p)
                        retcode = _ctsql.ctsqlSetBigIntParameter(cmd_hdl, n, 0, ctypes.byref(big))
                    else:
                        retcode = _ctsql.ctsqlSetIntegerParameter(cmd_hdl, n, param_sql, 0,
                                                              _integer(p))
                elif (isinstance(p,float)):
                    if param_sql == CtreeSql.CTSQL_NUMERIC or param_sql == CtreeSql.CTSQL_MONEY:
                        retcode = _ctsql.ctsqlSetNumericParameterAsString(cmd_hdl, n, param_sql, 0, to_Cstring(str(p)))  
                    else:
                        retcode = _ctsql.ctsqlSetFloatParameter(cmd_hdl, n, param_sql, 0, ctypes.c_double(p))
                elif (isinstance(p,NUMBER)):
                    retcode = _ctsql.ctsqlSetNumericParameterAsString(cmd_hdl, n, param_sql, 0, to_Cstring(str(p)))  
                elif (isinstance(p,Timestamp)): #we need to check Timestamp first since a "Timestamp" is also a "Date"
                    buf = _sqltimestamp()
                    buf.set_timestamp(p)
                    retcode = _ctsql.ctsqlSetTimeStampParameter(cmd_hdl, n, 0, ctypes.byref(buf))       
                elif (isinstance(p,Date)):
                    buf = _sqldate()
                    buf.set_date(p)
                    retcode = _ctsql.ctsqlSetDateParameter(cmd_hdl, n, 0, ctypes.byref(buf))
                elif (isinstance(p,Time)):
                    buf = _sqltime()
                    buf.set_time(p)
                    retcode = _ctsql.ctsqlSetTimeParameter(cmd_hdl, n, 0, ctypes.byref(buf))
                elif (isinstance(p,Binary)):
                    byt = p.getbytes()
                    le = len(p)
                    retcode = _ctsql.ctsqlSetBinaryParameter(cmd_hdl, n, 0, byt, le)
                elif (sys.version_info < (3,0,0)):
                    if (isinstance(p,unicode)):
                        if param_sql == CtreeSql.CTSQL_NCHAR or param_sql == CtreeSql.CTSQL_NVARCHAR:
                            retcode = _ctsql.ctsqlSetNCharParameter(cmd_hdl, n, param_sql, 0,
                                                               p, (len(p)+1)*ctypes.sizeof(ctypes.c_wchar)) # C string terminator 
                        else:
                            retcode = _ctsql.ctsqlSetCharParameter(cmd_hdl, n, param_sql, 0,
                                                               _conv_from_Wstring(p), len(p)+1) # C string terminator 

                else :
                    raise InterfaceError(33333, 'data type not yet supported')
            if retcode != 0:
                errmsg = CtreeSql.get_error_message(cmd.get_connection_handle())
                raise DatabaseError(retcode, errmsg)
            n = n + 1

    @staticmethod
    def execute(cmd):
        mycr = cursorHandle()
        retcode = _ctsql.ctsqlExecute(cmd.get_command_handle(), ctypes.byref(mycr))
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(cmd.get_connection_handle())
            raise DatabaseError(retcode, errmsg)
        cmd.set_cursor_handle(mycr.value)

    @staticmethod
    def get_row_count(cmd): 
        return _ctsql.ctsqlAffectedRows(cmd.get_command_handle())

    @staticmethod
    def get_column_count(cmd):
        return _ctsql.ctsqlGetColumnCount(cmd.get_cursor_handle())

    @staticmethod
    def get_column_description(cmd, column, sqlonly):
        _crhandle = cmd.get_cursor_handle()
        
        colsize = _ctsql.ctsqlGetColumnLength(_crhandle, column)
        retcode = _ctsql.ctsqlGetColumnType(_crhandle, column)
        if retcode == 0:
            retcode = None

        if sqlonly:

            #coldesc = (retcode, colsize)
            # mine
            if _isunicode:
                title = ctypes.create_unicode_buffer(128)
            else:
                title = ctypes.create_string_buffer(128)
            _ctsql.ctsqlGetColumnTitle(_crhandle, column, title, 128)
            name = from_Cstring(title.value)
            coldesc = (retcode, colsize, name)
            #end mine

        else:
            try:
                coltype = CtreeSql.PythonTypeFromSqlType[retcode]
            except exceptions.KeyError:
                coltype = None
            if _isunicode:
                title = ctypes.create_unicode_buffer(128)
            else:
                title = ctypes.create_string_buffer(128)
            retcode = _ctsql.ctsqlGetColumnTitle(_crhandle, column, title, 128)
            if retcode != 0:
                raise DatabaseError(retcode, 'error getting column title')
            name = from_Cstring(title.value)
            colprec = _ctsql.ctsqlGetColumnPrecisionX(_crhandle, column)
            colscale = _ctsql.ctsqlGetColumnScale(_crhandle, column)
            colnull = _ctsql.ctsqlIsNullable(_crhandle, column)
            if colnull >= 2:
                colnull = None
        
            coldesc = (name, coltype, None, colsize, 
                       colprec, colscale, colnull)
        return coldesc

    @staticmethod
    def get_next_tuple(cmd):
        desc = cmd._get_sqldescription()
        result = None
        _crhandle = cmd.get_cursor_handle()
        retcode = _ctsql.ctsqlNext(_crhandle)
        if retcode == 0 :
            cols = _ctsql.ctsqlGetColumnCount(_crhandle)
            for n in range ( 0, cols):
                if _ctsql.ctsqlIsColumnNull(_crhandle,n) == 1:
                    value = None
                else :
                    coltyp = desc[n][0]
                    colname=desc[n][2]
                    colsiz = desc[n][1]
                    if (coltyp==CtreeSql.CTSQL_CHAR or coltyp==CtreeSql.CTSQL_VARCHAR) and "data" not in colname:
                        _ctsql.ctsqlGetChar(_crhandle, n, cmd.fldbuffer)
                        value = _conv_from_MBSstring(cmd.fldbuffer.value)
                    elif (coltyp==CtreeSql.CTSQL_CHAR or coltyp==CtreeSql.CTSQL_VARCHAR)and "data" in colname:
                        _ctsql.ctsqlGetChar(_crhandle, n, cmd.fldbuffer)
                        value = _conv_from_Bytes(cmd.fldbuffer.value)
                    elif coltyp==CtreeSql.CTSQL_NCHAR or coltyp==CtreeSql.CTSQL_NVARCHAR:
                        buf = ctypes.create_unicode_buffer(8200)
                        _ctsql.ctsqlGetNChar(_crhandle, n, buf)
                        value = buf.value  #for python 2 is a unicode type
                    elif coltyp == CtreeSql.CTSQL_TINYINT or coltyp == CtreeSql.CTSQL_BIT:
                        buf = ctypes.c_byte()
                        _ctsql.ctsqlGetTinyInt(_crhandle, n, ctypes.byref(buf))
                        value = buf.value
                    elif coltyp == CtreeSql.CTSQL_SMALLINT:
                        buf = ctypes.c_short()
                        _ctsql.ctsqlGetSmallInt(_crhandle, n, ctypes.byref(buf))
                        value = buf.value
                    elif coltyp == CtreeSql.CTSQL_INTEGER:
                        buf = _integer()
                        _ctsql.ctsqlGetInteger(_crhandle, n, ctypes.byref(buf))
                        value = buf.value
                    elif coltyp == CtreeSql.CTSQL_BIGINT:
                        buf = _bigint()
                        _ctsql.ctsqlGetBigInt(_crhandle, n, ctypes.byref(buf))
                        value = buf.get_long()
                    elif (coltyp==CtreeSql.CTSQL_REAL):
                        buf = ctypes.c_float()
                        _ctsql.ctsqlGetReal(_crhandle, n, ctypes.byref(buf))
                        value = buf.value
                    elif (coltyp==CtreeSql.CTSQL_FLOAT):
                        buf = ctypes.c_double()
                        _ctsql.ctsqlGetFloat(_crhandle, n, ctypes.byref(buf))
                        value = buf.value
                    elif coltyp==CtreeSql.CTSQL_MONEY or coltyp==CtreeSql.CTSQL_NUMERIC:
                        if _isunicode:
                            buf = ctypes.create_unicode_buffer(50)
                            _ctsql.ctsqlGetNumericAsString(_crhandle, n, buf, 50*ctypes.sizeof(ctypes.c_wchar));
                            value = NUMBER(from_Cstring(buf.value));
                        else:
                            _ctsql.ctsqlGetNumericAsString(_crhandle, n, cmd.fldbuffer, 8200);
                            value = NUMBER(_conv_from_MBSstring(cmd.fldbuffer.value));
                    elif coltyp==CtreeSql.CTSQL_DATE:
                        buf = _sqldate()
                        _ctsql.ctsqlGetDate(_crhandle, n, ctypes.byref(buf))
                        value = buf.get_date()
                    elif coltyp==CtreeSql.CTSQL_TIME:
                        buf = _sqltime()
                        _ctsql.ctsqlGetTime(_crhandle, n, ctypes.byref(buf))
                        value = buf.get_time()
                    elif coltyp==CtreeSql.CTSQL_TIMESTAMP:
                        buf = _sqltimestamp()
                        _ctsql.ctsqlGetTimeStamp(_crhandle, n, ctypes.byref(buf))
                        value = buf.get_timestamp()
                    elif coltyp==CtreeSql.CTSQL_BINARY or coltyp==CtreeSql.CTSQL_VARBINARY :
                        blen = _ctsql.ctsqlGetBytes(_crhandle, n, cmd.fldbuffer, 8200)
                        value = Binary(cmd.fldbuffer[0:blen])
                    else:
                        raise InterfaceError(33333, 'data type not yet supported')
                if result == None:
                    result = []
                result.append(value)
        elif retcode != 100 : #CTSQL_NOTFOUND
            errmsg = CtreeSql.get_error_message(cmd.get_connection_handle())
            raise DatabaseError(retcode, errmsg) 
        return result

    @staticmethod
    def get_query_timeout(cmd): 
        return _ctsql.ctsqlGetTimeout(cmd.get_command_handle())
        
    @staticmethod
    def set_query_timeout(cmd, value): 
        return _ctsql.ctsqlSetTimeout(cmd.get_command_handle(), value)
        
    @staticmethod
    def prepare_batch(cmd, stmt, par): 
        retcode = _ctsql.ctsqlPrepareBatch(cmd.get_command_handle(), to_Cstring(stmt), par)
        if retcode != 0:
            errmsg = CtreeSql.get_error_message(cmd.get_connection_handle())
            raise DatabaseError(retcode, errmsg)
                
        
    @staticmethod
    def next_batch_item(cmd): 
        return _ctsql.ctsqlNextBatchItem(cmd.get_command_handle())

    @staticmethod
    def set_low_fetch_size(cmd, size):
        return _ctsql.ctsqlSetTupleCount(cmd.get_command_handle(),size)

    @staticmethod
    def set_scrollable_cursor(cmd, flag):
        return _ctsql.ctsqlSetScrollableCursor(cmd.get_command_handle(), flag)
    
    
