from horse import Horse
from random import random

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


class HorseRace:
    def __init__(self, bet: int, num_of_steps_to_victory: int=7):
        self.num_of_steps_to_victory = num_of_steps_to_victory
        self.bet = bet
        self.horses = [Horse() for _ in range(4)]
        generate_horse_step_probabilities(self.horses)
        normalize_horse_step_probabilities(self.horses)

if __name__ == '__main__':
    horse_race = HorseRace(0, num_of_steps_to_victory=7)
    sum_horse_probabilities = 0
    for horse in horse_race.horses:
        print(horse)
        sum_horse_probabilities += horse.step_probability
    print(f'{sum_horse_probabilities=}')
