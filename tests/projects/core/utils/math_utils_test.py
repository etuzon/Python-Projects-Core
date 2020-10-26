import unittest

from parameterized import parameterized

from projects.core.exceptions.core_exceptions import ApplicationException
from projects.core.utils.math_utils import MathUtil


class MathUtilTests(unittest.TestCase):
    @parameterized.expand([([1, 2, 3], [1, 1, 1], 2),
                           ([4, 9.5, 11.2], [1, 6.5, 2.5], 9.375),
                           ([-5, 0, 6], [3, 10, 18], 3)])
    def test_average(self, numbers, weights, expected_avg):
        avg = MathUtil.average(numbers, weights)
        self.assertTrue(avg == expected_avg, "Average of numbers ["
                        + str(numbers) + "] and weights ["
                        + str(weights) + "] is [" + str(avg)
                        + "], but it should be ["
                        + str(expected_avg) + "]")

    @parameterized.expand([([1, 2, 3], [1, 1]),
                           ([4, 9.5], [1, 6.5, 2.5])])
    def test_average_numbers_length_is_different_from_weights_length(
            self, numbers, weights):
        with self.assertRaises(ApplicationException):
            MathUtil.average(numbers, weights)

    @parameterized.expand([([1, True, 3], [1, 1, 1]),
                           ([4, 9.5, 4], [1, 6.5, "a"])])
    def test_average_numbers_and_weights_are_numbers(self, numbers, weights):
        with self.assertRaises(ApplicationException):
            MathUtil.average(numbers, weights)


if __name__ == '__main__':
    unittest.main()
