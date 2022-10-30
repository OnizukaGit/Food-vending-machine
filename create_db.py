from psycopg2 import connect, ProgrammingError

def CREATE_DB(cursor):
    create_db = """create database Snack_Machine"""
    cursor.execute(create_db)


def execute_sql():
    cnx = connect(host="localhost", user="postgres",password="coderslab")
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        CREATE_DB(cursor)
        print("Now u create database :)")
    except ProgrammingError:
        print("Oh sorry i cant :( ")
    cnx.close()
    cursor.close()

execute_sql()
