from flask import Blueprint, jsonify, request

from ..utils.database import Database
from ..utils.helper import is_local
from ..utils.line import Line

settings = Blueprint("settings", __name__)


@settings.route("/settings", methods=["GET"])
def get():
    if is_local():
        id = "xxxx"
    else:
        line = Line(request.args.get("token"))
        if not line.validate_token():
            return None
        id = line.get_user_id()
    database = Database(id)
    if not database.user_exists():
        database.add_user()
    return jsonify(database.settings_format())


@settings.route("/settings", methods=["PUT"])
def update():
    json = request.get_json()
    if is_local():
        id = "xxxx"
    else:
        id = Line(json["token"]).get_user_id()
    database = Database(id)
    database.update_settings(
        database.rformat_settings(json if is_local() else json["settings"])
    )
    return "", 200
