import datetime
import zoneinfo
from math import floor

from linebot.models import TextSendMessage

from ..instances.database import db
from ..instances.line import line_bot_api
from ..instances.scheduler import scheduler
from ..models.notification_time import NotificationTime
from ..models.user import User
from ..utils.database import Database
from ..utils.helper import is_local
from ..utils.reservation import Reservation


@scheduler.task("cron", id="do_job_1", minute="0")
def notify():
    with scheduler.app.app_context():
        now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo"))
        time = datetime.time(floor(now.hour + (now.minute + 30) / 60))
        users = (
            db.session.execute(
                db.select(User)
                .join(User.notification_times)
                .filter(
                    User.notification == True,  # noqa: E712
                    NotificationTime.time == time,
                )
            )
            .scalars()
            .all()
        )
        reservation = Reservation()
        for user in users:
            settings = Database(user.id).get_settings()
            msg = reservation.filter(
                days=settings["reservation_days"],
                times=settings["reservation_times"],
                cameras=settings["reservation_cameras"],
                vacancy=settings["reservation_vacancy"],
            ).format()
            if is_local():
                print(msg)
            else:
                line_bot_api.push_message(user.id, TextSendMessage(text=msg))
