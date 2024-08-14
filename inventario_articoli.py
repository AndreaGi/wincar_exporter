import time

from date_parser import convert_year
from fk_utilities import get_id_articolo

global cache_articolo
def commit(mariaCur):
    mariaCur.commit()
    return

def export(treeCur, mariaCur, conn):
    print ("Start lettura inventario")
    start_time = time.time()
    record = 1000
    record_letti = 0
    skip = 0

    while (True):

        treeCur.execute(
            f"SELECT TOP {record} SKIP {skip}"
            "admin.magpro.codice, "
            "admin.magpro.anno, "
            "admin.magpro.qta_iniziale, "
            "admin.magpro.qta_acquistata, "
            "admin.magpro.qta_venduta "
            "FROM admin.magpro "
            " ORDER BY admin.magpro.codice "
        )

        rows = treeCur.fetchall()
        if len(rows) > 0:
            update_data(rows, mariaCur, treeCur)
            commit(conn)
            skip += record
            record_letti += len(rows)
            print(f"Record letti: {len(rows)}")
        else:
            print(f"Totale record: {record_letti}")
            print(f"--- {(time.time() - start_time) / 60} minutes ---")
            break


def update_data(rows, mariaCur, treeCur):
    for row in rows:
        # print(f"Updating {row}")
        id_articolo = get_id_articolo(row[0])
        qta_impegnata = get_qta_impegnata(row[0], treeCur)
        data = InvLine(id_articolo, row[1], row[2], row[3], row[4], qta_impegnata)
        data.insert_query(mariaCur)


class InvLine:
    def __init__(self, id_articolo, anno, qta_iniziale, qta_acquistata, qta_venduta, qta_impegnata):

        self.data = {
            "id_articolo": id_articolo,
            "anno": convert_year(anno),
            "qta_iniziale": float(qta_iniziale),
            "qta_acquistata": float(qta_acquistata),
            "qta_venduta": float(qta_venduta),
            "qta_impegnata": float(qta_impegnata)
        }

    def build_sql(self):
        return "INSERT INTO magazzino (id_articolo, anno, qta_iniziale, qta_acquistata, qta_venduta, qta_impegnata ) " \
                "VALUES (%(id_articolo)s, %(anno)s, %(qta_iniziale)s, %(qta_acquistata)s, %(qta_venduta)s," \
                 " %(qta_impegnata)s )"

    def insert_query(self, cur):
        if self.data["id_articolo"]:
            query = self.build_sql()
            cur.execute(query, self.data)


def get_qta_impegnata(codice, treeCur):

    treeCur.execute(
        "SELECT admin.magdep.qta_impegnata "
        "FROM admin.magdep "
        " WHERE admin.magdep.codice = '" + codice + "' "
    )

    rows = treeCur.fetchall()
    if len(rows) > 0:
        qta = rows[0][0]
        if qta > 0.0:
            return qta
        return 0
    return 0
