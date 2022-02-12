import os
from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def get_token(token_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT token FROM scum_discord_token WHERE token_id = %s'
        cur.execute(sql, (token_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def config_cogs(client):
    for filename in os.listdir('./extension'):
        if filename.endswith('.py'):
            client.load_extension(f'extension.{filename[:-3]}')
