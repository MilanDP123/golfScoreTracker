import psycopg2 as pg


get_strokes_query = '''SELECT course_handicap FROM handicap
                WHERE tee ILIKE %s
                AND %s BETWEEN lower_bound AND upper_bound'''


def execute_select_query(query, arguments):
    conn = None
    cur = None
    result = None

    try:
        conn = pg.connect(
            host='localhost',
            dbname='golfscoretracker',
            user='postgres',
            port=5432)

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

    print(result)
    return result[0]


def get_strokes(tee, handicap):
    return int(execute_select_query(get_strokes_query, (tee, handicap)))
