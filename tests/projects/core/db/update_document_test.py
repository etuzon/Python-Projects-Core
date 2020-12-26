import unittest
from enum import Enum

from projects.core.db.mongo_db.update_document import \
    MongoDbUpdateDocumentBase


class MongoDbUpdateDocumentBaseTests(unittest.TestCase):
    class TestEnum(Enum):
        ONE = 1
        TWO = 2

    class TestClass(MongoDbUpdateDocumentBase):
        def __init__(self):
            super()._init_update_dict()

        def get_dict(self) -> dict:
            return self._update_dict

        def add_value(self, key: str, value):
            self._add_value(key, value)

    def test_1_init_update_dict(self):
        update_doc = MongoDbUpdateDocumentBaseTests.TestClass()
        self.assertIsNotNone(update_doc.get_dict())
        self.assertFalse(update_doc.get_dict())

    def test_2_add_key(self):
        key = 'key1'
        value = 'value1'

        update_doc = MongoDbUpdateDocumentBaseTests.TestClass()
        update_doc.add_value(key, value)
        self.assertTrue(update_doc.get_dict()[key] == value)

    def test_3_add_key_with_enum_value(self):
        key = 'key1'
        value = MongoDbUpdateDocumentBaseTests.TestEnum.TWO

        update_doc = MongoDbUpdateDocumentBaseTests.TestClass()
        update_doc.add_value(key, value)
        self.assertTrue(update_doc.get_dict()[key] == value.value)

    def test_4_add_key_with_none_value(self):
        key = 'key1'
        value = None

        update_doc = MongoDbUpdateDocumentBaseTests.TestClass()
        update_doc.add_value(key, value)
        self.assertTrue(key not in update_doc.get_dict())


if __name__ == '__main__':
    unittest.main()
