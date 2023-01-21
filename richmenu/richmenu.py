import os

from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import (
    MessageAction,
    RichMenu,
    RichMenuArea,
    RichMenuBounds,
    RichMenuSize,
    URIAction,
)

load_dotenv()

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))

rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

rich_menu_id = line_bot_api.create_rich_menu(
    RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=True,
        name="richmenu",
        chat_bar_text="メニュー",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=625, height=843),
                action=MessageAction(label="全件取得", text="全件取得"),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=626, y=0, width=625, height=843),
                action=MessageAction(label="カスタム取得", text="カスタム取得"),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1251, y=0, width=625, height=843),
                action=URIAction(label="設定", uri=os.getenv("LIFF_URL")),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1876, y=0, width=625, height=843),
                action=URIAction(
                    label="公式サイト",
                    uri="https://tokyoskydivingclub.jp/体験スカイダイビングご予約new/",
                ),
            ),
        ],
    )
)

with open(os.path.dirname(__file__) + "/richmenu.png", "rb") as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

line_bot_api.set_default_rich_menu(rich_menu_id)
