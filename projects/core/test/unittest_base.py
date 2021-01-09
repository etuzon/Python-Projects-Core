import unittest

from projects.core.etuzon_io.logger import \
    LogLevelEnum, init_logger, logger, ApplicationLogger


class UnitTestBase(unittest.TestCase):
    SEPARATOR = '=' * 70

    console_log_level: LogLevelEnum = LogLevelEnum.INFO
    file_log_level: LogLevelEnum = LogLevelEnum.DEBUG
    log_file_path: str = None

    @classmethod
    def setUpClass(
            cls):
        init_logger(LogLevelEnum.DEBUG, LogLevelEnum.DEBUG)

    def setUp(self) -> None:
        # In LoggerApplicationTests ApplicationLogger.destroy()
        # is being executed
        init_logger(LogLevelEnum.DEBUG, LogLevelEnum.DEBUG)
        if not ApplicationLogger.is_logger_closed:
            logger().info(
                f'\n{self.SEPARATOR}\n'
                f'     Start Test [{self._testMethodName}]\n'
                f'{self.SEPARATOR}')

    def tearDown(self) -> None:
        # In LoggerApplicationTests ApplicationLogger.destroy()
        # is being executed
        init_logger(LogLevelEnum.DEBUG, LogLevelEnum.DEBUG)
        if not ApplicationLogger.is_logger_closed:
            logger().info(
                f'\n{self.SEPARATOR}\n'
                f'     End Test [{self._testMethodName}]\n'
                f'{self.SEPARATOR}')

    def _verify_exception(self, exception_class_type, expected_message):
        with self.assertRaises(exception_class_type) as e:
            raise exception_class_type(expected_message)

        self.assertTrue(e.exception.message == expected_message)
