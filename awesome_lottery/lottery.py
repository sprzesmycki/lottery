import random
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from operator import attrgetter
from typing import Generator


@dataclass_json
@dataclass
class Participant:
    id: int
    first_name: str
    last_name: str
    weight: int
    OPENER_PREFIX: str = 'participant_'

    def reduce_win_chance(self):
        self.weight = max(
            self.weight - 1,
            0
        )

    @staticmethod
    def factory(row: dict) -> "Participant":
        idk = int(row.get('id'))
        first_name = row.get('first_name')
        last_name = row.get('last_name')
        weight = int(row.get('weight') or 1)
        return Participant(idk, first_name, last_name, weight)


@dataclass_json
@dataclass
class Prize:
    id: int
    name: str
    amount: int = 1


@dataclass_json
@dataclass
class Prizes:
    name: str
    prizes: list[Prize]
    OPENER_PREFIX: str = 'prize_'

    @property
    def total_count(self) -> int:
        return sum(
            map(
                attrgetter('amount'),
                self.prizes
            )
        )

    def __iter__(self) -> Generator[Prize, None, None]:
        for prize in self.prizes:
            for _ in range(prize.amount):
                yield prize

    @staticmethod
    def factory(x: dict) -> "Prizes":
        prizes = []
        for z in x["prizes"]:
            prizes.append(Prize(**z))
        return Prizes(name=x["name"], prizes=prizes)


@dataclass_json
@dataclass
class Winner:
    winner: Participant
    prize: Prize

    def __str__(self) -> str:
        return f'-> {self.winner.first_name} {self.winner.last_name} won {self.prize.name}'


@dataclass_json
@dataclass
class Lottery:
    participants: list[Participant]
    prizes: Prizes
    winners: list[Winner] = field(default_factory=list)

    def get_winners_with_prizes(self) -> list[Winner]:
        for prize in self.prizes:
            self.winners.append(Winner(self.get_winner(), prize))
        return self.winners

    def get_winner(self) -> Participant:
        list_of_weights = list(map(attrgetter('weight'), self.participants))
        winner = random.choices(self.participants, weights=list_of_weights, k=1)[0]
        winner.reduce_win_chance()
        return winner
