from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def battlemetric(id_token):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT token FROM scum_discord_token WHERE token_id = %s'
        cur.execute(sql, id_token)
        row = cur.fetchall()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)
