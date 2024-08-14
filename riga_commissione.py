import pyctree
import mariadb
import uuid
import time


from fk_utilities import get_id_commessa, get_id_articolo


def commit(mariaCur):
    mariaCur.commit()
    return


def export(treeCur, mariaCur, conn):
    print("Start export righe commissioni.")
    start_time = time.time()
    record = 10000
    record_esportati = 0
    skip = 0

    while (True):

        treeCur.execute(
            f"SELECT  TOP {record} SKIP {skip}"
            " admin.comrig.nr_commessa, "
            "admin.comrig.nr_riga, "
            "admin.comrig.codice_articolo, "
            "admin.comrig.descrizione, "
            "admin.comrig.tipo_addebito,"
            "admin.comrig.um, "
            "admin.comrig.qta, "
            "admin.comrig.prezzo "
            "FROM admin.comrig "
            "ORDER BY admin.comrig.nr_commessa, admin.comrig.nr_riga"
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
    DESC = "DESC"
    ART = "ART"
    for row in rows:
        id_commessa = get_id_commessa(row[0])
        id_articolo = get_id_articolo(row[2])
        tipo_riga = DESC
        if id_articolo is not None:
            tipo_riga = ART

        riga = Riga_Commessa(id_commessa, tipo_riga, row[1], id_articolo, row[3], row[4], row[5], row[6], row[7])
        riga.insert_query(mariaCur)


class Riga_Commessa:
    def __init__(self, id_commessa, tipo_riga, numero_riga, id_articolo, descrizione, addebito, um, quantita, prezzo):

        self.data = {
            'uuid': str(uuid.uuid4()),
            'id_commessa': id_commessa,
            'tipo_riga': tipo_riga,
            'numero_riga': numero_riga + 1,
            'id_articolo': id_articolo,
            'descrizione': descrizione.strip(),
            'addebito': addebito.strip(),
            'um': um,
            'quantita': quantita,
            'prezzo': prezzo / 100,
        }

    def build_sql(self):
        return "INSERT INTO riga_commessa (uuid, id_commessa, tipo_riga, numero_riga, id_articolo, " \
               "descrizione, charge, um, quantita, prezzo, iva ) " \
               "VALUES (%(uuid)s, %(id_commessa)s, %(tipo_riga)s, %(numero_riga)s, %(id_articolo)s, %(descrizione)s, " \
                "%(addebito)s, %(um)s, %(quantita)s, %(prezzo)s, 22)"

    def insert_query(self, cur):
        query = self.build_sql()
        # print(self.data)
        cur.execute(query, self.data)
