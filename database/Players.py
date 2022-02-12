from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def players_exists(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT COUNT(*) FROM scum_players WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
    except Error as e:
        print(e)


def players(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'SELECT * FROM scum_players WHERE DISCORD_ID=%s'
        cur.execute(sql, (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)


def players_update_coin(discord_id, coin):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s'
        cur.execute(sql, (coin, discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)


def players_newbie_update(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        sql = 'UPDATE scum_players SET NEWBIE = 1 WHERE DISCORD_ID = %s'
        cur.execute(sql, (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
