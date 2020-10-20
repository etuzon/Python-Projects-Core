import enum


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
            else:
                self._update_dict[key] = value

    def _init_update_dict(self):
        self._update_dict = {}
