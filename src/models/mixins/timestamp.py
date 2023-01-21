from datetime import datetime as dt

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


class Timestamp:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=dt.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=dt.now(), onupdate=dt.now(), nullable=False)
