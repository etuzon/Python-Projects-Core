import unittest

from parameterized import parameterized

from projects.core.utils.numbers_utils import NumbersUtil


class NumbersUtilTests(unittest.TestCase):

    @parameterized.expand(
        [([1, 2, 3], ),
         ([11.2], ),
         ([-5, 0, 612344], )])
    def test_all_numbers(self, numbers):
        self.assertTrue(NumbersUtil.is_all_numbers(numbers))

    @parameterized.expand(
        [(['1a', 2, 3],),
         (['11.2'],),
         ([-5, True, 612344],),
         ([-5, 6, False],)])
    def test_all_numbers_negative(self, numbers):
        self.assertFalse(
            NumbersUtil.is_all_numbers(numbers),
            'Test was not found that there is'
            f'none numeric variable in [{numbers}]')


if __name__ == '__main__':
    unittest.main()
