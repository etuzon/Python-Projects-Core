import enum

from projects.core.objects.numbers import DecimalNumber


class MongoDbUpdateDocumentBase:
    """
    Base class for classes that create update dictionary
    for MongoDB update method
    """
    _update_dict: dict

    def _add_value(self, key: str, value):
        if value is not None:
            if isinstance(value, enum.Enum):
                self._update_dict[key] = value.value
            elif isinstance(value, DecimalNumber):
                self._update_dict[key] = float(value)
            else:
                self._update_dict[key] = value

    def _init_update_dict(self):
        self._update_dict = {}
