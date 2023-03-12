import pyctree
import mariadb
import time

from date_parser import convert_date


def export(treeCur, mariaCur):
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
            "admin.magaz.qta_confezione, "
            "admin.magaz.prezzo_listino, "
            "admin.magaz.prezzo_precedente, "
            "admin.magaz.data_aggiornamento, "
            "admin.magaz.prezzo_acquisto, "
            "admin.magaz.data_ultimo_acquisto, "
            "admin.magaz.data_ultima_vendita, "
            "admin.magaz.data_creazione, "
            "admin.magaz.codice_solo, "
            "admin.magaz.precodice_solo "
            "FROM admin.magaz "
            " ORDER BY admin.magaz.codice_articolo"
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
        self.codice_fornitore = codice_fornitore
        self.categoria = categoria_merc.strip()
        self.unita_misura = unita_misura.strip()
        self.codice_articolo = codice_articolo.strip()
        self.descrizione = descrizione.strip()
        self.cod_iva = cod_iva
        self.quantita_confezione = quantita_confezione
        self.prezzo_listino = prezzo_listino / 100
        self.prezzo_precendente = prezzo_precedente / 100
        self.data_aggiornamento = convert_date(data_aggiornamento)
        self.prezzo_acquisto = prezzo_acquisto / 100
        self.data_ultimo_acquisto = convert_date(data_ultimo_acquisto)
        self.data_ultima_vendita = convert_date(data_ultima_vendita)
        self.data_creazione = convert_date(data_creazione)
        self.codice_solo = codice_solo.strip()
        self.precodice_solo = precodice_solo.strip()

    def build_sql(self):
        return f"INSERT INTO articolo (codice_fornitore, categoria, unita_misura, codice_articolo, descrizione, " \
               f"cod_iva, quantita_confezione, prezzo_listino, prezzo_precedente, data_aggiornamento, prezzo_acquisto, " \
               f"data_ultimo_acquisto, data_ultima_vendita, data_creazione, codice_solo, precodice_solo ) VALUES" \
               f"( \"{self.codice_fornitore}\", \"{self.categoria}\", \"{self.unita_misura}\", \"{self.codice_articolo}\", \"{self.descrizione}\", " \
               f"\"{self.cod_iva}\", {self.quantita_confezione}, {self.prezzo_listino}, {self.prezzo_precendente}, {self.data_aggiornamento}," \
               f"{self.prezzo_acquisto}, {self.data_ultimo_acquisto}, {self.data_ultima_vendita}, {self.data_creazione}, " \
               f"\"{self.codice_solo}\", \"{self.precodice_solo}\" ); "

    def insert_query(self, cur):
        query = self.build_sql()
        # print(query)
        cur.execute(query)
