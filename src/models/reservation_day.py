from sqlalchemy import Column, ForeignKey, Integer, String

from .bases.multiple_option import MultipleOption
from .mixins.timestamp import Timestamp


class ReservationDay(MultipleOption[int], Timestamp):

    __tablename__ = "reservation_days"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    day = Column(Integer, nullable=False)

    options = {1: "月", 2: "火", 3: "水", 4: "木", 5: "金", 6: "土", 7: "日"}

    @classmethod
    def get_all(cls, id: str) -> list[int]:
        return cls.get_all_by_column(id=id, column="day")

    @classmethod
    def add_all(cls, id: str, options: list[int], commit: bool = True) -> None:
        cls.add_all_by_column(id=id, column="day", options=options, commit=commit)

    @classmethod
    def delete_all(cls, id: str, options: list[int], commit: bool = True) -> None:
        cls.delete_all_by_column(id=id, column="day", options=options, commit=commit)
