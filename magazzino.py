import pyctree
import mariadb
import time

from date_parser import convert_date
from fk_utilities import get_id_cliente, get_id_categoria, get_id_scadenza, get_id_tipo_pagamento, get_id_tipo_commessa, \
    get_id_commessa, get_id_tipo_riga, get_id_articolo


def export(treeCur, mariaCur):
    print("Start export magazzino.")
    start_time = time.time()
    record = 1000
    record_esportati = 0
    skip = 0

    while (True):

        treeCur.execute(
            f"SELECT  TOP {record} SKIP {skip}"
            " admin.comrig.nr_commessa, "
            "admin.comrig.tipo_riga_jtt27, "
            "admin.comrig.nr_riga, "
            "admin.comrig.codice_articolo, "
            "admin.comrig.descrizione, "
            "admin.comrig.um, "
            "admin.comrig.qta, "
            "admin.comrig.prezzo "
            "FROM admin.comrig "
            "ORDER BY admin.comrig.nr_commessa, admin.comrig.nr_riga"
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
        print(row)
        id_commessa = get_id_commessa(row[0])
        id_tipo_riga = get_id_tipo_riga(row[1])
        id_articolo = get_id_articolo(row[3])

        riga = Riga_Commessa(id_commessa, id_tipo_riga, row[2], id_articolo, row[4], row[5], row[6], row[7])
        riga.insert_query(mariaCur)


class Riga_Commessa:
    def __init__(self, id_commessa, id_tipo_riga, numero_riga, id_articolo, descrizione, um, quantita, prezzo):

        self.data = {
            'id_commessa': id_commessa,
            'id_tipo': id_tipo_riga,
            'numero_riga': numero_riga,
            'id_articolo': id_articolo,
            'descrizione': descrizione.strip(),
            'um': um,
            'quantita': quantita,
            'prezzo': prezzo / 100,
        }

    def build_sql(self):
        return "INSERT INTO riga_commessa (id_commessa, id_tipo_riga, numero_riga, id_articolo, " \
               "descrizione, um, quantita, prezzo ) " \
               "VALUES (%(id_commessa)s, %(id_tipo)s, %(numero_riga)s, %(id_articolo)s, %(descrizione)s, %(um)s, " \
               "%(quantita)s, %(prezzo)s)"

    def insert_query(self, cur):
        query = self.build_sql()
        # print(self.data)
        cur.execute(query, self.data)
