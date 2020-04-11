from flask import Blueprint, request, jsonify

import functools
from . import db
from . import auth


bp = Blueprint("books", __name__, url_prefix="/books")


REQUIRED_KEYS = [
    "title", "amazon_url", "author", "genre",
]


def when_book_exists(view):

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not db.get_book(request.json["title"]):
            return jsonify(message=f"Book with title '{request.json['title']}' doesn't exists."), 404
        return view(*args, **kwargs)

    return wrapper


@bp.route("/insert/", methods=["POST"])
@auth.requires_authorization
@auth.check_request(*REQUIRED_KEYS)
def insert_book():
    if db.book_exists(request.json["title"], request.json["author"]):
        return jsonify(message="Book already exists."), 409
    db.insert_book(**request.json)
    return jsonify(message="Success"), 200


@bp.route("/get/", methods=["POST"])
@auth.requires_authorization
@auth.check_request("title")
@when_book_exists
def get_book():
    json = db.get_book(request.json["title"])
    return jsonify(json), 200


@bp.route("/", methods=["GET", "POST"])
@auth.requires_authorization
def get_all_books():
    sql = "SELECT title, author, amazon_url, genre FROM favorite_books;"
    cur = db.get_cursor()
    cur.execute(sql)
    books = [dict(book) for book in cur.fetchall()]
    return jsonify(books), 200


@bp.route("/update/", methods=["PUT"])
@auth.requires_authorization
@auth.check_request("title", "update")
@when_book_exists
def update_book():
    book = db.get_book(request.json["title"])
    if not isinstance(request.json["update"], dict):
        return jsonify(message="The 'update' value should be JSON."), 400
    book.update(request.json["update"])

    sql = "UPDATE favorite_books SET amazon_url = %s, author = %s, genre = %s WHERE title = %s;"
    cur = db.get_cursor()
    cur.execute(sql, (book["amazon_url"], book["author"], book["genre"], request.json["title"]))
    return jsonify(message="Success"), 200


@bp.route("/delete/", methods=["DELETE"])
@auth.requires_authorization
@auth.check_request("title")
@when_book_exists
def delete_book():
    sql = "DELETE FROM favorite_books WHERE title = %s;"
    cur = db.get_cursor()
    cur.execute(sql, (request.json["title"], ))
    return jsonify(message="Success"), 200
