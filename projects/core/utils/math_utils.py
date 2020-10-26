from decimal import Decimal

from projects.core.exceptions.core_exceptions import ApplicationException
from projects.core.utils.numbers_utils import NumbersUtil


class MathUtil:
    @staticmethod
    def average(numbers: list, weights: list) -> Decimal:
        MathUtil._verify_all_list_are_numbers(numbers)
        MathUtil._verify_all_list_are_numbers(weights)

        if len(numbers) != len(weights):
            raise ApplicationException("Numbers list len ["
                                       + str(len(numbers))
                                       + "] is different from "
                                         "weights list len ["
                                       + str(len(weights)) + "]")
        numbers_weighted = 0

        for i in range(len(numbers)):
            numbers_weighted += numbers[i] * weights[i]

        return numbers_weighted / sum(weights)

    @staticmethod
    def _verify_all_list_are_numbers(numbers: list):
        if not NumbersUtil.is_all_numbers(numbers):
            raise ApplicationException("Not all numbers in list ["
                                       + str(numbers) + "] are numbers.")
