from flask import Blueprint, abort, current_app, request
from linebot.exceptions import InvalidSignatureError

from ..instances.line import handler

callback = Blueprint("callback", __name__)


@callback.route("/callback", methods=["POST"])
def cb():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature.")
        abort(400)
    return "OK"
