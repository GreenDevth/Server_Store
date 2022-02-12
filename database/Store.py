from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def get_command(package_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT package_data FROM scum_package WHERE package_name = %s'
        cur.execute(sql, (package_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)

def get_prict(package_name):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT package_price FROM scum_package WHERE package_name = %s'
        cur.execute(sql, (package_name,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)