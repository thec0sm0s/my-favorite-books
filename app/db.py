from flask import g

import configs
import psycopg2


def get_db():
    return psycopg2.connect(dbname=configs.DATABASE, user=configs.DB_USER, password=configs.DB_PASSWORD)


def get_cursor():
    db = g.get("db")
    if db:
        return db.cursor()
    g.db = get_db()
    return g.db.cursor()


def make_migrations():
    sql = f"CREATE TABLE IF NOT EXISTS {configs.DB_TABLE}" \
          f"(ID serial PRIMARY KEY, Title varchar, amazon_url varchar, author varchar, genre varchar);"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()


def close_db_cursor():
    db_conn = g.pop("db_conn", None)
    if db_conn:
        db_conn.commit()
        db_conn.close()
