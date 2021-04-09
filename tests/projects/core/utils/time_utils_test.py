from datetime import datetime

import time
import unittest

from projects.core.test.unittest_base import UnitTestBase
from projects.core.utils.time_utils import TimeUtil


class TimeUtilTests(UnitTestBase):
    def test_get_current_time_ms(self):
        prev = TimeUtil.get_current_time_ms()
        current = int(round(time.time() * 1000))
        future = TimeUtil.get_current_time_ms()
        self.assertTrue(current >= prev)
        self.assertTrue(future >= current)

    def test_date_to_ms(self):
        ms = TimeUtil.date_to_ms(datetime(1970, 1, 3))
        self.assertEqual(165600000, ms)


if __name__ == '__main__':
    unittest.main()
