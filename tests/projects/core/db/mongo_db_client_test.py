import unittest

from projects.core.db.mongo_db.mongo_db_client import UserTypeEnum, DbClient
from projects.core.etuzon_io.logger import \
    LogLevelEnum, init_logger
from projects.core.test.unittest_base import UnitTestBase


class DbClientTests(UnitTestBase):
    """
    The test contains connection to real DB,
    so it will not be run as part of the regression tests
    """

    MONGO_DB_USER = 'admin'
    MONGO_DB_PASSWORD = 'tech'

    DB_USER = 'user'
    DB_PASSWORD = 'password'

    DB_NEW_USER = 'new_user'
    DB_NEW_PASSWORD = 'password'

    DB_NAME = 'test_db'

    HOSTNAME = '127.0.0.1'
    PORT = 27017

    COLLECTION_NAME = 'test_collection'

    def setUp(self) -> None:
        init_logger(
            LogLevelEnum.DEBUG,
            LogLevelEnum.DEBUG)
        DbClient.enable_mock_db()

    def test_1_create_db_and_collection(self):
        db_client = self._mock_mongo_db_with_admin_user()
        self.assertTrue(
            not db_client.is_db_exist(self.DB_NAME),
            f'DB [{self.DB_NAME}] should not be exist')
        self.assertTrue(db_client.user_type == UserTypeEnum.MONGO_DB_USER)
        db_client.create_db(self.DB_NAME, self.COLLECTION_NAME)
        self.assertTrue(
            db_client.is_db_exist(self.DB_NAME),
            f'DB [{self.DB_NAME}] was not created')
        db = db_client.get_db(self.DB_NAME)
        self.assertTrue(
            self.COLLECTION_NAME in db.list_collection_names(),
            f'Collection [{self.COLLECTION_NAME}] was not created')

    def test_2_admin_db_name_is_admin(self):
        db_client = self._mock_mongo_db_with_admin_user()
        self.assertTrue(db_client.db, 'DB is None')
        self.assertEqual(db_client.db.name, db_client.db_name)
        self.assertEqual(db_client.db.name, "admin")

    def test_3_mock_with_minimum_parameters_and_get_hostname_and_port(self):
        db_client = self._mock_mongo_db_with_minimum_parameters()
        self.assertTrue(db_client.user_type == UserTypeEnum.DB_USER)
        self.assertTrue(
            not db_client.is_db_exist(self.DB_NAME),
            f'DB [{self.DB_NAME}] should not be exist')
        self.assertEqual(db_client.db_hostname, self.HOSTNAME)
        self.assertEqual(db_client.db_port, self.PORT)

    def test_4_get_mongo_db_hostname(self):
        hostname = 'test123'
        port = 1234
        expected_hostname = f'{hostname}:{port}'
        self.assertEqual(
            DbClient.get_mongo_db_hostname(hostname, port),
            expected_hostname)

    def test_5_test_create_db_and_collection_and_delete_db(self):
        db_client = self._mock_mongo_db_with_db_user()
        db_client.create_db(self.DB_NAME, self.COLLECTION_NAME)
        self.assertTrue(db_client.is_db_exist(self.DB_NAME),
                        f'DB [{self.DB_NAME}] was not created')
        self.assertTrue(
            self.COLLECTION_NAME in db_client.get_collection_names(),
            f'Collection [{self.COLLECTION_NAME}] was not created')
        db_client.delete_db(self.DB_NAME)
        self.assertTrue(not db_client.is_db_exist(db_client.db.name))

    def _mock_mongo_db_with_db_user(self) -> DbClient:
        return DbClient(
            self.DB_USER,
            self.DB_PASSWORD,
            UserTypeEnum.DB_USER,
            self.HOSTNAME,
            self.PORT,
            self.DB_NAME,
            False,
            False)

    def _mock_mongo_db_with_minimum_parameters(self) -> DbClient:
        return DbClient(self.DB_USER, self.DB_PASSWORD, UserTypeEnum.DB_USER)

    def _mock_mongo_db_with_admin_user(self) -> DbClient:
        return DbClient(
            self.MONGO_DB_USER,
            self.MONGO_DB_PASSWORD,
            UserTypeEnum.MONGO_DB_USER,
            self.HOSTNAME,
            self.PORT,
            'admin',
            False,
            False)


if __name__ == '__main__':
    unittest.main()
