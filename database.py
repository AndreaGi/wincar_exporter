import sys
import mariadb

def get_mysql_connection():
    try:
        mariadb_conn = mariadb.connect(
                    user="root",
                    password="6qzlkE3B6hm&",
                    host="167.235.53.57",
                    port=3306,
                    database="19_10"
        )
        return mariadb_conn;
    except Exception as e:
        print("error", e)
        sys.exit(1)
