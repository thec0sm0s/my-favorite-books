from flask import Blueprint, request, jsonify

from . import auth
from . import db


bp = Blueprint("books", __name__, url_prefix="/books")


REQUIRED_KEYS = [
    "title", "amazon_url", "author", "genre",
]


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
def get_book():
    json = db.get_book(request.json["title"])
    if not json:
        return jsonify(message=f"Book with title '{request.json['title']}' doesn't exists."), 404
    return jsonify(json), 200


@bp.route("/", methods=["GET"])
@auth.requires_authorization
def get_all_books():
    return "Get all books"


@bp.route("/update/", methods=["PUT"])
@auth.requires_authorization
def update_book():
    return "Update book"


@bp.route("/delete/", methods=["DELETE"])
@auth.requires_authorization
def delete_book():
    return "delete book"
