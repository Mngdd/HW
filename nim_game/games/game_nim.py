import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent
from nim_game.common.enumerations import Players


class GameNim:
    _environment: EnvironmentNim  # состояния кучек
    _agent: Agent  # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config) as f:
            data = json.load(f)
            self._agent = Agent(data["opponent_level"])
            self._environment = EnvironmentNim(data["heaps_amount"])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """

        game_ = GameState()

        self._environment.change_state(player_step)

        if self.is_game_finished():
            game_.heaps_state = self.heaps_state
            game_.opponent_step = None
            game_.winner = Players.USER
            return game_

        bot_step = self._agent.make_step(self.heaps_state)
        self._environment.change_state(bot_step)

        if self.is_game_finished():
            game_.heaps_state = self.heaps_state
            game_.opponent_step = player_step
            game_.winner = Players.BOT
            return game_

        game_.heaps_state = self.heaps_state
        game_.opponent_step = player_step
        game_.winner = None

        return game_

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        return len(self.heaps_state) == 0

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
