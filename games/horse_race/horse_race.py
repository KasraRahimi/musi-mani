from functools import cached_property
from games.horse_race.horse_pool import HORSE_POOL
from games.horse_race.horse import Horse
from random import random, choices
from math import comb
from itertools import product
from dataclasses import dataclass


@dataclass
class HorseInfo:
    index: int
    name: str
    win_odds: float

    @property
    def win_multiplier(self) -> float:
        return 1 / self.win_odds


def generate_horse_step_probabilities(
    horses: list[Horse], num_of_trials: int = 2
) -> None:
    for horse in horses:
        random_number = 0
        for _ in range(num_of_trials):
            random_number += random()
        horse.step_probability = random_number / num_of_trials


def normalize_horse_step_probabilities(horses: list[Horse]) -> None:
    sum_horse_probabilities = 0
    for horse in horses:
        sum_horse_probabilities += horse.step_probability

    for horse in horses:
        horse.step_probability /= sum_horse_probabilities


def get_random_horses(count: int=4) -> list[Horse]:
    weights = [horse.selection_weight for horse in HORSE_POOL]
    horses = []
    while len(horses) < count:
        horse_to_add = choices(HORSE_POOL, weights=weights).pop()
        if horse_to_add not in horses:
            horses.append(horse_to_add.copy())
    return horses


def calculate_probability_of_win_with_steps(
    index_of_winner: int,
    num_of_loser_steps: tuple[int, int, int],
    step_probabilities: tuple[float, ...],
    steps_to_victory: int = 7,
) -> float:
    num_of_steps = (
        *num_of_loser_steps[:index_of_winner],
        steps_to_victory - 1,
        *num_of_loser_steps[index_of_winner:],
    )
    probability_product = 1
    for i, probability in enumerate(step_probabilities):
        probability_product *= probability ** num_of_steps[i]

    tmp_step_list = list(num_of_steps)
    combinations = 1
    while len(tmp_step_list) > 0:
        tmp_step = tmp_step_list.pop()
        combinations *= comb(sum(tmp_step_list + [tmp_step]), tmp_step)

    return probability_product * step_probabilities[index_of_winner] * combinations


class HorseRace:
    def __init__(
        self,
        bet: int,
        num_of_steps_to_victory: int = 7,
        horses: list[Horse] = None,
    ):
        self.num_of_steps_to_victory = num_of_steps_to_victory
        self.bet = bet
        self.chosen_horse_index = None

        if horses is None:
            horses = get_random_horses(count=4)
            normalize_horse_step_probabilities(horses)
            self.horses = horses
        else:
            self.horses = horses

    @property
    def horse_step_probabilities(self) -> tuple[float, ...]:
        return tuple([horse.step_probability for horse in self.horses])

    @cached_property
    def win_probabilities(self) -> tuple[float, ...]:
        win_probabilities = [0 for _ in range(4)]
        step_probabilities = self.horse_step_probabilities
        for i, j, k in product(range(self.num_of_steps_to_victory), repeat=3):
            for index, win in enumerate(win_probabilities):
                win_probabilities[index] += calculate_probability_of_win_with_steps(
                    index_of_winner=index,
                    num_of_loser_steps=(i, j, k),
                    step_probabilities=step_probabilities,
                    steps_to_victory=self.num_of_steps_to_victory,
                )
        return tuple(win_probabilities)

    @property
    def horse_infos(self) -> tuple[HorseInfo, ...]:
        horse_infos = []
        for i, horse in enumerate(self.horses):
            horse_infos.append(
                HorseInfo(
                    index=i,
                    name=horse.name,
                    win_odds=self.win_probabilities[i],
                )
            )
        return tuple(horse_infos)

    def pick_winning_horse(self, index: int) -> None:
        if index < 0 or index >= len(self.horses):
            raise IndexError("Index out of range")
        self.chosen_horse_index = index

    @property
    def race_winner_index(self) -> int | None:
        for i, horse in enumerate(self.horses):
            if horse.number_of_steps == self.num_of_steps_to_victory:
                return i

        return None

    @property
    def winning_horse_info(self) -> HorseInfo | None:
        if self.race_winner_index is None:
            return None
        else:
            return self.horse_infos[self.race_winner_index]

    @property
    def chosen_horse_info(self) -> HorseInfo | None:
        if self.chosen_horse_index is not None:
            return self.horse_infos[self.chosen_horse_index]
        else:
            return None

    def step(self) -> None:
        indices = tuple(range(len(self.horses)))
        if self.race_winner_index is None:
            random_horse_index = choices(
                indices, weights=self.horse_step_probabilities
            ).pop()
            self.horses[random_horse_index].step()

    @property
    def horses_position_string(self) -> str:
        position_strings = []
        for horse in self.horses:
            position_strings.append(horse.position_string(self.num_of_steps_to_victory))
        return "\n".join(position_strings)

    @property
    def potential_payouts(self) -> tuple[int, ...]:
        payouts = [
            int(self.bet * horse_info.win_multiplier) for horse_info in self.horse_infos
        ]
        return tuple(payouts)

    @property
    def is_game_over(self) -> bool:
        return self.race_winner_index is not None

    @property
    def winnings(self) -> int:
        if self.chosen_horse_index is None:
            return 0
        if self.race_winner_index is None:
            return 0
        if self.race_winner_index == self.chosen_horse_index:
            return int(self.bet * self.winning_horse_info.win_multiplier)
        else:
            return 0

    @property
    def is_player_win(self) -> bool:
        if self.is_game_over:
            return self.chosen_horse_index == self.race_winner_index
        else:
            return False

    @classmethod
    def simulate_horse_races(
            cls,
            horses: list[Horse],
            num_of_steps_to_victory:int = 7,
            num_of_trials: int = 100
    ) -> tuple[float, ...]:
        game_wins = [0 for _ in range(len(horses))]
        for i in range(num_of_trials):
            new_horses = list(map(lambda horse: horse.copy(), horses))
            horse_race = cls(bet=0, num_of_steps_to_victory=num_of_steps_to_victory, horses=new_horses)
            while not horse_race.is_game_over:
                horse_race.step()
            game_wins[horse_race.race_winner_index] += 1

        return tuple([game_win / num_of_trials for game_win in game_wins])


if __name__ == "__main__":
    horse_race = HorseRace(bet=100, num_of_steps_to_victory=7)
    simulation_outcome = HorseRace.simulate_horse_races(horse_race.horses, 7, 10_000)
    for horse_info, win_odds, simulation_odds in zip(horse_race.horse_infos, horse_race.win_probabilities, simulation_outcome):
        print(f"{horse_info.name}\ntheoretical odds: {horse_info.win_odds*100:.3f}%\nsimulation odds: {simulation_odds*100:.3f}%\n")