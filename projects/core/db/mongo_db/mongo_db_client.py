"""
@author: Eyal Tuzon
"""

from enum import Enum

import mongomock
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from projects.core.exceptions.core_exceptions import ApplicationException
from projects.core.exceptions.db_exceptions import \
    DbConnectionException, DbException
from projects.core.etuzon_io.logger import logger


class UserTypeEnum(Enum):
    MONGO_DB_USER = 1
    DB_USER = 2


class DbClientBase:
    MAX_COLLECTION_NAME = 64

    LOCAL_HOST = '127.0.0.1'
    DEFAULT_PORT = 27017

    _mongo_db_client: MongoClient = None

    _db_hostname: str
    _db_port: int
    _is_test: bool
    _user_type: UserTypeEnum
    _db_name: str

    def __init__(
            self,
            db_hostname: str = None,
            db_port: int = None,
            user_type: UserTypeEnum = UserTypeEnum.DB_USER,
            db_name: str = None):
        if db_hostname:
            self._db_hostname = db_hostname
        else:
            self._db_hostname = self.LOCAL_HOST

        if db_port:
            self._db_port = db_port
        else:
            self._db_port = DbClientBase.DEFAULT_PORT

        self._user_type = user_type
        self._db_name = db_name

    @property
    def db_name(self) -> str:
        return self._db_name

    @db_name.setter
    def db_name(self, db_name: str):
        self._db_name = db_name

    @property
    def db_hostname(self):
        return self._db_hostname

    @property
    def db_port(self):
        return self._db_port

    @property
    def user_type(self) -> UserTypeEnum:
        return self._user_type

    @property
    def mongo_db_client(self):
        return self._mongo_db_client

    @mongo_db_client.setter
    def mongo_db_client(self, mongo_db_client):
        self._mongo_db_client = mongo_db_client

    def verify_connected_to_db(self):
        try:
            self._mongo_db_client.get_default_database()
        except ServerSelectionTimeoutError:
            raise DbConnectionException(
                'Unable connect to DB with hostname ['
                f'{self.db_hostname}:{self.db_port}] due to a timeout')
        except OperationFailure as e:
            raise DbConnectionException(
                'Unable connect to DB with hostname ['
                f'{self.db_hostname}:{self.db_port}].\n'
                f'{e}')

    @staticmethod
    def get_mongo_db_hostname(hostname: str, port: int) -> str:
        return f'{hostname}:{port}'


