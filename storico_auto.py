import pyctree
import mariadb
import time

from fk_utilities import get_id_cliente, get_id_marca


def commit(mariaCur):
    mariaCur.commit()
    return


def export(treeCur, mariaCur, conn):
    print("Start export storico auto.")
    start_time = time.time()
    record = 1000
    record_esportati = 0
    skip = 0

    while (True):

        treeCur.execute(
            f"SELECT TOP {record} SKIP {skip} "
            "admin.stoaut.codice_cliente, "
            "admin.stoaut.telaio, "
            "admin.stoaut.codice_marca_jtt76, "
            "admin.stoaut.descrizione_modello, "
            "admin.stoaut.targa, "
            "admin.stoaut.nr_interventi_officina "
            "FROM admin.stoaut "
            "ORDER BY admin.stoaut.progressivo "
        )

        rows = treeCur.fetchall()
        if len(rows) > 0:
            export_row(rows, mariaCur)
            commit(conn)
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
        id_cliente = get_id_cliente(row[0])
        id_marca = get_id_marca(row[2])

        if id_cliente != 0:
            storico_auto = Auto(id_cliente, id_marca, row[1], row[4], row[3], row[5])
            storico_auto.insert_query(mariaCur)


class Auto:

    def __init__(self, id_cliente, id_marca, telaio, targa, modello, nr_interventi):

        self.data = {
            'id_cliente': id_cliente,
            'id_marca': id_marca,
            'telaio': telaio.strip(),
            'targa': targa.strip(),
            'modello': modello.strip(),
            'nr_interventi': nr_interventi,
        }

    def build_sql(self):
        return "INSERT INTO auto (id_cliente, id_marca, telaio, targa, " \
               "modello, nr_interventi) " \
               "VALUES (%(id_cliente)s, %(id_marca)s, %(telaio)s, %(targa)s, " \
               "%(modello)s, %(nr_interventi)s)"

    def insert_query(self, cur):
        query = self.build_sql()
        # print(self.data)
        cur.execute(query, self.data)