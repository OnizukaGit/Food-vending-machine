from psycopg2 import connect, ProgrammingError

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"


def execute_sql(db, sql_code, params=None):
    with connect(host=HOST, user=USER, password=PASSWORD, dbname=db) as cnx:
        cnx.autocommit = True
        with cnx.cursor() as cursor:
            cursor.execute(sql_code, params)
            try:
                return list(cursor)
            except ProgrammingError:
                return []