import datetime as dt

from sqlalchemy import Column, ForeignKey, Integer, String, Time

from .bases.multiple_option import MultipleOption
from .mixins.timestamp import Timestamp


class NotificationTime(MultipleOption[dt.time], Timestamp):

    __tablename__ = "notification_times"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    time = Column(Time, nullable=False)

    options = {dt.time(i): dt.time(i).isoformat(timespec="minutes") for i in range(24)}

    @classmethod
    def get_all(cls, id: str) -> list[dt.time]:
        return cls.get_all_by_column(id=id, column="time")

    @classmethod
    def add_all(cls, id: str, options: list[dt.time], commit: bool = True) -> None:
        cls.add_all_by_column(id=id, column="time", options=options, commit=commit)

    @classmethod
    def delete_all(cls, id: str, options: list[dt.time], commit: bool = True) -> None:
        cls.delete_all_by_column(id=id, column="time", options=options, commit=commit)
