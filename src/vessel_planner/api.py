from flask import Blueprint, request
import json
import pandas as pd
from flask_cors import cross_origin
from vessel_planner.db import get_db

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
