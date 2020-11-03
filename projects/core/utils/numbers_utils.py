from numbers import Number

from projects.core.objects.numbers import DecimalNumber


class NumbersUtil:

    @staticmethod
    def is_all_numbers(numbers: list) -> bool:
        for item in numbers:
            if (not isinstance(item, Number)
                and not isinstance(item, DecimalNumber)) \
                    or isinstance(item, bool):
                return False

        return True
