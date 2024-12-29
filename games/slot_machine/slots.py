from dataclasses import dataclass

@dataclass
class SlotIcon:
    emoji: str
    weight: int


class Slots:
    def __init__(self, bet: int, slot_icons: list[SlotIcon]):
        self.bet = bet
        self.slot_icons = slot_icons

if __name__ == "__main__":
    slot_icons = [
        SlotIcon(emoji="🍒", weight=40),  # Cherry
        SlotIcon(emoji="🍋", weight=30),  # Lemon
        SlotIcon(emoji="🍊", weight=20),  # Orange
        SlotIcon(emoji="🍉", weight=10),  # Watermelon
        SlotIcon(emoji="⭐", weight=5),    # Star
        SlotIcon(emoji="💎", weight=1),   # Diamond
    ]