import unittest

from projects.core.exceptions.db_exceptions import \
    DbConnectionException, DbException
from projects.core.test.unittest_base import UnitTestBase


class DbExceptionsTest(UnitTestBase):
    def test_db_connection_exception(self):
        msg = 'test 123'
        self._verify_exception(DbConnectionException, msg)

    def test_db_exception(self):
        msg = 'test 123'
        self._verify_exception(DbException, msg)


if __name__ == '__main__':
    unittest.main()
