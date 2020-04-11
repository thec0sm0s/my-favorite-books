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
    sql = "CREATE TABLE IF NOT EXISTS favorite_books " \
          "(ID SERIAL PRIMARY KEY, Title varchar, amazon_url varchar, author varchar, genre varchar);"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()


def close_db_cursor(_=None):
    db = g.pop("db", None)
    if db:
        db.commit()
        db.close()


def insert_book(**kwargs):
    sql = "INSERT INTO favorite_books (title, amazon_url, author, genre) values (%s, %s, %s, %s)"

    cur = get_cursor()
    cur.execute(sql, (kwargs["title"], kwargs["amazon_url"], kwargs["author"], kwargs["genre"]))
