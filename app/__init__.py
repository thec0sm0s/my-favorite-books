from flask import Flask

from . import db
from . import auth
from . import books


BLUEPRINTS = [
    auth.bp, books.bp
]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("configs")
    db.make_migrations()
    app.teardown_appcontext(db.close_db_cursor)

    for bp in BLUEPRINTS:
        app.register_blueprint(bp)

    return app
