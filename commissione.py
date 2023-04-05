import pyctree
import mariadb
import time

from date_parser import convert_date
from fk_utilities import get_id_cliente, get_id_categoria, get_id_scadenza, get_id_tipo_pagamento, get_id_tipo_commessa


def export(treeCur, mariaCur):
    print("Start export commissioni.")
    start_time = time.time()
    record = 1000
    record_esportati = 0
    skip = 9000

    while (True):

        treeCur.execute(
            f"SELECT TOP {record} SKIP {skip} "
            "admin.com.telaio, "
            "admin.com.commessa, "
            "admin.com.targa, "
            "admin.com.tipo_commessa_jtt2b, "
            "admin.com.cliente, "
            "admin.com.categoria_jtt06, "
            "admin.com.tipo_pagamento_jtt02, "
            "admin.com.scadenza_jtt01, "
            "admin.com.km, "
            "admin.com.data_commessa, "
            "admin.com.data_chiusura, "
            "admin.com.ora_ingresso_garanzia, "
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
        id_cliente = get_id_cliente(row[4])
        id_categoria = get_id_categoria(row[5])
        id_pagamento = get_id_tipo_pagamento(row[6])
        id_scadenza = get_id_scadenza(row[7])
        tipo_commessa = get_id_tipo_commessa(row[3])

        commessa = Commessa(row[0], row[1], row[2], tipo_commessa, id_cliente, id_categoria, id_pagamento,
                            id_scadenza, row[8], row[9], row[10], row[11], row[12], row[13])
        commessa.insert_query(mariaCur)


class Commessa:
    def __init__(self, telaio, commessa, targa, tipo_commessa, id_cliente, id_categoria, id_pagamento, id_scadenza,
                 km, data_commessa, data_chiusura, ora_ingresso_garanzia, importo_pagato, tipo_documento):

        self.data = {
            'telaio': telaio.strip(),
            'commessa': commessa,
            'targa': targa.strip(),
            'tipo_commessa': tipo_commessa,
            'id_cliente': id_cliente,
            'id_categoria': id_categoria,
            'id_tipo_pagamento': id_pagamento,
            'id_scadenza': id_scadenza,
            'km': km,
            'data_commessa': convert_date(data_commessa),
            'data_chiusura': convert_date(data_chiusura),
            'ora_ingresso_garanzia': ora_ingresso_garanzia,
            'importo_pagato': importo_pagato,
            'tipo_documento': tipo_documento,
        }

    def build_sql(self):
        return "INSERT INTO commessa (id_cliente, telaio, numero, targa, id_tipo_commessa, id_categoria,  " \
               "id_tipo_pagamento, id_scadenza, km, data_commessa, data_chiusura, ora_garanzia, " \
               "importo_pagato, tipo_documento) " \
               "VALUES (%(id_cliente)s, %(telaio)s, %(commessa)s, %(targa)s, %(tipo_commessa)s, %(id_categoria)s, " \
               "%(id_tipo_pagamento)s, %(id_scadenza)s, %(km)s, %(data_commessa)s, %(data_chiusura)s, " \
               "%(ora_ingresso_garanzia)s, %(importo_pagato)s, %(tipo_documento)s)"

    def insert_query(self, cur):
        query = self.build_sql()
        # print(self.data)
        cur.execute(query, self.data)
