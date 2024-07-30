import time
import uuid

from date_parser import convert_date
from fk_utilities import get_id_commessa, get_id_movimento, get_id_causale, \
    get_id_articolo, get_id_bolla, update_movimento_cache, update_bolla_cache


def commit(mariaCur):
    mariaCur.commit()
    return

def export(treeCur, mariaCur, conn):
    print ("Start lettura movimenti")
    start_time = time.time()
    record = 1000
    record_letti = 0
    skip = 0

    while (True):

        treeCur.execute(
            f"SELECT TOP {record} SKIP {skip}"
            "admin.mov.data_reg, "
            "admin.mov.nr_reg, "
            "admin.mov.riga, "
            "admin.mov.codice_articolo, "
            "admin.mov.causale_movimento_jet10, "
            "admin.mov.codice_cliente, "
            "admin.mov.numero_documento, "
            "admin.mov.numero_riga, "
            "admin.mov.quantita, "
            "admin.mov.prezzo_listino, "
            "admin.mov.prezzo_netto, "
            "admin.mov.sconto1 "
            "FROM admin.mov "
            " ORDER BY admin.mov.nr_reg, admin.mov.riga "
        )

        rows = treeCur.fetchall()
        if len(rows) > 0:
            export_rows(rows, mariaCur)
            commit(conn)
            skip += record
            record_letti += len(rows)
            print(f"Record letti: {len(rows)}")
        else:
            print(f"Totale record: {record_letti}")
            print(f"--- {(time.time() - start_time) / 60} minutes ---")
            break

def export_rows(rows, mariaCur):
    for row in rows:
        # print(row)
        mov_date = convert_date(row[0])
        if mov_date.year >= 2019:
            is_commessa = True
            fk_id = get_id_commessa(row[6])
            id_articolo = get_id_articolo(row[3])
            if fk_id is None:
                is_commessa = False
                fk_id = get_id_bolla(row[6])
                if fk_id is None:
                    fk_id = generate_bolla(row[6], mov_date, mariaCur)

            if fk_id is not None:
                mov_id = get_id_movimento(row[1])
                if mov_id is None:
                    mov_id = add_movimento(row, is_commessa, mariaCur)

                quantita = row[8] if row[8] is not None else 0
                prezzo_listino = row[9] if row[9] is not None else 0
                prezzo_netto = row[10] if row[10] is not None else 0
                sconto = row[11] if row[11] is not None else 0
                riga_mov = RigaMovimento(mov_id, row[7], id_articolo, is_commessa, fk_id, quantita, prezzo_listino, prezzo_netto, sconto)
                riga_mov.insert_query(mariaCur)


def add_movimento(row, is_commessa, mariaCur):
    id_causale = get_id_causale(row[4])
    movimento_data = Movimento(row[1], row[0], id_causale)
    movimento_data.insert_query(mariaCur)
    movId = mariaCur.lastrowid
    update_movimento_cache(movId, row[1])
    return movId


def generate_bolla(document_nr, date, mariaCur):
    data = Bolla(document_nr, date)
    bolla_id = data.insert_query(mariaCur)
    update_bolla_cache(bolla_id, document_nr)
    return bolla_id


class RigaMovimento:

    def __init__(self, id_mov, numero_riga, id_articolo, is_commessa, id_ext, quantita, prezzo_listino, prezzo_netto, sconto):

        self.data = {
            "uuid": str(uuid.uuid4()),
            "id_movimento": id_mov,
            "numero_riga": numero_riga,
            "id_articolo": id_articolo,
            "isCommessa": is_commessa,
            "id_ext": id_ext,
            "quantita": quantita,
            "prezzo_listino": prezzo_listino / 100,
            "prezzo_netto": prezzo_netto / 100,
            "sconto": sconto
        }

    def build_sql(self, isCommessa):
        sql = "INSERT INTO riga_movimento (uuid, id_movimento, numero_riga, id_articolo, id_commessa, " \
           "id_bolla, quantita, prezzo_listino, prezzo_netto, sconto) " \
           "VALUES (%(uuid)s, %(id_movimento)s, %(numero_riga)s, %(id_articolo)s,"
        if isCommessa is True:
            sql = sql + " %(id_ext)s, NULL, %(quantita)s, %(prezzo_listino)s, %(prezzo_netto)s, %(sconto)s)"
        else:
            sql = sql + " NULL, %(id_ext)s, %(quantita)s, %(prezzo_listino)s, %(prezzo_netto)s, %(sconto)s)"
        return sql

    def insert_query(self, cur):
        query = self.build_sql(self.data['isCommessa'])
        # print("RIGA MOV:" + query)
        # print(self.data)
        cur.execute(query, self.data)


class Movimento:
    def __init__(self, nr_reg, data_reg, id_causale):

        self.data = {
            "nr_reg": nr_reg,
            "id_causale": id_causale,
            "data_reg": convert_date(data_reg),
        }

    def build_sql(self):
        return "INSERT INTO movimento (nr_reg, causale, data_reg) " \
                "VALUES (%(nr_reg)s, %(id_causale)s, %(data_reg)s)"

    def insert_query(self, cur):
        if self.data['nr_reg']:
            query = self.build_sql()
            # print("MOV:" + query)
            # print(self.data)
            cur.execute(query, self.data)
            return cur.lastrowid
        return None


class Bolla:

    def __init__(self, document_nr, date):

        self.data = {
            "document_nr": document_nr,
            "data": date
        }


    def build_sql(self):
        return "INSERT INTO bolla (document_nr, data) VALUES (%(document_nr)s, %(data)s)"


    def insert_query(self, cursor):
        query = self.build_sql()
        # print("BOLLA:" + query)
        # print(self.data)
        cursor.execute(query, self.data)
        return cursor.lastrowid