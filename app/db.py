from flask import g

import configs
import psycopg2

from psycopg2 import extras


def get_db():
    return psycopg2.connect(dbname=configs.DATABASE, user=configs.DB_USER, password=configs.DB_PASSWORD)


def get_cursor(factory=extras.RealDictCursor):
    db = g.get("db")
    if db:
        return db.cursor(cursor_factory=factory)
    g.db = get_db()
    return g.db.cursor(cursor_factory=factory)


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


def get_book(title):
    sql = "SELECT * FROM favorite_books WHERE title LIKE %s;"
    cur = get_cursor()
    cur.execute(sql, (title, ))
    try:
        json = dict(cur.fetchone())
    except TypeError:
        return dict()
    json.pop("id")
    return json


def book_exists(title, author):
    sql = "SELECT * FROM favorite_books WHERE title = %s AND author = %s;"
    cur = get_cursor()
    cur.execute(sql, (title, author))
    return bool(cur.fetchone())
