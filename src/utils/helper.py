import os


def difference(l1: list, l2: list) -> list:
    return list(set(l1) - set(l2))


def is_local() -> bool:
    return os.getenv("CHANNEL_SECRET", "") == ""
