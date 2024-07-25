import database
from storico_auto import Auto

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
global cache_id_auto_telaio
global cache_id_auto_targa

maria_connection = database.get_mysql_connection()
cursor = maria_connection.cursor()

cache_bolla = {}
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
cache_id_auto_telaio = {}
cache_id_auto_targa = {}
cache_id_movimento = {}
cache_id_causale = {}
CODICE_FORNITORE_DEFAULT = '00003'
CODICE_CLIENTE_DEFAULT = '0'
CODICE_IVA_DEFAULT = '01'


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


def get_id_cliente(codice, tipo):
    global cache_cliente
    if tipo == 'F':
        codice = codice.strip()
        if codice == '':
            codice = CODICE_FORNITORE_DEFAULT
        codice = int(codice)
    else:
        codice = codice.strip()
        if codice == '':
            codice = CODICE_CLIENTE_DEFAULT
    if codice in cache_cliente:
        return cache_cliente[codice]
    cursor.execute("SELECT id FROM cliente WHERE codice = %(codice)s AND tipo = %(tipo)s ", {'codice': codice, 'tipo': tipo})
    values = cursor.fetchall()
    # print(f"values: {values}, codice: {codice}, tipo: {tipo}")
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


def get_id_bolla(numero):
    global cache_bolla
    if numero in cache_bolla:
        return cache_bolla[numero]
    cursor.execute("SELECT id FROM bolla WHERE document_nr = %(numero)s", {'numero': numero})
    values = cursor.fetchall()
    if len(values) > 0:
        cache_categoria[numero] = values[0][0]
        return values[0][0]
    return None

def update_bolla_cache(id, nr_reg):
    global cache_bolla
    cache_bolla[nr_reg] = id


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


def get_id_movimento(nr_reg):
    global cache_id_movimento
    if nr_reg in cache_id_movimento:
        return cache_id_movimento[nr_reg]
    cursor.execute("SELECT id FROM movimento WHERE nr_reg = %(nr_reg)s", {'nr_reg': nr_reg})
    values = cursor.fetchall()
    if len(values) > 0:
        cache_id_movimento[nr_reg] = values[0][0]
        return values[0][0]
    return None

def update_movimento_cache(id, nr_reg):
    global cache_id_movimento
    cache_id_movimento[nr_reg] = id


def get_id_causale(codice):
    global cache_id_causale
    if codice in cache_id_causale:
        return cache_id_causale[codice]
    cursor.execute("SELECT id FROM e_causale_mov WHERE ext_code = %(codice)s", {'codice': codice})
    values = cursor.fetchall()
    if len(values) > 0:
        cache_id_causale[codice] = values[0][0]
        return values[0][0]
    return None


def get_id_auto(telaio, targa, id_cliente):
    global maria_connection
    global cursor
    maria_connection = database.get_mysql_connection()
    cursor = maria_connection.cursor()
    global cache_id_auto_telaio
    if telaio in cache_id_auto_telaio:
        return cache_id_auto_telaio[telaio]
    if targa in cache_id_auto_targa:
        return cache_id_auto_targa[targa]
    if telaio != '':
        cursor.execute("SELECT id FROM auto WHERE telaio = %(telaio)s",
                   {'telaio': telaio})
        values = cursor.fetchall()
        if len(values) > 0:
            cache_id_auto_telaio[telaio] = values[0][0]
            return values[0][0]
    if targa != '':
        cursor.execute("SELECT id FROM auto WHERE telaio = %(targa)s",
                       {'targa': targa})
        values = cursor.fetchall()
        if len(values) > 0:
            cache_id_auto_targa[targa] = values[0][0]
            return values[0][0]

    auto = Auto(id_cliente, 63, telaio, targa, '', 0)
    auto.insert_query(cursor)
    maria_connection.commit()
    return cursor.lastrowid

def get_unita_misura(unita):
    if unita.strip() in ['01','R','0R','19','20','3R','99','9R']:
        return 'PZ'
    return unita.strip()


def clear_codice_articolo(codiceArticolo):
    codice_articolo = codiceArticolo.strip()
    codice_articolo = ' '.join(codice_articolo.split())
    return codice_articolo
