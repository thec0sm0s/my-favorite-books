from flask import Blueprint, jsonify, redirect, url_for, request, current_app

import jwt
import datetime
import functools


bp = Blueprint("auth", __name__,)


@bp.route("/auth/", methods=["GET", "POST"])
def authorize():
    expires_at = datetime.datetime.now() + datetime.timedelta(seconds=current_app.config["JWT_TOKEN_EXPIRES_IN"])
    # TODO: Make sure expiration works.
    token = jwt.encode({
        "exp": expires_at,
    }, key=current_app.config["JWT_SECRET_KEY"])
    token = token.decode("utf-8")
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
        except jwt.DecodeError:
            return jsonify(message="Can't decode JWT Authorization Token"), 401

        return view(*args, **kwargs)

    return wrapper


def check_request(*required_keys):

    def decorator(view):

        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify(message="Invalid JSON body."), 400
            missing_keys = set(required_keys) - set(request.json.keys())
            if missing_keys:
                return jsonify(message="Missing required keys for book entry.", missing_keys=list(missing_keys)), 400
            return view(*args, **kwargs)

        return wrapper

    return decorator
