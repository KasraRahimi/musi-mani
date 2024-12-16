from functools import cached_property
from horse import Horse
from random import random, choices
from math import comb
from itertools import product

def generate_horse_step_probabilities(horses: list[Horse], num_of_trials: int=2) -> None:
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


def calculate_probability_of_win_with_steps(
        index_of_winner: int,
        num_of_loser_steps: tuple[int, int, int],
        step_probabilities: tuple[float, ...],
        steps_to_victory: int=7
) -> float:
    num_of_steps = (
        *num_of_loser_steps[:index_of_winner],
        steps_to_victory - 1,
        *num_of_loser_steps[index_of_winner:]
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
    def __init__(self, bet: int, num_of_steps_to_victory: int=7, step_probabilities: tuple[float, ...]=None):
        self.num_of_steps_to_victory = num_of_steps_to_victory
        self.bet = bet
        self.horses = [Horse() for _ in range(4)]
        self.chosen_horse_index = None
        if step_probabilities is None:
            generate_horse_step_probabilities(self.horses)
            normalize_horse_step_probabilities(self.horses)
        else:
            for horse, probablity in zip(self.horses, step_probabilities):
                horse.step_probability = probablity

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

    def step(self) -> None:
        indices = tuple(range(len(self.horses)))
        if self.race_winner_index is None:
            random_horse_index = choices(indices, weights=self.horse_step_probabilities).pop()
            self.horses[random_horse_index].step()

    @property
    def winnings(self) -> int:
        if self.chosen_horse_index is None:
            return 0
        if self.race_winner_index is None:
            return 0
        if self.race_winner_index == self.chosen_horse_index:
            odds = self.win_probabilities[self.chosen_horse_index]
            return int(self.bet / odds)
        else:
            return 0



if __name__ == '__main__':
    horse_race = HorseRace(bet=0, num_of_steps_to_victory=7)
    for horse in horse_race.horses:
        print(horse)
    print(horse_race.win_probabilities)
    print(horse_race.win_probabilities)
    print(horse_race.win_probabilities)
    print(horse_race.win_probabilities)
    print(sum(horse_race.win_probabilities))
