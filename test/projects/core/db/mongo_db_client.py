import unittest

from projects.core.db.mongodb.mongo_db_client import DbClient, UserTypeEnum
from projects.core.io.logger import LogLevelEnum, LoggerFormatterEnum, init_logger


class DbClientTests(unittest.TestCase):
    MONGO_DB_USER = "admin"
    MONGO_DB_PASSWORD = "tech"

    DB_USER = "user"
    DB_PASSWORD = "password"

    DB_NEW_USER = "new_user"
    DB_NEW_PASSWORD = "password"

    DB_NAME = "test_db"

    HOSTNAME = "127.0.0.1"
    PORT = 27017

    COLLECTION_NAME = "test_collection"

    def setUp(self) -> None:
        init_logger(LogLevelEnum.DEBUG, LogLevelEnum.DEBUG, LoggerFormatterEnum.DETAILED)
        DbClient.enable_mock_db()

    def test_create_db_and_collection(self):
        db_client = self._mock_mongo_db_with_admin_user()
        self.assertTrue(not db_client.is_db_exist(self.DB_NAME),
                        "DB [" + self.DB_NAME + "] should not be exist")
        db_client.create_db(self.DB_NAME, self.COLLECTION_NAME)
        self.assertTrue(db_client.is_db_exist(self.DB_NAME),
                        "DB [" + self.DB_NAME + "] was not created")
        db = db_client.get_db(self.DB_NAME)
        self.assertTrue(self.COLLECTION_NAME in db.list_collection_names(),
                        "Collection [" + self.COLLECTION_NAME + "] was not created")

    def test_admin_db_name_is_admin(self):
        db_client = self._mock_mongo_db_with_admin_user()
        self.assertTrue(db_client.db, "DB is None")
        self.assertTrue(db_client.db.name == db_client.db_name, "DB name [" + db_client.db.name
                        + "] not equal to db_name [" + db_client.db_name + "]")
        self.assertTrue(db_client.db.name == "admin", "DB name [" + db_client.db.name
                        + "] is not admin")

    def _mock_mongo_db_with_db_user(self) -> DbClient:
        return DbClient(self.DB_USER, self.DB_PASSWORD,
                        UserTypeEnum.DB_USER, self.HOSTNAME, self.PORT,
                        self.DB_NAME, False, False)

    def _mock_mongo_db_with_admin_user(self) -> DbClient:
        return DbClient(self.MONGO_DB_USER, self.MONGO_DB_PASSWORD,
                        UserTypeEnum.MONGO_DB_USER, self.HOSTNAME, self.PORT,
                        "admin", False, False)


if __name__ == '__main__':
    unittest.main()
