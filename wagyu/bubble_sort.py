from typing import (Callable,
                    MutableSequence)

from .hints import Domain


def bubble_sort(sequence: MutableSequence[Domain],
                comparator: Callable[[Domain, Domain], bool],
                on_swap: Callable[[Domain, Domain], None]
                ) -> MutableSequence[Domain]:
    if not sequence:
        return sequence
    result = sequence[:]
    while True:
        no_swaps = True
        for index in range(len(result) - 1):
            if not comparator(result[index], result[index + 1]):
                on_swap(result[index], result[index + 1])
                result[index], result[index + 1] = (result[index + 1],
                                                    result[index])
                if no_swaps:
                    no_swaps = False
        if no_swaps:
            return result
