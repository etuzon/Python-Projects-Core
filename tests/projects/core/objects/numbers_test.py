import unittest

from parameterized import parameterized
from projects.core.objects.numbers import \
    DecimalNumber, set_decimal_number_prec


class DecimalNumberTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        set_decimal_number_prec(6)

    @parameterized.expand(
        [(DecimalNumber(1), DecimalNumber(3), DecimalNumber(4)),
         (DecimalNumber(-1), DecimalNumber(3), DecimalNumber(2)),
         (DecimalNumber(5.5), DecimalNumber(7.1), DecimalNumber(12.6)),
         (DecimalNumber(0), DecimalNumber(3.2), DecimalNumber(3.2)),
         (DecimalNumber(1.1), 3, DecimalNumber(4.1)),
         (DecimalNumber(1.2), 3.2, DecimalNumber(4.4))])
    def test_add(self, num1, num2, expected_result):
        result = num1 + num2
        self.assertTrue(result == expected_result,
                        "Result is [" + str(result)
                        + "], but it should be ["
                        + str(expected_result) + "]")

    @parameterized.expand(
        [(DecimalNumber(1), DecimalNumber(3), DecimalNumber(-2)),
         (DecimalNumber(-1), DecimalNumber(3), DecimalNumber(-4)),
         (DecimalNumber(5.5), DecimalNumber(7.1), DecimalNumber(-1.6)),
         (DecimalNumber(0), DecimalNumber(3.2), DecimalNumber(-3.2)),
         (DecimalNumber(1.1), 3, DecimalNumber(-1.9)),
         (DecimalNumber(1.2), 3.2, DecimalNumber(-2))])
    def test_sub(self, num1, num2, expected_result):
        result = num1 - num2
        self.assertTrue(result == expected_result,
                        "Result is [" + str(result)
                        + "], but it should be ["
                        + str(expected_result) + "]")

    @parameterized.expand(
        [(DecimalNumber(1), DecimalNumber(3), DecimalNumber(3)),
         (DecimalNumber(-1), DecimalNumber(-3), DecimalNumber(3)),
         (DecimalNumber(5.5), DecimalNumber(7.1), DecimalNumber(39.05)),
         (DecimalNumber(0), DecimalNumber(3.2), DecimalNumber(0)),
         (DecimalNumber(1.1), 3, DecimalNumber(3.3)),
         (DecimalNumber(1.2), 3.2, DecimalNumber(3.84))])
    def test_multiple(self, num1, num2, expected_result):
        result = num1 * num2
        self.assertTrue(result == expected_result,
                        "Result is [" + str(result)
                        + "], but it should be ["
                        + str(expected_result) + "]")

    @parameterized.expand(
        [(DecimalNumber(1), DecimalNumber(1), DecimalNumber(1)),
         (DecimalNumber(-1), DecimalNumber(-4), DecimalNumber(0.25)),
         (DecimalNumber(10), DecimalNumber(4), DecimalNumber(2.5)),
         (DecimalNumber(0), DecimalNumber(3.2), DecimalNumber(0)),
         (DecimalNumber(9), 3, DecimalNumber(3)),
         (DecimalNumber(-9), 6, DecimalNumber(-1.5))])
    def test_div(self, num1, num2, expected_result):
        result = num1 / num2
        self.assertTrue(result == expected_result,
                        "Result is [" + str(result)
                        + "], but it should be ["
                        + str(expected_result) + "]")

    @parameterized.expand(
        [(DecimalNumber(1), DecimalNumber(1), DecimalNumber(1)),
         (DecimalNumber(-2), DecimalNumber(2), DecimalNumber(4)),
         (DecimalNumber(10), DecimalNumber(3), DecimalNumber(1000)),
         (DecimalNumber(0), DecimalNumber(3.2), DecimalNumber(0)),
         (DecimalNumber(9), 2.5, DecimalNumber(243)),
         (DecimalNumber(-9), 6, DecimalNumber(531441))])
    def test_pow(self, num1, num2, expected_result):
        result = num1 ** num2
        self.assertTrue(result == expected_result,
                        "Result is [" + str(result)
                        + "], but it should be ["
                        + str(expected_result) + "]")

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(1)),
                           (DecimalNumber(2), DecimalNumber(2)),
                           (DecimalNumber(0), DecimalNumber(0)),
                           (DecimalNumber(0), 0),
                           (DecimalNumber(9), 9),
                           (DecimalNumber(-9.555), -9.555)])
    def test_equal_operator(self, num1, num2):
        self.assertTrue(num1 == num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(1.1)),
                           (DecimalNumber(2), DecimalNumber(-2)),
                           (DecimalNumber(0), DecimalNumber(0.1)),
                           (DecimalNumber(0), -0.01),
                           (DecimalNumber(9), 19),
                           (DecimalNumber(-9.555), 9.555)])
    def test_equal_operator_negative(self, num1, num2):
        self.assertFalse(num1 == num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(1.1)),
                           (DecimalNumber(2), DecimalNumber(-2)),
                           (DecimalNumber(0), DecimalNumber(0.1)),
                           (DecimalNumber(0), -0.01),
                           (DecimalNumber(9), 19),
                           (DecimalNumber(-9.555), 9.555)])
    def test_different_operator(self, num1, num2):
        self.assertTrue(num1 != num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(1)),
                           (DecimalNumber(2), DecimalNumber(2)),
                           (DecimalNumber(0), DecimalNumber(0)),
                           (DecimalNumber(0), 0),
                           (DecimalNumber(9), 9),
                           (DecimalNumber(-9.555), -9.555)])
    def test_different_operator_negative(self, num1, num2):
        self.assertFalse(num1 != num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(0.99)),
                           (DecimalNumber(2), DecimalNumber(-2)),
                           (DecimalNumber(0), DecimalNumber(-0.1)),
                           (DecimalNumber(0), -90),
                           (DecimalNumber(9), 8),
                           (DecimalNumber(-9.555), -19.555)])
    def test_gt_operator(self, num1, num2):
        self.assertTrue(num1 > num2)

    @parameterized.expand([(DecimalNumber(-11), DecimalNumber(-1.1)),
                           (DecimalNumber(2), DecimalNumber(2)),
                           (DecimalNumber(0), DecimalNumber(0.1)),
                           (DecimalNumber(0), 0.01),
                           (DecimalNumber(9), 9),
                           (DecimalNumber(-9.555), 9.555)])
    def test_gt_operator_negative(self, num1, num2):
        self.assertFalse(num1 > num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(1.99)),
                           (DecimalNumber(2), DecimalNumber(22)),
                           (DecimalNumber(0), DecimalNumber(0.1)),
                           (DecimalNumber(-10.102), 90),
                           (DecimalNumber(9), 18),
                           (DecimalNumber(-9.555), 19.555)])
    def test_lt_operator(self, num1, num2):
        self.assertTrue(num1 < num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(-1.1)),
                           (DecimalNumber(2), DecimalNumber(2)),
                           (DecimalNumber(1), DecimalNumber(0.1)),
                           (DecimalNumber(20), 0.01),
                           (DecimalNumber(9), 9),
                           (DecimalNumber(19.555), 9.555)])
    def test_lt_operator_negative(self, num1, num2):
        self.assertFalse(num1 < num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(0.99)),
                           (DecimalNumber(2), DecimalNumber(2)),
                           (DecimalNumber(0), DecimalNumber(-0.1)),
                           (DecimalNumber(0), -90),
                           (DecimalNumber(9), 9),
                           (DecimalNumber(-9.555), -19.555)])
    def test_ge_operator(self, num1, num2):
        self.assertTrue(num1 >= num2)

    @parameterized.expand([(DecimalNumber(-11), DecimalNumber(-1.1)),
                           (DecimalNumber(2), DecimalNumber(2.1)),
                           (DecimalNumber(0), DecimalNumber(0.1)),
                           (DecimalNumber(0), 0.01),
                           (DecimalNumber(9), 9.001),
                           (DecimalNumber(-9.555), 9.555)])
    def test_ge_operator_negative(self, num1, num2):
        self.assertFalse(num1 >= num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(1.99)),
                           (DecimalNumber(22), DecimalNumber(22)),
                           (DecimalNumber(0), DecimalNumber(0.1)),
                           (DecimalNumber(-10.102), 90),
                           (DecimalNumber(9), 18),
                           (DecimalNumber(-9.555), -9.555)])
    def test_le_operator(self, num1, num2):
        self.assertTrue(num1 <= num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(-1.1)),
                           (DecimalNumber(2), DecimalNumber(-2)),
                           (DecimalNumber(1), DecimalNumber(0.1)),
                           (DecimalNumber(20), 0.01),
                           (DecimalNumber(9), 8),
                           (DecimalNumber(19.555), 1.555)])
    def test_le_operator_negative(self, num1, num2):
        self.assertFalse(num1 <= num2)

    @parameterized.expand([(DecimalNumber(1), DecimalNumber(1)),
                           (DecimalNumber(2), DecimalNumber(2)),
                           (DecimalNumber(-1.1), DecimalNumber(1.1)),
                           (DecimalNumber(20), DecimalNumber(20)),
                           (DecimalNumber(-9), DecimalNumber(9)),
                           (DecimalNumber(19.555), DecimalNumber(19.555))])
    def test_abs(self, num, expected_result):
        self.assertTrue(abs(num) == expected_result)

    def test_prec(self):
        num1 = DecimalNumber(9.123456789, 8)
        self.assertTrue(num1, 9.12345678)
        self.assertTrue(num1.get_prec() == 8)
        self.assertTrue(
            DecimalNumber.get_prec() == DecimalNumber.DEFAULT_PREC,
            "DecimalNumber.prec value is ["
            + str(DecimalNumber.get_prec()) + "] but should be ["
            + str(DecimalNumber.DEFAULT_PREC) + "]")
        DecimalNumber.set_prec(2)
        num2 = DecimalNumber(4.1234)
        self.assertTrue(num2 == 4.12)
        DecimalNumber.set_prec(10)
        self.assertTrue(DecimalNumber.get_prec() == 10)
        DecimalNumber.set_prec(DecimalNumber.DEFAULT_PREC)

    @parameterized.expand([(DecimalNumber(11.1111), 2, DecimalNumber(11.11)),
                           (DecimalNumber(22.33331111), None, 22)])
    def test_round(self, num, digits, expected_result):
        result = round(num, digits)
        self.assertTrue(
            result == expected_result,
            "Result of round [" + str(num) + "] with [" + str(digits)
            + "] digits is [" + str(result) + "], but should be ["
            + str(expected_result) + "]")

    @parameterized.expand([(DecimalNumber(11.1111), DecimalNumber(-11.1111)),
                           (DecimalNumber(0), DecimalNumber(0)),
                           (DecimalNumber(-5), DecimalNumber(5)),
                           (DecimalNumber(44), DecimalNumber(-44)),
                           (DecimalNumber(-5.22), DecimalNumber(5.22)),
                           (DecimalNumber(44), -44)])
    def test_negative(self, num, expected_result):
        self.assertTrue(-num == expected_result)


if __name__ == '__main__':
    unittest.main()
