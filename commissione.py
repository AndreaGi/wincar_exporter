import pyctree
import mariadb
import time

from date_parser import convert_date


def export(treeCur, mariaCur):
    print("Start export commissioni.")
    start_time = time.time()
    record = 1000
    record_esportati = 0
    skip = 0

    while (True):

        treeCur.execute(
            f"SELECT TOP {record} SKIP {skip} "
            "admin.com.telaio, "
            "admin.com.commessa, "
            "admin.com.targa, "
            "admin.com.tipo_commessa_jtt2b, "
            "admin.com.flag, "
            "admin.com.cliente, "
            "admin.com.categoria_jtt06, "
            "admin.com.tipo_pagamento_jtt02, "
            "admin.com.scadenza_jtt01, "
            "admin.com.km, "
            "admin.com.data_preventivo, "
            "admin.com.nr_preventivo, "
            "admin.com.data_commessa, "
            "admin.com.data_chiusura, "
            "admin.com.nr_documento, "
            "admin.com.ora_ingresso_garanzia, "
            "admin.com.flag_ricevuta_fiscale, "
            "admin.com.importo_pagato, "
            "admin.com.tipo_documento "
            "FROM admin.com "
            "ORDER BY admin.com.commessa "
        )

        rows = treeCur.fetchall()
        if len(rows) > 0:
            export_row(rows, mariaCur)
            skip += record
            record_esportati += len(rows)
            print(f"Esportati: {len(rows)}")
        else:
            print(f"Totale record: {record_esportati}")
            print(f"--- {(time.time() - start_time) / 60} minutes ---")
            break


def export_row(rows, mariaCur):
    for row in rows:
        # print(row)
        articolo = Articolo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                            row[9], row[10], row[11], row[12], row[13], row[14], row[15])
        articolo.insert_query(mariaCur)


class Articolo:
    def __init__(self, codice_fornitore, categoria_merc, unita_misura, codice_articolo, descrizione, cod_iva,
                 quantita_confezione, prezzo_listino, prezzo_precedente, data_aggiornamento, prezzo_acquisto,
                 data_ultimo_acquisto, data_ultima_vendita, data_creazione, codice_solo, precodice_solo):
        self.data = {
            'codice_fornitore': codice_fornitore,
            'categoria': categoria_merc.strip(),
            'unita_misura': unita_misura.strip(),
            'codice_articolo': codice_articolo.strip(),
            'descrizione': descrizione.strip(),
            'cod_iva': cod_iva.strip(),
            'quantita_confezione': quantita_confezione,
            'prezzo_listino': prezzo_listino / 100,
            'prezzo_precendente': prezzo_precedente / 100,
            'data_aggiornamento': convert_date(data_aggiornamento),
            'prezzo_acquisto': prezzo_acquisto / 100,
            'data_ultimo_acquisto': convert_date(data_ultimo_acquisto),
            'data_ultima_vendita': convert_date(data_ultima_vendita),
            'data_creazione': convert_date(data_creazione),
            'codice_solo': codice_solo.strip(),
            'precodice_solo': precodice_solo.strip(),
        }

    def build_sql(self):
        return "INSERT INTO articolo (codice_fornitore, categoria, unita_misura, codice_articolo, descrizione, " \
               "cod_iva, quantita_confezione, prezzo_listino, prezzo_precedente, data_aggiornamento, prezzo_acquisto, " \
               "data_ultimo_acquisto, data_ultima_vendita, data_creazione, codice_solo, precodice_solo ) " \
               "VALUES (%(codice_fornitore)s, %(categoria)s, %(unita_misura)s, %(codice_articolo)s, %(descrizione)s, " \
               "%(cod_iva)s, %(quantita_confezione)s, %(prezzo_listino)s, %(prezzo_precendente)s, %(data_aggiornamento)s, " \
               "%(prezzo_acquisto)s, %(data_ultimo_acquisto)s, %(data_ultima_vendita)s, %(data_creazione)s," \
               " %(codice_solo)s, %(precodice_solo)s)"

    def insert_query(self, cur):
        if self.data['descrizione'] != '':
            query = self.build_sql()
            # print(self.data)
            cur.execute(query, self.data)
