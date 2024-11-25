from flask import Blueprint, request
import json
import pandas as pd
from flask_cors import cross_origin
from .db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/get_prop", methods=["POST"])
@cross_origin()
def get_prop():
    prop = request.json["prop"]

    db = get_db()
    df = pd.read_sql(f"select * from {prop}", db)

    return df.to_json()


@bp.route("/save_prop", methods=["POST"])
@cross_origin()
def save_prop():
    prop = request.json["prop"]
    
    df = pd.read_json(json.dumps(request.json["frame"]), orient="split")

    db = get_db()
    rows = df.to_sql(prop, db,if_exists="replace")

    return json.dumps("Pass") if rows else json.dumps(
        "Failed to write frame to database.")

@bp.route("/check_or_create_task_table", methods=["POST"])
@cross_origin()
def check_or_create_task_table():
    db = get_db()
    try:
       
        result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Task';").fetchone()
        if result is None:
           
            db.execute("""
                CREATE TABLE Task (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    "index" TEXT NOT NULL,
                    columns TEXT NOT NULL,
                    data TEXT NOT NULL
                );
            """)
            db.commit()
            return {"message": "Table `Task` created successfully"}, 201
        else:
            return {"message": "Table `Task` already exists"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

