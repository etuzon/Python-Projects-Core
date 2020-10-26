import unittest
from coverage import Coverage


class TestsSuite:
    CONFIG_FILE = ".coveragerc"

    _coverage: Coverage = None
    _is_coverage: bool

    def __init__(self, is_coverage: bool = False):
        self._coverage = Coverage(config_file=self.CONFIG_FILE)
        self._is_coverage = is_coverage

    def run_tests(self):
        if self._is_coverage:
            self._coverage.start()

        tests = unittest.TestLoader().discover(start_dir='.',
                                               pattern='*_test.py')
        unittest.TextTestRunner(verbosity=2).run(tests)

        if self._is_coverage:
            self._coverage.stop()

    def create_report(self):
        self._coverage.report()
        self._coverage.json_report()
        self._coverage.html_report()

    def erase_data(self):
        self._coverage.erase()
