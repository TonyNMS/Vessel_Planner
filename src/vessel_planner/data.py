from flask import current_app
import pandas as pd


def load_prop(prop):
    app = current_app()
    with app.open_instance_resource(f"{prop}.json") as prop_json:
        return pd.read_json(prop_json)

    return None


def save_prop(prop, frame):
    app = current_app()
    with app.open_instance_resource(f"{prop}.json", "w") as prop_json:
        frame.to_json(prop_json)
