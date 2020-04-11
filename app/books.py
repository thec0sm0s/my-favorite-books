from flask import Blueprint, request, jsonify

from . import auth
from . import db


bp = Blueprint("books", __name__, url_prefix="/books")


REQUIRED_KEYS = [
    "title", "amazon_url", "author", "genre",
]


@bp.route("/insert/", methods=["POST"])
@auth.requires_authorization
def insert_book():
    if not request.is_json:
        return jsonify(message="Invalid JSON body."), 400
    json = request.json
    missing_keys = set(REQUIRED_KEYS) - set(json.keys())
    if missing_keys:
        return jsonify(message="Missing required keys for book entry.", missing_keys=list(missing_keys)), 400
    db.insert_book(**json)
    return jsonify(message="Success"), 200


@bp.route("/get/", methods=["POST"])
@auth.requires_authorization
def get_book():
    return "Get Book"


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
