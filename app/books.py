from flask import Blueprint, request, jsonify

from . import auth
from . import db


bp = Blueprint("books", __name__, url_prefix="/books")


REQUIRED_KEYS = [
    "title", "amazon_url", "author", "genre",
]


def __insert_new_book(**kwargs):
    cur = db.get_cursor()
    cur.execute()


@bp.route("/insert/", methods=["POST"])
@auth.requires_authorization
async def insert_book():
    if not request.is_json:
        return jsonify(message="Invalid JSON body."), 400
    json = request.json
    missing_keys = set(REQUIRED_KEYS) - set(json.keys())
    if missing_keys:
        return jsonify(message=f"Missing required key of book.", missing_keys=list(missing_keys)), 400
    # TODO: Insert record. __insert_new_book().


@bp.route("/<title>/", methods=["GET"])
@auth.requires_authorization
def get_book(title):
    ...


@bp.route("/", methods=["GET"])
@auth.requires_authorization
def get_all_books():
    ...


@bp.route("/update/", methods=["PUT"])
@auth.requires_authorization
def update_book():
    ...


@bp.route("/delete/", methods=["DELETE"])
@auth.requires_authorization
def delete_book():
    ...
