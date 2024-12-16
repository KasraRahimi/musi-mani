from dataclasses import dataclass

@dataclass
class Horse:
    number_of_steps: int = 0
    step_probability: float = 0.0
    emoji: str = "🐎"

    def step(self) -> None:
        self.number_of_steps += 1

    def position_string(self, steps_to_victory: int, race_track_character: str = "=") -> str:
        if steps_to_victory < 0:
            raise ValueError("steps_to_victory cannot be negative")
        if steps_to_victory < self.number_of_steps:
            raise ValueError(f"steps_to_victory must be less than {self.number_of_steps}")

        characters = []
        num_of_characters = steps_to_victory + 1
        for i in range(num_of_characters):
            if i == self.number_of_steps:
                characters.append(self.emoji)
            else:
                characters.append(race_track_character)

        position_string = " ".join(characters)
        return position_string[::-1]

if __name__ == "__main__":
    horse = Horse()
    steps_to_victory = 7
    print(horse.position_string(steps_to_victory))
    for i in range(steps_to_victory):
        horse.step()
        print(horse.position_string(steps_to_victory))