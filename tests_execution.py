from projects.core.etuzon_io.logger import init_logger, LogLevelEnum
from projects.core.test.tests_suite import TestsSuite

if __name__ == '__main__':
    init_logger(LogLevelEnum.DEBUG, LogLevelEnum.DEBUG)
    test_suite = TestsSuite(True)
    test_suite.run_tests()
    test_suite.create_report()
    test_suite.erase_data()
