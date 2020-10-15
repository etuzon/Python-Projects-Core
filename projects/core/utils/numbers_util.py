from numbers import Number


class NumbersUtil:

    @staticmethod
    def is_all_numbers(numbers: list) -> bool:
        for item in numbers:
            if not isinstance(item, Number):
                return False

        return True
