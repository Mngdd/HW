from random import randint, choice

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        if level not in (AgentLevels.EASY.value,
                         AgentLevels.NORMAL.value,
                         AgentLevels.HARD.value):
            raise ValueError
        self._level = AgentLevels(level)

    def make_step(self, state_curr: list[int]) -> NimStateChange:

        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """

        match self._level:
            case AgentLevels.EASY:
                return self.__easy_mode_turn(state_curr)
            case AgentLevels.NORMAL:
                return self.__normal_mode_turn(state_curr)
            case AgentLevels.HARD:
                return self.__hard_mode_turn(state_curr)

    @staticmethod
    def __easy_mode_turn(state_curr):
        non_empty_heaps = []
        for i in range(len(state_curr)):
            if state_curr[i] != 0:
                non_empty_heaps.append(i)
        heap_id = choice(non_empty_heaps)

        return NimStateChange(heap_id + 1, randint(1, state_curr[heap_id]))

    @staticmethod
    def __normal_mode_turn(state_curr):
        if randint(0, 1):
            return Agent.__easy_mode_turn(state_curr)
        return Agent.__hard_mode_turn(state_curr)

    @staticmethod
    def __hard_mode_turn(state_curr):  # до этого косячный был немног, пофиксил
        if Agent.__xor_sum(state_curr) == 0:
            return Agent.__easy_mode_turn(state_curr)

        for heap_id in range(len(state_curr)):
            for dec in range(1, state_curr[heap_id] + 1):
                state_curr[heap_id] -= dec
                if Agent.__xor_sum(state_curr) == 0:
                    state_curr[heap_id] += dec
                    return NimStateChange(heap_id + 1, dec)
                state_curr[heap_id] += dec
        return Agent.__easy_mode_turn(state_curr)

    @staticmethod
    def __xor_sum(state_curr):
        ans = 0
        for i in state_curr:
            ans ^= i
        return ans
