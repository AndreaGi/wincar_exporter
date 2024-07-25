import pyctree
import mariadb
import time


def exportClienti(treeCur, mariaCur, conn):
    print("Start export clienti.")
    export(treeCur, mariaCur, conn)


def commit(conn):
    conn.commit()
    return


def export(treeCur, mariaCur, conn):
    start_time = time.time()
    record = 1000
    record_esportati = 0
    skip = 0

    while(True):

        treeCur.execute(
            f"SELECT TOP {record} SKIP {skip}" 
            "admin.clfo.codice, " 
            "admin.clfo.ragione_sociale, " 
            "admin.clfo.ragione_sociale2, " 
            "admin.clfo.indirizzo, "
            "admin.clfo.cap, "
            "admin.clfo.citta, "
            "admin.clfo.provincia, "
            "admin.clfo.codice_comune_aci, "
            "admin.clfo.sesso, "
            "admin.clfo.telefono, "
            "admin.clfo.fax, "
            "admin.clfo.codice_fiscale, "
            "admin.clfo.partita_iva, "
            "admin.clfo.banca_appoggio, "
            "admin.clfo.codice_abi, "
            "admin.clfo.codice_cab, "
            "admin.clfo.conto_corrente, "
            "admin.clfo.email, "
            "admin.clfo.c_cf "
            "FROM admin.clfo "
            " ORDER BY admin.clfo.codice"
        )

        rows = treeCur.fetchall()
        if len(rows) > 0:
            exportRows(rows, mariaCur)
            commit(conn)
            skip += record
            record_esportati += len(rows)
            print(f"Esportati: {len(rows)}")
        else:
            print(f"Totale record: {record_esportati}")
            print(f"--- {(time.time() - start_time)/60} minutes ---")
            break


def exportRows(rows, mariaCur):
    for row in rows:
        # print(row)
        cliente = Cliente(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                          row[9], row[10], row[17], row[11], row[12], row[13], row[14], row[15], row[16], row[18])

        cliente.insertQuery(mariaCur)


class Cliente:
    def __init__(self, codice, ragione_sociale, ragione_sociale2,
                 indirizzo, cap, citta, provincia, codice_comune_aci,
                 sesso, telefono, fax, email, codice_fiscale, partita_iva,
                nome_banca, abi, cab, conto, cliente_flag):

        self.sesso = None
        self.azienda = 0
        if sesso.strip() != '':
            if sesso == 'M' or sesso == 'F':
                self.sesso = sesso.strip()
            else:
                self.azienda = 1

        self.dettagli_indirizzo = Indirizzo(indirizzo, cap, citta, provincia, codice_comune_aci)
        self.dettagli_banca = DettagliBanca(nome_banca, abi, cab, conto)

        self.data = {
           'codice': codice.strip(),
           'ragione_sociale':  f"{ragione_sociale} {ragione_sociale2}".strip().replace("\"", ""),
            'id_indirizzo': None,
            'sesso': self.sesso,
            'azienda': self.azienda,
            'telefono': telefono.strip(),
            'fax': fax.strip(),
            'email': email.strip(),
            'codice_fiscale': codice_fiscale.strip(),
            'partita_iva': partita_iva.strip(),
            'id_banca': None,
            'cliente_flag': cliente_flag
        }

    def buildSQLQuery(self):
        return f"INSERT INTO cliente (codice, ragione_sociale, indirizzo, sesso, azienda, telefono," \
               "fax, email, codice_fiscale, partita_iva, banca, tipo) VALUES " \
               "( %(codice)s, %(ragione_sociale)s, %(id_indirizzo)s, %(sesso)s, %(azienda)s, %(telefono)s, " \
               "%(fax)s, %(email)s, %(codice_fiscale)s, %(partita_iva)s, %(id_banca)s, %(cliente_flag)s)"
               # f"(\"{self.codice}\", \"{self.ragione_sociale}\", {self.id_indirizzo}, \"{self.sesso}\", {self.azienda}, " \
               # f"\"{self.telefono}\", \"{self.fax}\", \"{self.email}\", \"{self.codice_fiscale}\", " \
               # f"\"{self.partita_iva}\", {self.id_banca});"

    def insertQuery(self, cur):
        if self.dettagli_indirizzo.data['indirizzo'].strip() != "":
            self.data['id_indirizzo'] = self.dettagli_indirizzo.insertQuery(cur)

        if self.dettagli_banca.data['banca'].strip() != "":
            self.data['id_banca'] = self.dettagli_banca.insertQuery(cur)

        query = self.buildSQLQuery()
        # print(self.data)
        cur.execute(query, self.data)


class DettagliBanca:
    def __init__(self, banca, abi, cab, conto):
        self.abi = None
        if abi.strip().replace("\"", "") != "":
            self.abi = abi.strip().replace("\"", "")

        self.cab = None
        if cab.strip().replace("\"", "") != "":
            self.cab = cab.strip().replace("\"", "")

        self.data = {
            'banca': banca.strip().replace("\"", ""),
            'abi': self.abi,
            'cab': self.cab,
            'conto': conto.strip().replace("\"", "")

        }

    def buildSQLInsert(self):
        return "INSERT INTO dettagli_banca (banca, abi, cab, conto) VALUES " \
               "(%(banca)s, %(abi)s, %(cab)s, %(conto)s) "

    def insertQuery(self, cur):
        query = self.buildSQLInsert()
        # print(query)
        cur.execute(query, self.data)
        return cur.lastrowid


class Indirizzo:
    def __init__(self, indirizzo, cap, citta, provincia, cod_aci):

        self.cod_aci = None
        if cod_aci.strip() != "":
            self.cod_aci = cod_aci.strip().replace("\"", "")

        self.data = {
            'indirizzo': indirizzo.strip().replace("\"", ""),
            'cap': cap.strip().replace("\"", ""),
            'citta': citta.strip().replace("\"", ""),
            'provincia': provincia.strip().replace("\"", ""),
            'cod_aci': self.cod_aci
        }

    def buildSQLInsert(self):
        return "INSERT INTO indirizzo (indirizzo, cap, citta, provincia_sigla, codice_comune_aci) VALUES " \
               "(%(indirizzo)s, %(cap)s, %(citta)s, %(provincia)s, %(cod_aci)s)"

    def insertQuery(self, cur):
        query = self.buildSQLInsert()
        # print(query)
        cur.execute(query, self.data)
        return cur.lastrowid
