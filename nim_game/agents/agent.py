from random import randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels  # уровень сложности

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
    def __easy_mode_turn(state_curr: list[int]) -> NimStateChange:
        choice = NimStateChange(0, 0)

        choice.heap_id = randint(1, len(state_curr))
        choice.decrease = randint(1, state_curr[choice.heap_id])

        return choice

    @staticmethod
    def __hard_mode_turn(state_curr: list[int]) -> NimStateChange:
        choice = NimStateChange(0, 0)

        if Agent.__xor_sum(state_curr) == 0:  # проигрышное положение
            return Agent.__easy_mode_turn(state_curr)

        curr_xor_sum = Agent.__xor_sum(state_curr)  # супер алгос из инета 3000
        bin_xor = bin(Agent.__xor_sum(state_curr))[2:][::-1]

        for i in range(1, len(state_curr)):
            temp_str = bin(state_curr[i])[2:][::-1]
            tn = len(bin_xor)

            if (len(temp_str) >= len(bin_xor)) and (temp_str[tn - 1] == bin_xor[tn - 1]):
                choice.heap_id = i
                choice.decrease = state_curr[i] - (state_curr[i] ^ curr_xor_sum)

                return choice

    @staticmethod
    def __normal_mode_turn(state_curr: list[int]) -> NimStateChange:
        if randint(0, 1):
            return Agent.__easy_mode_turn(state_curr)
        return Agent.__hard_mode_turn(state_curr)

    @staticmethod
    def __xor_sum(state_curr: list[int]) -> int:
        ans = 0
        for i in state_curr:
            ans ^= i
        return ans
