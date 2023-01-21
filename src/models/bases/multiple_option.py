from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from flask_sqlalchemy import DefaultMeta

from ...instances.database import db
from ...utils.helper import difference

T = TypeVar("T")


class DefaultABCMeta(DefaultMeta, ABCMeta):
    pass


class MultipleOption(db.Model, Generic[T], metaclass=DefaultABCMeta):  # type: ignore

    __abstract__ = True

    options: dict[T, str]

    @classmethod
    @abstractmethod
    def get_all(cls, id: str) -> list[T]:
        pass

    @classmethod
    @abstractmethod
    def add_all(cls, id: str, options: list[T], commit: bool = True) -> None:
        pass

    @classmethod
    @abstractmethod
    def delete_all(cls, id: str, options: list[T], commit: bool = True) -> None:
        pass

    @classmethod
    def get_all_by_column(cls, id: str, column: str) -> list[T]:
        return (
            db.session.execute(db.select(getattr(cls, column)).filter_by(user_id=id))
            .scalars()
            .all()
        )

    @classmethod
    def add_all_by_column(
        cls, id: str, column: str, options: list, commit: bool = True
    ) -> None:
        db.session.add_all([cls(**{"user_id": id, column: opt}) for opt in options])
        if commit:
            db.session.commit()

    @classmethod
    def delete_all_by_column(
        cls, id: str, column: str, options: list[T], commit: bool = True
    ) -> None:
        db.session.execute(db.delete(cls).where(getattr(cls, column).in_(options)))
        if commit:
            db.session.commit()

    @classmethod
    def delsert(cls, id: str, options: list[T], commit: bool = True) -> None:
        old_options = cls.get_all(id=id)
        cls.delete_all(id=id, options=difference(old_options, options))
        cls.add_all(id=id, options=difference(options, old_options))
        if commit:
            db.session.commit()

    @classmethod
    def get_option_keys(cls) -> list[T]:
        return list(cls.options.keys())

    @classmethod
    def get_option_values(cls) -> list[str]:
        return list(cls.options.values())

    @classmethod
    def format(cls, id: str) -> list[str]:
        options = cls.get_all(id=id)
        return [cls.options[option] for option in options]

    @classmethod
    def rformat(cls, options_str: list[str]) -> list[T]:
        roptions = {v: k for k, v in cls.options.items()}
        return [roptions[option_str] for option_str in options_str]
