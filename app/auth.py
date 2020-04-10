from flask import Blueprint, jsonify, redirect, url_for, request, current_app

import jwt
import datetime
import functools


bp = Blueprint("auth", __name__,)


@bp.route("/auth/", methods=["GET", "POST"])
def authorize():
    expires_at = datetime.datetime.now() + datetime.timedelta(hours=current_app.config["JWT_TOKEN_EXPIRES_IN"])
    token = jwt.encode({
        "exp": expires_at,
    }, key=current_app.config["JWT_SECRET_KEY"])
    return jsonify(token=token)


def requires_authorization(view):

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify(message="Unauthorized"), 401
        try:
            jwt.decode(token, key=current_app.config["JWT_SECRET_KEY"])
        except jwt.exceptions.InvalidSignatureError:
            return jsonify(message="Invalid JWT Authorization Token"), 401
        except jwt.exceptions.ExpiredSignatureError:
            return redirect(url_for("authorize"))

        return view(*args, **kwargs)

    return wrapper
