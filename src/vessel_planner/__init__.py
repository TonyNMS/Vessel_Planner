import os

from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    print("Creating Flask app...")

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)


    from . import api
    app.register_blueprint(api.bp)

    return app
