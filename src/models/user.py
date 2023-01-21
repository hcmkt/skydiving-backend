from sqlalchemy import Boolean, Column, Integer, String

from ..instances.database import db
from .mixins.timestamp import Timestamp


class User(db.Model, Timestamp):  # type: ignore

    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    reservation_vacancy = Column(Integer, default=1, nullable=False)
    notification = Column(Boolean, default=True, nullable=False)
    reservation_days = db.relationship("ReservationDay", backref="user")
    reservation_times = db.relationship("ReservationTime", backref="user")
    reservation_cameras = db.relationship("ReservationCamera", backref="user")
    notification_times = db.relationship("NotificationTime", backref="user")

    notifications = {True: "ON", False: "OFF"}

    @classmethod
    def get(cls, id: str) -> "User":
        return db.session.execute(db.select(cls).filter_by(id=id)).scalars().first()

    @classmethod
    def add(cls, id: str, commit: bool = True) -> None:
        db.session.add(cls(id=id))
        if commit:
            db.session.commit()

    @classmethod
    def update(
        cls, id: str, reservation_vacancy: int, notification: bool, commit: bool = True
    ) -> None:
        user = db.session.execute(db.select(cls).filter_by(id=id)).scalars().first()
        user.reservation_vacancy = reservation_vacancy
        user.notification = notification
        if commit:
            db.session.commit()

    @classmethod
    def format_notification(cls, notification: bool) -> str:
        return cls.notifications[notification]

    @classmethod
    def rformat_notification(cls, notification_str: str) -> bool:
        rnotifications = {v: k for k, v in cls.notifications.items()}
        return rnotifications[notification_str]
