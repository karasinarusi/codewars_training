import typing


class SpiralCreator:
    ZERO = 0
    POINT = 1

    def __init__(self, size: int):
        self.size = size
        self._is_size_even = self.is_even(self.size)

    def _change_value(self, value: int) -> typing.Optional[int]:
        if value == self.ZERO:
            return self.POINT
        if value == self.POINT:
            return self.ZERO

    def _get_row_half(self, row_number: int) -> int:
        """Возвращает 1, если строка относится к верхней половине спирали"""
        """ 2 - если к нижней """
        if self._is_size_even:
            if self.size % 4 == 0:
                return 2 if row_number >= self.size / 2 else 1
            return 2 if row_number > self.size / 2 else 1
        else:
            return 2 if row_number > self.size / 2 else 1

    def _get_row_more_points(self, number: int, half: int) -> bool:
        """Возвращает True, если в строке больше точек, чем пропусков"""
        is_number_even = self.is_even(number)
        if is_number_even and not self._is_size_even:
            return True
        if self._is_size_even:
            if half == 1 and is_number_even:
                return True
            if half == 2 and not is_number_even:
                return True
        return False

    def _get_mono_row(self, full: bool = False) -> typing.List[int]:
        return [self.POINT if full else self.ZERO for i in range(self.size)]

    def _change_values_on_positions(self, row: typing.List[int], positions: typing.List[int]):
        return [
            row[i] if i not in positions else self._change_value(row[i]) for i in range(len(row))
        ]

    def _get_positions_to_replace(
        self,
        row_number: int,
        half: int,
        default_positions: typing.List[int],
        left_start: int,
        right_start: int,
        range_start: int = 0,
    ):
        if half == 1:
            iter_range = range(range_start, row_number + 1, 2)
        else:
            iter_range = range((self.size - row_number) // 2)
        res = default_positions.copy()
        for i in iter_range:
            if left_start < right_start:
                left_start += 2
                right_start -= 2
                res.append(left_start)
                res.append(right_start)

        return res

    def _make_more_points_row(self, number: int, half_number: int) -> typing.List[int]:
        if number == 0 or number == self.size - 1:
            return self._get_mono_row(full=True)
        left = -1
        if half_number == 2:
            return self._change_values_on_positions(
                row=self._get_mono_row(full=True),
                positions=self._get_positions_to_replace(
                    row_number=number,
                    half=half_number,
                    default_positions=[],
                    left_start=left,
                    right_start=self.size,
                ),
            )
        elif half_number == 1:
            right = self.size - 2
            return self._change_values_on_positions(
                row=self._get_mono_row(full=True),
                positions=self._get_positions_to_replace(
                    row_number=number,
                    half=half_number,
                    default_positions=[right],
                    left_start=left,
                    right_start=right,
                    range_start=4,
                ),
            )

    def _make_more_spaces_row(self, number: int, half_number: int) -> typing.List[int]:

        left = -2
        if half_number == 2:
            return self._change_values_on_positions(
                row=self._get_mono_row(full=False),
                positions=self._get_positions_to_replace(
                    row_number=number,
                    half=half_number,
                    default_positions=[],
                    left_start=left,
                    right_start=self.size + 1,
                ),
            )
        elif half_number == 1:
            right = self.size - 1
            return self._change_values_on_positions(
                row=self._get_mono_row(full=False),
                positions=self._get_positions_to_replace(
                    row_number=number,
                    half=half_number,
                    default_positions=[right],
                    left_start=left,
                    right_start=right,
                    range_start=3,
                ),
            )

    def _get_row_by_number(self, number: int) -> typing.List[int]:
        half = self._get_row_half(row_number=number)
        if self._get_row_more_points(number=number, half=half):
            return self._make_more_points_row(number=number, half_number=half)
        else:
            return self._make_more_spaces_row(number=number, half_number=half)

    def crete_spiral(self):
        return [self._get_row_by_number(raw_number) for raw_number in range(self.size)]

    @staticmethod
    def is_even(value: int) -> bool:
        return value % 2 == 0


def spiralize(size):
    return [row for row in SpiralCreator(size=size).crete_spiral()]
