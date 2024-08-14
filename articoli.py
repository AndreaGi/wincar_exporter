import pyctree
import mariadb
import time

from date_parser import convert_date
from fk_utilities import get_id_iva, clear_codice_articolo, get_id_cliente, get_unita_misura

global cache_fornitori
global cache_iva


def commit(mariaCur):
    mariaCur.commit()
    return


def export(treeCur, mariaCur, conn):
    print("Start export articoli magazzino.")
    start_time = time.time()
    record = 1000
    record_esportati = 0
    skip = 0


    while (True):

        treeCur.execute(
            f"SELECT TOP {record} SKIP {skip}"
            "admin.magaz.codice_fornitore, "
            "admin.magaz.categoria_merc_jet07, "
            "admin.magaz.unita_misura, "
            "admin.magaz.codice_articolo, "
            "admin.magaz.descrizione_articolo, "
            "admin.magaz.codice_iva_jtt03, "
            "admin.magaz.prezzo_listino, "
            "admin.magaz.prezzo_precedente, "
            "admin.magaz.data_aggiornamento, "
            "admin.magaz.prezzo_acquisto, "
            "admin.magaz.data_ultimo_acquisto, "
            "admin.magaz.data_ultima_vendita "
            "FROM admin.magaz "
            " ORDER BY admin.magaz.codice_articolo"
        )

        rows = treeCur.fetchall()
        if len(rows) > 0:
            export_row(rows, mariaCur, treeCur)
            commit(conn)
            skip += record
            record_esportati += len(rows)
            print(f"Esportati: {len(rows)}")
        else:
            print(f"Totale record: {record_esportati}")
            print(f"--- {(time.time() - start_time) / 60} minutes ---")
            break


def export_row(rows, mariaCur, treeCur):
    for row in rows:
        id_fornitore = get_id_cliente(row[0], 'F')
        # print(f"id_fornitore:{id_fornitore}")
        id_iva = get_id_iva(row[5])
        posizione = get_posizione_articolo(row[3], treeCur)
        # print(f"{id_fornitore}")

        # print(row)
        articolo = Articolo(id_fornitore, row[1], row[2], row[3], row[4], id_iva, row[6], row[7],
                            row[8], row[9], row[10], row[11], posizione)
        articolo.insert_query(mariaCur)


class Articolo:
    def __init__(self, id_fornitore, categoria_merc, unita_misura, codice_articolo, descrizione, id_iva,
                 prezzo_listino, prezzo_precedente, data_aggiornamento, prezzo_acquisto,
                 data_ultimo_acquisto, data_ultima_vendita, posizione):

        self.data = {
            'id_fornitore': id_fornitore,
            'categoria': categoria_merc.strip(),
            'unita_misura': get_unita_misura(unita_misura),
            'codice_articolo': clear_codice_articolo(codice_articolo.strip()),
            'descrizione': descrizione.strip(),
            'iva': 22,
            'prezzo_listino': prezzo_listino / 100,
            'prezzo_precendente': prezzo_precedente / 100,
            'data_aggiornamento': convert_date(data_aggiornamento),
            'prezzo_acquisto': prezzo_acquisto / 100,
            'data_ultimo_acquisto': convert_date(data_ultimo_acquisto),
            'data_ultima_vendita': convert_date(data_ultima_vendita),
            'posizione': posizione
        }

    def build_sql(self):
        return "INSERT INTO articolo (id_fornitore, unita_misura, codice_articolo, descrizione, " \
               "iva, prezzo_listino, prezzo_precedente, data_aggiornamento, prezzo_acquisto, " \
               "data_ultimo_acquisto, data_ultima_vendita, posizione ) " \
               "VALUES (%(id_fornitore)s, %(unita_misura)s, %(codice_articolo)s, %(descrizione)s, " \
               "%(iva)s, %(prezzo_listino)s, %(prezzo_precendente)s, %(data_aggiornamento)s, " \
               "%(prezzo_acquisto)s, %(data_ultimo_acquisto)s, %(data_ultima_vendita)s, " \
               " %(posizione)s)"

    def insert_query(self, cur):
        if self.data['descrizione'] != '':
            query = self.build_sql()
            # print(self.data)
            cur.execute(query, self.data)


def get_posizione_articolo(codice, treeCur):

    treeCur.execute(
        "SELECT admin.magdep.posizione "
        "FROM admin.magdep "
        " WHERE admin.magdep.codice = '" + codice + "' "
    )

    rows = treeCur.fetchall()
    if len(rows) > 0:
        posizione = rows[0][0]
        posizione = posizione.strip()
        posizione = posizione.replace('/', '')
        if posizione != '':
            return posizione
        return 0
    return 0

