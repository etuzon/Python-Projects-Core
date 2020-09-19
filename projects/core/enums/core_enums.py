from enum import Enum


class CoreEnum(Enum):
    """
    Enum that will return None in case value not part of Enum
    instead of raise ValueError exception.
    """

    def __new__(cls, value):
        try:
            return Enum(value=value)
        except ValueError:
            return None
