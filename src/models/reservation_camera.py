from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .bases.multiple_option import MultipleOption
from .mixins.timestamp import Timestamp


class ReservationCamera(MultipleOption[bool], Timestamp):

    __tablename__ = "reservation_cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    camera = Column(Boolean, nullable=False)

    options = {True: "有", False: "無"}

    @classmethod
    def get_all(cls, id: str) -> list[bool]:
        return cls.get_all_by_column(id=id, column="camera")

    @classmethod
    def add_all(cls, id: str, options: list[bool], commit: bool = True) -> None:
        cls.add_all_by_column(id=id, column="camera", options=options, commit=commit)

    @classmethod
    def delete_all(cls, id: str, options: list[bool], commit: bool = True) -> None:
        cls.delete_all_by_column(id=id, column="camera", options=options, commit=commit)
