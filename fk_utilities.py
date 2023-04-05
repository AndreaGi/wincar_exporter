import database

global cache_fornitori
global cache_iva
global cache_tipo_pagamento
global cache_tipo_commessa
global cache_scadenze
global cache_cliente
global cache_categoria

maria_connection = database.get_mysql_connection()
cursor = maria_connection.cursor()

cache_fornitori = {}
cache_iva = {}
cache_tipo_pagamento = {}
cache_tipo_commessa = {}
cache_scadenze = {}
cache_cliente = {}
cache_categoria = {}
CODICE_FORNITURE_DEFAULT = '00003'
CODICE_IVA_DEFAULT = '01'


def get_id_fornitore(codice_fornitore):
    global cache_fornitori
    # print(f"{codice_fornitore}")
    if codice_fornitore.strip() == '':
        codice_fornitore = CODICE_FORNITURE_DEFAULT
    if codice_fornitore in cache_fornitori:
        return cache_fornitori[codice_fornitore]

    cursor.execute("SELECT id FROM fornitore WHERE codice = %(fornitore)s", {'fornitore': int(codice_fornitore)})
    values = cursor.fetchall()
    # print(f"{values[0][0]}")
    cache_fornitori[codice_fornitore] = values[0][0]
    return values[0][0]


def get_id_iva(codice_iva):
    global cache_iva
    # print(f"'{codice_iva}'")
    if codice_iva.strip() == '':
        codice_iva = CODICE_IVA_DEFAULT
    if codice_iva in cache_iva:
        return cache_iva[codice_iva]

    cursor.execute("SELECT id FROM e_iva WHERE ext_code = %(codice_iva)s", {'codice_iva': codice_iva})
    values = cursor.fetchall()
    # print(f" iva {values[0][0]}")
    cache_iva[codice_iva] = values[0][0]
    return values[0][0]


def get_id_tipo_pagamento(ext_code):
    global cache_tipo_pagamento
    if ext_code in cache_tipo_pagamento:
        return cache_tipo_pagamento[ext_code]
    cursor.execute("SELECT id FROM e_tipo_pagamento WHERE ext_code = %(ext_code)s", {'ext_code': ext_code})
    values = cursor.fetchall()
    if len(values) == 0:
        return 1
    cache_tipo_pagamento[ext_code] = values[0][0]
    return values[0][0]


def get_id_tipo_commessa(ext_code):
    global cache_tipo_commessa
    if ext_code in cache_tipo_commessa:
        return cache_tipo_commessa[ext_code]
    cursor.execute("SELECT id FROM e_tipo_commessa WHERE ext_code = %(ext_code)s", {'ext_code': ext_code})
    values = cursor.fetchall()
    cache_tipo_commessa[ext_code] = values[0][0]
    return values[0][0]


def get_id_scadenza(ext_code):
    global cache_scadenze
    if ext_code in cache_scadenze:
        return cache_scadenze[ext_code]
    cursor.execute("SELECT id FROM e_scadenze WHERE ext_code = %(ext_code)s", {'ext_code': ext_code})
    values = cursor.fetchall()
    if len(values) == 0:
        return 1
    cache_scadenze[ext_code] = values[0][0]
    return values[0][0]


def get_id_cliente(codice):
    global cache_cliente
    if codice in cache_cliente:
        return cache_cliente[codice]
    cursor.execute("SELECT id FROM cliente WHERE codice = %(codice)s", {'codice': codice})
    values = cursor.fetchall()
    cache_cliente[codice] = values[0][0]
    return values[0][0]


def get_id_categoria(codice):
    global cache_categoria
    if codice in cache_categoria:
        return cache_categoria[codice]
    cursor.execute("SELECT id FROM e_categoria WHERE ext_code = %(codice)s", {'codice': codice})
    values = cursor.fetchall()
    if len(values) == 0:
        return 1
    cache_categoria[codice] = values[0][0]
    return values[0][0]