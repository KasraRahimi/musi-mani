from dataclasses import dataclass
from typing import Self

@dataclass
class Horse:
    name: str
    number_of_steps: int = 0
    step_probability: float = 0.0
    emoji: str = "🐎"
    selection_weight: int = 0

    def step(self) -> None:
        self.number_of_steps += 1

    def copy(self) -> Self:
        return Horse(
            name=self.name,
            number_of_steps=self.number_of_steps,
            step_probability=self.step_probability,
            emoji=self.emoji,
            selection_weight=self.selection_weight,
        )

    def position_string(
        self, steps_to_victory: int, race_track_character: str = "=",
    ) -> str:
        if steps_to_victory < 0:
            raise ValueError("steps_to_victory cannot be negative")
        if steps_to_victory < self.number_of_steps:
            raise ValueError(
                f"steps_to_victory must be less than {self.number_of_steps}"
            )

        characters = []
        num_of_characters = steps_to_victory + 1
        for i in range(num_of_characters):
            if i == self.number_of_steps:
                characters.append(self.emoji)
            else:
                characters.append(race_track_character)
            # elif i != 0:
            #     characters.append(race_track_character)

        position_string = " ".join(characters)
        return f"__{self.name}__\n" + position_string[::-1]


if __name__ == "__main__":
    horse = Horse()
    steps_to_victory = 7
    print(horse.position_string(steps_to_victory))
    for i in range(steps_to_victory):
        horse.step()
        print(horse.position_string(steps_to_victory))
