import os

from linebot.models import MessageEvent, TextMessage, TextSendMessage

from ..instances.line import handler, line_bot_api
from ..utils.database import Database
from ..utils.reservation import Reservation


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) -> None:
    MAX_MESSAGE_LENGTH = 5000
    text = event.message.text
    if text == "全件取得":
        res = Reservation().filter().format(MAX_MESSAGE_LENGTH)
    elif text == "カスタム取得":
        setting = Database(event.source.user_id).get_settings()
        if not setting:
            return
        res = (
            Reservation()
            .filter(
                days=setting["reservation_days"],
                times=setting["reservation_times"],
                cameras=setting["reservation_cameras"],
                vacancy=setting["reservation_vacancy"],
            )
            .format()
        )
    elif text == "公式":
        res = "https://tokyoskydivingclub.jp"
    elif text == "設定":
        res = os.getenv("LIFF_URL", "")
    else:
        return
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=res))
