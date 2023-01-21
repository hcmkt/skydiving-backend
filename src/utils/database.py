from datetime import time
from typing import TypedDict

from ..instances.database import db
from ..models.notification_time import NotificationTime
from ..models.reservation_camera import ReservationCamera
from ..models.reservation_day import ReservationDay
from ..models.reservation_time import ReservationTime
from ..models.user import User


class TypeSnakeSettings(TypedDict):
    reservation_days: list[int]
    reservation_times: list[time]
    reservation_cameras: list[bool]
    reservation_vacancy: int
    notification: bool
    notification_times: list[time]


class TypeCamelSettingsValue(TypedDict):
    reservationDays: list[str]
    reservationTimes: list[str]
    reservationCameras: list[str]
    reservationVacancy: int
    notification: str
    notificationTimes: list[str]


class Database:
    def __init__(self, id: str) -> None:
        self.id = id

    def user_exists(self) -> bool:
        return db.session.execute(db.select(User).filter_by(id=self.id)).scalar()

    def add_user(self) -> None:
        User.add(self.id, False)
        ReservationDay.add_all(self.id, ReservationDay.get_option_keys(), False)
        ReservationTime.add_all(self.id, ReservationTime.get_option_keys(), False)
        ReservationCamera.add_all(self.id, ReservationCamera.get_option_keys(), False)
        NotificationTime.add_all(self.id, NotificationTime.get_option_keys(), False)
        db.session.commit()

    def get_settings(self) -> TypeSnakeSettings:
        user = User.get(self.id)
        return {
            "reservation_days": ReservationDay.get_all(self.id),
            "reservation_times": ReservationTime.get_all(self.id),
            "reservation_cameras": ReservationCamera.get_all(self.id),
            "reservation_vacancy": user.reservation_vacancy,
            "notification": user.notification,
            "notification_times": NotificationTime.get_all(self.id),
        }

    def update_settings(self, settings: TypeSnakeSettings) -> None:
        User.update(
            self.id, settings["reservation_vacancy"], settings["notification"], False
        )
        ReservationDay.delsert(self.id, settings["reservation_days"], False)
        ReservationTime.delsert(self.id, settings["reservation_times"], False)
        ReservationCamera.delsert(self.id, settings["reservation_cameras"], False)
        NotificationTime.delsert(self.id, settings["notification_times"], False)

    def settings_format(self) -> TypeCamelSettingsValue:
        user = User.get(self.id)
        return {
            "reservationDays": ReservationDay.format(self.id),
            "reservationTimes": ReservationTime.format(self.id),
            "reservationCameras": ReservationCamera.format(self.id),
            "reservationVacancy": user.reservation_vacancy,
            "notification": User.format_notification(user.notification),
            "notificationTimes": NotificationTime.format(self.id),
        }

    @staticmethod
    def rformat_settings(settings: TypeCamelSettingsValue) -> TypeSnakeSettings:
        return {
            "reservation_days": ReservationDay.rformat(settings["reservationDays"]),
            "reservation_times": ReservationTime.rformat(settings["reservationTimes"]),
            "reservation_cameras": ReservationCamera.rformat(
                settings["reservationCameras"]
            ),
            "reservation_vacancy": settings["reservationVacancy"],
            "notification": User.rformat_notification(settings["notification"]),
            "notification_times": NotificationTime.rformat(
                settings["notificationTimes"]
            ),
        }
