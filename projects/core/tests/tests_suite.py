import unittest
from unittest import TestLoader, TextTestRunner, TestSuite, TestResult


class TestsSuite:
    _test_suite: TestSuite
    _test_loader: TestLoader
    _text_test_runner: TextTestRunner
    _tests_suite: TestSuite
    _test_results: TestResult = None

    def __init__(self, test_classes_list: list):
        self._test_suite = unittest.TestSuite()
        self._test_loader = unittest.TestLoader()
        self._text_test_runner = unittest.TextTestRunner()
        self._init_tests(test_classes_list)

    def run(self):
        self._test_results = self._text_test_runner.run(self._tests_suite)

    def _init_tests(self ,test_classes_list: list):
        tests_list = []

        for test_class in test_classes_list:
            test_suite = self._test_loader.loadTestsFromTestCase(test_class)
            tests_list.append(test_suite)

        self._tests_suite = unittest.TestSuite(tests_list)
