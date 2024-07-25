import pyctree
import mariadb
import time

from date_parser import convert_date


def commit(mariaCur):
    mariaCur.commit()
    return


def export(treeCur, mariaCur, conn):
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
            "admin.com.cliente, "
            "admin.com.tipo_pagamento_jtt02, "
            "admin.com.scadenza_jtt01, "
            "admin.com.km, "
            "admin.com.data_commessa, "
            "admin.com.data_chiusura, "
            "admin.com.ora_ingresso_garanzia, "
            "admin.com.importo_pagato, "
            "admin.com.nr_documento, "
            "admin.com.data_documento "
            "FROM admin.com "
            "ORDER BY admin.com.commessa "
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
    from fk_utilities import get_id_cliente, get_id_scadenza, get_id_tipo_pagamento, \
        get_id_tipo_commessa, \
        get_id_auto

    for row in rows:
        # print(row)
        id_cliente = get_id_cliente(row[4], 'C')
        id_pagamento = get_id_tipo_pagamento(row[5])
        id_scadenza = get_id_scadenza(row[6])
        tipo_commessa = get_id_tipo_commessa(row[3])
        if tipo_commessa == 1:
            tipo_commessa = 'E'
        else:
            tipo_commessa = 'I'
        id_auto = get_id_auto(row[0], row[2], id_cliente)

        commessa = Commessa(id_auto, row[1], tipo_commessa, id_cliente, id_pagamento,
                            id_scadenza, row[7], row[8], row[9], row[10], row[11], row[12], row[13])
        commessa.insert_query(mariaCur)


class Commessa:
    def __init__(self, id_auto, commessa, tipo_commessa, id_cliente, id_pagamento, id_scadenza,
                 km, data_commessa, data_chiusura, ora_ingresso_garanzia, importo_pagato, nr_fattura, data_fattura):

        self.data = {
            'commessa': commessa,
            'id_auto': id_auto,
            'tipo_commessa': tipo_commessa,
            'id_cliente': id_cliente,
            'id_tipo_pagamento': id_pagamento,
            'id_scadenza': id_scadenza,
            'km': km,
            'data_commessa': convert_date(data_commessa),
            'data_chiusura': convert_date(data_chiusura),
            'ora_ingresso_garanzia': ora_ingresso_garanzia,
            'importo_pagato': importo_pagato / 100,
            'nr_fattura': nr_fattura,
            'data_fattura': convert_date(data_fattura),
        }

    def build_sql(self):
        return "INSERT INTO commessa (id_cliente, id_auto, numero, tipo,  " \
               "id_tipo_pagamento, id_scadenza, km, data_commessa, data_chiusura, ora_garanzia, " \
               "importo_pagato, nr_fattura, data_fattura) " \
               "VALUES (%(id_cliente)s, %(id_auto)s, %(commessa)s, %(tipo_commessa)s, " \
               "%(id_tipo_pagamento)s, %(id_scadenza)s, %(km)s, %(data_commessa)s, %(data_chiusura)s, " \
               "%(ora_ingresso_garanzia)s, %(importo_pagato)s, %(nr_fattura)s, %(data_fattura)s)"

    def insert_query(self, cur):
        query = self.build_sql()
        # print(self.data)
        cur.execute(query, self.data)
