import database

global cache_fornitori
global cache_iva
global cache_tipo_pagamento
global cache_tipo_commessa
global cache_scadenze
global cache_cliente
global cache_categoria
global cache_commissione
global cache_tipo_riga
global cache_articoli
global cache_marca_auto

maria_connection = database.get_mysql_connection()
cursor = maria_connection.cursor()

cache_fornitori = {}
cache_iva = {}
cache_tipo_pagamento = {}
cache_tipo_commessa = {}
cache_scadenze = {}
cache_cliente = {}
cache_categoria = {}
cache_commissione = {}
cache_tipo_riga = {}
cache_articoli = {}
cache_marca_auto = {}
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
    if len(values) == 0:
        return None
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
    if len(values) == 0:
        return 0
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


def get_id_commessa(numero):
    cursor.execute("SELECT id FROM commessa WHERE numero = %(numero)s", {'numero': numero})
    values = cursor.fetchall()
    if len(values) > 0:
        return values[0][0]
    return None


def get_id_tipo_riga(codice):
    global cache_tipo_riga
    if codice in cache_tipo_riga:
        return cache_tipo_riga[codice]
    cursor.execute("SELECT id FROM e_tipo_riga WHERE ext_code = %(codice)s", {'codice': codice})
    values = cursor.fetchall()
    cache_tipo_riga[codice] = values[0][0]
    return values[0][0]

def get_id_articolo(codice):
    global cache_articoli
    if codice in cache_articoli:
        return cache_articoli[codice]
    cursor.execute("SELECT id FROM articolo WHERE codice_articolo = %(codice)s", {'codice': clear_codice_articolo(codice)})
    values = cursor.fetchall()
    if len(values) > 0:
        cache_articoli[codice] = values[0][0]
        return values[0][0]
    return None

def get_id_marca(codice):
    global cache_marca_auto
    if codice in cache_marca_auto:
        return cache_marca_auto[codice]
    cursor.execute("SELECT id FROM e_marca WHERE ext_code = %(codice)s", {'codice': codice})
    values = cursor.fetchall()
    if len(values) > 0:
        cache_marca_auto[codice] = values[0][0]
        return values[0][0]
    return 63

def clear_codice_articolo(codiceArticolo):
    codice_articolo = codiceArticolo.strip()
    codice_articolo = ' '.join(codice_articolo.split())
    return codice_articolo