class DbClient(DbClientBase):
    _db_client_dict = {}

    _mongo_db_client: MongoClient = None
    _db: Database = None

    _is_mock_db: bool = False

    def __init__(
            self,
            db_username: str,
            db_password: str,
            user_type: UserTypeEnum,
            db_hostname: str = None,
            db_port: int = None,
            db_name: str = None,
            is_tls: bool = False,
            is_unique: bool = True):
        super().__init__(db_hostname, db_port, user_type, db_name)

        if is_unique:
            self._create_unique_connection(
                db_username,
                db_password,
                user_type,
                db_hostname,
                db_port,
                db_name,
                is_tls)
        else:
            self._create_new_connection(
                db_username,
                db_password,
                user_type,
                db_hostname,
                db_port,
                db_name,
                is_tls)

    def get_mongo_db_uri(
            self,
            db_username: str = None,
            db_password: str = None,
            user_type: UserTypeEnum = UserTypeEnum.DB_USER,
            db_hostname: str = None,
            db_port: int = None,
            db_name: str = None,
            is_tls: bool = False):
        uri = self._get_uri_tls(is_tls)
        uri += self._get_uri_username_and_password(db_username, db_password)
        uri += self._get_uri_hostname_and_port(db_hostname, db_port)

        if user_type == UserTypeEnum.MONGO_DB_USER:
            uri += '/admin'
        elif db_name:
            uri += '/' + db_name
        elif db_username:
            uri += '/defaultauthdb'

        return uri

    @property
    def db(self) -> Database:
        return self._db

    @property
    def mongo_db_client(self) -> MongoClient:
        return self._mongo_db_client

    def is_db_exist(self, db_name: str) -> bool:
        return db_name in self.get_db_name_list()

    def get_db(self, db_name: str) -> Database:
        if not self.is_db_exist(db_name):
            raise DbException(f'Database [{db_name}] was not found')

        return self._mongo_db_client[db_name]

    def get_db_name_list(self) -> list:
        return self._mongo_db_client.list_database_names()

    def create_db(self, db_name: str, collection_name: str = None) -> Database:
        if db_name in self._mongo_db_client.list_database_names():
            raise DbException(f'Unable to create database [{db_name}]'
                              ' because it is already exist')

        logger().info(f'Create database [{db_name}]')
        db = self._mongo_db_client[db_name]

        if collection_name:
            logger().info(f'Create collection [{db_name}]')
            db.create_collection(collection_name)

        return db

    def delete_db(self, db_name: str):
        if self.is_db_exist(db_name):
            logger().info(f'Delete database [{db_name}]')
            self._mongo_db_client.drop_database(db_name)
        else:
            raise DbException(f'Unable to delete database [{db_name}]'
                              ' because it is not exist')

    def create_user(self, username: str, password: str, roles: list):
        if not self.db_name:
            raise DbException(f'Unable to create user [{username}]'
                              ' because database was not chosen')

        logger().info(f'Create user [{username}]')
        self.mongo_db_client[self.db_name].command('createUser', username,
                                                   pwd=password, roles=roles)

    def delete_user(self, username: str):
        if not self.db_name:
            raise DbException(f'Unable to delete user [{username}]'
                              ' because database was not chosen')

        try:
            logger().info(f'Delete user [{username}] if it is exist')
            self.mongo_db_client[self.db_name].command('dropUser', username)
        except OperationFailure:
            logger().debug(f'User [{username}] not exist')

    def get_collection_names(self) -> list:
        if not self.db_name:
            raise DbException('Unable to get collection names'
                              ' because database name was not provided')

        return self.mongo_db_client[self.db_name].list_collection_names()

    def get_users(self) -> dict:
        if not self.db_name:
            raise DbException('Unable to get users'
                              ' because database name was not provided')

        db = self.mongo_db_client[self.db_name]
        return db.command('usersInfo')['users']

    def _create_new_connection(
            self,
            db_username: str,
            db_password: str,
            user_type: UserTypeEnum,
            db_hostname: str,
            db_port: int,
            db_name: str,
            is_tls: bool):
        uri = self.get_mongo_db_uri(
            db_username,
            db_password,
            user_type,
            db_hostname,
            db_port,
            db_name,
            is_tls)
        logger().debug(f'Connect to MongoDB using URI [{uri}]')
        if DbClient.is_mock_db_enabled():
            self._mongo_db_client = mongomock.MongoClient(uri)
        else:
            self._mongo_db_client = MongoClient(uri)
        self.verify_connected_to_db()
        self._db = self._mongo_db_client.get_database()

    def _create_unique_connection(
            self,
            db_username: str,
            db_password: str,
            user_type: UserTypeEnum,
            db_hostname: str,
            db_port: int,
            db_name: str,
            is_tls: bool):
        key = self._get_db_client_key(db_username, user_type)

        if key in DbClient._db_client_dict:
            self.__dict__.update(DbClient._db_client_dict[key])
        else:
            self._create_new_connection(
                db_username,
                db_password,
                user_type,
                db_hostname,
                db_port,
                db_name,
                is_tls)
            DbClient._db_client_dict[key] = self

    @classmethod
    def _get_uri_tls(cls, is_tls: bool):
        if is_tls:
            return 'mongodb+srv://'
        return 'mongodb://'

    @classmethod
    def _get_uri_username_and_password(
            cls,
            db_username: str,
            db_password: str):
        if (db_username and not db_password) \
                or (db_password and not db_username):
            raise ApplicationException(
                f'Both Username [{db_username}] and Password [{db_password}]'
                ' must be with values, or both of them must be None')

        if db_username and db_password:
            return db_username + ':' + db_password + '@'

        return ''

    def _get_uri_hostname_and_port(self, hostname: str, port: int):
        if not hostname:
            hostname = self.LOCAL_HOST

        if not port:
            port = self.DEFAULT_PORT

        return f'{hostname}:{port}'

    def _get_db_client_key(self, db_username: str, user_type: UserTypeEnum):
        key = f'{self.db_hostname}_{self.db_port}'
        if db_username:
            key += f'_{db_username}_'

        key += str(user_type.value)

        return key

    @staticmethod
    def enable_mock_db():
        logger().debug('Unit test DbClient using mongomock')
        DbClient._is_mock_db = True

    @staticmethod
    def is_mock_db_enabled() -> bool:
        return DbClient._is_mock_db
