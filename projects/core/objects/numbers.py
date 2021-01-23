

class DecimalNumber:
    DEFAULT_PREC = 6

    _prec: int = 6

    _number: float = None
    _local_prec: int = None

    def __init__(self, number, prec: int = None):
        if prec is not None:
            self._local_prec = prec
        else:
            self._local_prec = DecimalNumber._prec

        self._number = round(float(number), self._local_prec)

    @property
    def number(self) -> float:
        return self._number

    def __add__(self, other):
        return DecimalNumber(self._number + float(other))

    def __sub__(self, other):
        return DecimalNumber(self._number - float(other))

    def __mul__(self, other):
        return DecimalNumber(self._number * float(other))

    def __truediv__(self, other):
        return DecimalNumber(self._number / float(other))

    def __pow__(self, power, modulo=None):
        return DecimalNumber(self.number ** float(power))

    def __neg__(self):
        return DecimalNumber(-self.number)

    def __eq__(self, other) -> bool:
        return self.number == float(DecimalNumber(other))

    def __ne__(self, other) -> bool:
        return self.number != float(DecimalNumber(other))

    def __gt__(self, other) -> bool:
        return self.number > float(DecimalNumber(other))

    def __ge__(self, other):
        return self.number >= float(DecimalNumber(other))

    def __lt__(self, other):
        return self.number < float(DecimalNumber(other))

    def __le__(self, other):
        return self.number <= float(DecimalNumber(other))

    def __float__(self):
        return self.number

    def __int__(self):
        return int(self.number)

    def __abs__(self):
        if self.number < 0:
            return DecimalNumber(-self.number)

        return DecimalNumber(self.number)

    def __round__(self, n=None):
        return DecimalNumber(round(self._number, n))

    def __str__(self):
        return str(self.number)

    def __setattr__(self, key, value):
        if key == '_number':
            self.__dict__[key] = round(float(value), self._get_prec())
        else:
            self.__dict__[key] = value

    @staticmethod
    def set_prec(prec: int):
        DecimalNumber._prec = prec

    def get_prec(self=None):
        if self:
            return self._local_prec
        return DecimalNumber._prec

    def _get_prec(self) -> int:
        return self._local_prec


def set_decimal_number_prec(prec: int):
    DecimalNumber._prec = prec
