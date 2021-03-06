import sys
from decimal import Decimal
from typing import Optional

from hypothesis import strategies

from tests.utils import Strategy
from wagyu.hints import Coordinate

MAX_VALUE = 10 ** 6
MIN_VALUE = -MAX_VALUE


def to_floats(min_value: Optional[Coordinate] = None,
              max_value: Optional[Coordinate] = None) -> Strategy:
    return (strategies.floats(min_value=min_value,
                              max_value=max_value,
                              allow_nan=False,
                              allow_infinity=False)
            .map(to_digits_count))


def to_digits_count(number: float,
                    *,
                    max_digits_count: int = sys.float_info.dig) -> float:
    decimal = Decimal(number).normalize()
    _, significant_digits, exponent = decimal.as_tuple()
    significant_digits_count = len(significant_digits)
    if exponent < 0:
        fixed_digits_count = (1 - exponent
                              if exponent <= -significant_digits_count
                              else significant_digits_count)
    else:
        fixed_digits_count = exponent + significant_digits_count
    if fixed_digits_count <= max_digits_count:
        return number
    whole_digits_count = max(significant_digits_count + exponent, 0)
    if whole_digits_count:
        whole_digits_offset = max(whole_digits_count - max_digits_count, 0)
        decimal /= 10 ** whole_digits_offset
        whole_digits_count -= whole_digits_offset
    else:
        decimal *= 10 ** (-exponent - significant_digits_count)
        whole_digits_count = 1
    decimal = round(decimal, min(max(max_digits_count - whole_digits_count, 0),
                                 significant_digits_count))
    return float(str(decimal))


floats = to_floats(MIN_VALUE, MAX_VALUE)
coordinates = strategies.integers(MIN_VALUE, MAX_VALUE)
trits = strategies.sampled_from([-1, 0, 1])
sizes = strategies.integers(0, 65535)
integers_32 = strategies.integers(-2147483648, 2147483647)
non_negative_integers = strategies.integers(0)
