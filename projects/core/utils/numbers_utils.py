from numbers import Number


class NumbersUtil:

    @staticmethod
    def is_all_numbers(numbers: list) -> bool:
        for item in numbers:
            if not isinstance(item, Number) or isinstance(item, bool):
                return False

        return True
