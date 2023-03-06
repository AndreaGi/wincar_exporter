import pyctree
import mariadb
import time


def exportClienti(treeCur, mariaCur):
    print("Start export clienti.")
    export(treeCur, mariaCur)


def export(treeCur, mariaCur):
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

        self.tableName = "cliente"

        if cliente_flag == 'F':
            self.tableName = "fornitore"
        self.codice = codice.strip()
        self.ragione_sociale = f"{ragione_sociale} {ragione_sociale2}".strip().replace("\"", "")
        self.id_indirizzo = "NULL"
        self.dettagli_indirizzo = Indirizzo(indirizzo, cap, citta, provincia, codice_comune_aci)
        self.sesso = ""
        self.azienda = 0
        if sesso.strip() != '':
            if sesso == 'M' or sesso == 'F':
                self.sesso = sesso.strip()
            else:
                self.azienda = 1
        self.telefono = telefono.strip()
        self.fax = fax.strip()
        self.email = email.strip()
        self.codice_fiscale = codice_fiscale.strip()
        self.partita_iva = partita_iva.strip()
        self.id_banca = "NULL"
        self.dettagli_banca = DettagliBanca(nome_banca, abi, cab, conto)

    def buildSQLQuery(self):
        return f"INSERT INTO {self.tableName} (codice, ragione_sociale, indirizzo, sesso, azienda, telefono," \
               f"fax, email, codice_fiscale, partita_iva, banca) VALUES " \
               f"(\"{self.codice}\", \"{self.ragione_sociale}\", {self.id_indirizzo}, \"{self.sesso}\", {self.azienda}, " \
               f"\"{self.telefono}\", \"{self.fax}\", \"{self.email}\", \"{self.codice_fiscale}\", " \
               f"\"{self.partita_iva}\", {self.id_banca});"

    def insertQuery(self, cur):
        if self.dettagli_indirizzo.indirizzo.strip() != "":
            self.id_indirizzo = self.dettagli_indirizzo.insertQuery(cur)

        if self.dettagli_banca.banca.strip() != "":
            self.id_banca = self.dettagli_banca.insertQuery(cur)

        query = self.buildSQLQuery()
        # print(query)
        cur.execute(query)


class DettagliBanca:
    def __init__(self, banca, abi, cab, conto):
        self.banca = banca.strip().replace("\"", "")
        self.abi = "NULL"
        if abi.strip().replace("\"", "") != "":
            self.abi = abi.strip().replace("\"", "")
        self.cab = "NULL"
        if cab.strip().replace("\"", "") != "":
            self.cab = cab.strip().replace("\"", "")
        self.conto = conto.strip().replace("\"", "")

    def buildSQLInsert(self):
        return f"INSERT INTO dettagli_banca (banca, abi, cab, conto) VALUES " \
               f"(\"{self.banca}\", {self.abi}, {self.cab}, \"{self.conto}\"); "

    def insertQuery(self, cur):
        query = self.buildSQLInsert()
        # print(query)
        cur.execute(query)
        return cur.lastrowid


class Indirizzo:
    def __init__(self, indirizzo, cap, citta, provincia, cod_aci):
        self.indirizzo = indirizzo.strip().replace("\"", "")
        self.cap = cap.strip().replace("\"", "")
        self.citta = citta.strip().replace("\"", "")
        self.provincia = provincia.strip().replace("\"", "")
        self.cod_aci = "NULL"
        if cod_aci.strip() != "":
            self.cod_aci = cod_aci.strip().replace("\"", "")

    def buildSQLInsert(self):
        return f"INSERT INTO indirizzo (indirizzo, cap, citta, provincia_sigla, codice_comune_aci) VALUES " \
               f"(\"{self.indirizzo}\",\"{self.cap}\",\"{self.citta}\",\"{self.provincia}\",{self.cod_aci});"

    def insertQuery(self, cur):
        query = self.buildSQLInsert()
        # print(query)
        cur.execute(query)
        return cur.lastrowid
