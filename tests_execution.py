from projects.core.test.tests_suite import TestsSuite

if __name__ == '__main__':
    test_suite = TestsSuite(True)
    test_suite.run_tests()
    test_suite.create_report()
    test_suite.erase_data()
