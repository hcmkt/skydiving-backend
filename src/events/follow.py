from linebot.models import FollowEvent, TextSendMessage

from ..instances.line import handler, line_bot_api
from ..utils.database import Database


@handler.add(FollowEvent)
def handle_follow(event):
    database = Database(event.source.user_id)
    if not database.user_exists():
        database.add_user()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="こんにちは"))
