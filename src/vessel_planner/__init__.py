import os
import sys
from flask import Flask



def create_app(test_config=None):
    print("Creating Flask app...")
    print("Current Working Directory:", os.getcwd())
    print("Python Path:", sys.path)
    app = Flask(__name__, instance_relative_config=True)
    
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
