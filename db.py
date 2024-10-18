import psycopg2 as pg
from dotenv import load_dotenv
import os

load_dotenv()

hostname = 'pg-golfscoretracker-milandepaepe-e238.d.aivencloud.com'
databasename = 'defaultdb'
dbuser = 'avnadmin'
dbport = 15977
passw = os.getenv('PASSW')

get_strokes_query = '''SELECT course_handicap FROM handicap
                WHERE tee ILIKE %s
                AND %s BETWEEN lower_bound AND upper_bound'''


get_usernames_query = ''' SELECT user_name FROM users'''

get_userid_query = ''' SELECT user_id FROM users WHERE user_name LIKE %s'''

get_password_query = ''' SELECT password FROM users WHERE user_name LIKE %s'''


new_user_query = ''' INSERT INTO users (user_name, password) VALUES (%s, %s)'''


def execute_select_query(query, arguments):
    conn = None
    cur = None
    result = None

    try:
        conn = pg.connect(
            host=hostname,
            dbname=databasename,
            user=dbuser,
            port=dbport,
            password=passw)

        cur = conn.cursor()

        cur.execute(query, arguments)
        result = cur.fetchone()

        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

    return result


def execute_insert_query(query, arguments):
    conn = None
    cur = None

    try:
        conn = pg.connect(
            host=hostname,
            dbname=databasename,
            user=dbuser,
            port=dbport,
            password=passw)

        cur = conn.cursor()

        cur.execute(query, arguments)

        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()


def get_strokes(tee, handicap):
    return int(execute_select_query(get_strokes_query, (tee, handicap))[0])


def get_usernames():
    return execute_select_query(get_usernames_query, '')


def get_userid(username):
    return execute_select_query(get_userid_query, (username,))[0]


def check_password(username, password):
    return execute_select_query(get_password_query, (username,))[0] == password


def new_user(username, password):
    execute_insert_query(new_user_query, (username, password))
