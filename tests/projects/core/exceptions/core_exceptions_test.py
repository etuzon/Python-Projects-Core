import unittest

from projects.core.exceptions.core_exceptions import ApplicationException
from projects.core.test.unittest_base import UnitTestBase


class CoreExceptionsTests(UnitTestBase):
    def test_application_exception(self):
        msg = 'test 123'
        self._verify_exception(ApplicationException, msg)


if __name__ == '__main__':
    unittest.main()
