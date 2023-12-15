from random import randint

from nim_game.common.models import NimStateChange

HEAPS_AMOUNT_MIN = 2
HEAPS_AMOUNT_MAX = 10

STONE_AMOUNT_MIN = 1        # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10       # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]       # кучки

    def __init__(self, heaps_amount: int) -> None:
        if not (isinstance(heaps_amount, int) and
                HEAPS_AMOUNT_MIN <= heaps_amount <= HEAPS_AMOUNT_MAX):
            raise ValueError
        self._heaps = [randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX)
                       for _ in range(heaps_amount)]

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек

        :return: копия списка кучек
        """

        return self._heaps.copy()

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния
        """
        if not ((0 <= state_change.heap_id-1 < len(self._heaps)) and
                (0 < state_change.decrease <=
                 self._heaps[state_change.heap_id - 1])):
            raise ValueError
        self._heaps[state_change.heap_id - 1] -= state_change.decrease
