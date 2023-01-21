from datetime import datetime, time, timedelta
from typing import TypedDict

import ratelimit
import requests

from ..models.reservation_camera import ReservationCamera
from ..models.reservation_day import ReservationDay
from ..models.reservation_time import ReservationTime


class TypeReservation(TypedDict):
    datetime: datetime
    camera: bool
    vacancy: int


class Reservation:
    def __init__(
        self,
        reservations: list[TypeReservation] = [],
        start_date: datetime = datetime.now(),
        days: int = 150,
    ) -> None:
        if reservations:
            self.reservations = reservations
        else:
            raw_reservations = Reservation.__fetch(start_date, days)
            self.reservations = Reservation.__extract(raw_reservations)

    def filter(
        self,
        days: list[int] = ReservationDay.get_option_keys(),
        times: list[time] = ReservationTime.get_option_keys(),
        cameras: list[bool] = ReservationCamera.get_option_keys(),
        vacancy: int = 1,
    ) -> "Reservation":
        return Reservation(
            list(
                filter(
                    lambda reservation: reservation["vacancy"] >= vacancy
                    and reservation["datetime"].isoweekday() in days
                    and reservation["datetime"].time() in times
                    and reservation["camera"] in cameras,
                    self.reservations,
                )
            )
        )

    def format(self, limitation: int | None = None) -> str:
        msg = "\n".join(
            [
                "{} {} {}".format(
                    reservation["datetime"].strftime("%Y/%m/%d(%a) %H:%M"),
                    reservation["vacancy"],
                    ReservationCamera.options[reservation["camera"]],
                )
                for reservation in self.reservations
            ]
        )[:limitation]
        return msg[: None if limitation is None else msg.rfind("\n")]

    @staticmethod
    @ratelimit.sleep_and_retry
    @ratelimit.limits(calls=1, period=1)
    def __fetch_once(start_date: datetime, end_date: datetime) -> list[dict]:
        url = "https://coubic.com/api/v2/merchants/tokyoskydivingclub/booking_events"
        params = {
            "renderer": "widgetCalendar",
            "start": start_date.isoformat(timespec="seconds"),
            "end": end_date.isoformat(timespec="seconds"),
        }
        raw_reservations = requests.get(url, params=params).json()
        return raw_reservations

    @staticmethod
    def __fetch(start_date: datetime, days: int) -> list[dict]:
        MAX_DAYS = 50
        raw_reservations = []
        for _ in range(days // MAX_DAYS):
            end_date = Reservation.__get_datetime_after_days(start_date, MAX_DAYS)
            raw_reservations += Reservation.__fetch_once(start_date, end_date)
            start_date += timedelta(days=MAX_DAYS)
        if reminder_days := days % MAX_DAYS:
            end_date = Reservation.__get_datetime_after_days(start_date, reminder_days)
            raw_reservations += Reservation.__fetch_once(start_date, end_date)
        return raw_reservations

    @staticmethod
    def __get_datetime_after_days(dt: datetime, days: int) -> datetime:
        return dt + timedelta(days=days) - timedelta(seconds=1)

    @staticmethod
    def __extract(raw_reservations: list[dict]) -> list[TypeReservation]:
        return [
            {
                "datetime": datetime.strptime(r["start"], "%Y-%m-%d %H:%M"),
                "camera": r["title"] == "カメラマン付",
                "vacancy": r["vacancy"],
            }
            for r in raw_reservations
        ]
