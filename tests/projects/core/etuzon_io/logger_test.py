import unittest

from projects.core.exceptions.core_exceptions import ApplicationException
from projects.core.etuzon_io.logger import \
    ApplicationLogger, LogLevelEnum
from projects.core.test.unittest_base import UnitTestBase


class LoggerApplicationTests(UnitTestBase):
    def setUp(self):
        ApplicationLogger.destroy()

    def test_logger_print_without_exceptions(self):
        msg = '123'
        logger = ApplicationLogger(
            console_log_level=LogLevelEnum.DEBUG,
            file_log_level=LogLevelEnum.DEBUG)
        logger.debug(msg)
        logger.info(msg)
        logger.warn(msg)
        logger.error(msg)
        logger.critical(msg)
        logger.exception(msg)
        self.assertTrue(True)

    def test_logger_destroy(self):
        logger = ApplicationLogger(
            console_log_level=LogLevelEnum.DEBUG,
            file_log_level=LogLevelEnum.DEBUG)
        logger.instance()
        logger.destroy()
        with self.assertRaises(ApplicationException):
            logger.instance()

    def test_logger_close(self):
        logger = ApplicationLogger(
            console_log_level=LogLevelEnum.INFO,
            file_log_level=LogLevelEnum.DEBUG)
        self.assertTrue(logger.is_logger_init)
        self.assertTrue(not logger.is_logger_closed)
        logger.close()
        self.assertTrue(logger.is_logger_closed)


if __name__ == '__main__':
    unittest.main()
