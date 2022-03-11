import csv
import json
from pathlib import Path
import random
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from operator import attrgetter
from typing import Generator, Optional, TextIO
from io import StringIO

import sys
import click


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


class File:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path

    @staticmethod
    def load_lottery(file_object) -> Generator:
        x = json.load(file_object)
        yield x

    @property
    def file_extension(self) -> str:
        return Path(self.file_path).suffix[1:]

    def read_file(self, adapter_class, file_type: str = None) -> Generator:
        file_type = file_type or self.file_extension
        opener = OPENERS[adapter_class.OPENER_PREFIX + file_type]
        with open(self.file_path) as data_file:
            for x in opener(data_file):
                yield adapter_class.factory(x)

    @staticmethod
    def get_first_file_in_path(path: str) -> str:
        return str(next(Path(f"{path}/").iterdir()))


OPENERS = {
    "participant_csv": csv.DictReader,
    "participant_json": json.load,
    "prize_json": File.load_lottery,
}


class ResultsWriter:
    lottery: Lottery
    output: TextIO

    def __init__(self, lottery: Lottery, output: Optional[StringIO] = None):
        self.lottery = lottery
        if output:
            self.output = output
        else:
            self.output = sys.stdout

    def display_results_in_console(self):
        results = 'Winners of lottery:\n'
        for winner in self.lottery.winners:
            results += str(winner) + '\n'
        results += 'Congratulations for winners!'
        print(results, file=self.output)

    def save_output_to_file(self, output: str):
        with open(output, 'w') as f:
            f.write(Winner.schema().dumps(self.lottery.winners, many=True))

    def dump(self, output: str):
        if output:
            self.save_output_to_file(output)
        else:
            self.display_results_in_console()


def validate_file(ctx, param, value) -> str:
    if value:
        return value
    raise click.BadParameter('-- File not specified --')


def validate_rewards(ctx, param, value) -> str:
    if value:
        return value

    try:
        return File.get_first_file_in_path('data/lottery_templates')
    except FileNotFoundError:
        raise click.BadParameter("-- File doesn't exist --")


@click.command()
@click.option('--file', help='Provide file path to process',
              type=click.UNPROCESSED, callback=validate_file, prompt=True)
@click.option('--filetype', help='Provide file type csv/json', type=click.Choice(['csv', 'json'], case_sensitive=False))
@click.option('--rewards', help='Provide path for file with rewards',
              type=click.UNPROCESSED, callback=validate_rewards)
@click.option('--results', help='Provide filename to save results')
def main(file, filetype, rewards, results):  # pragma: no cover
    participant_file = File(file)
    rows = participant_file.read_file(Participant, filetype)
    participants = list(rows)

    prize_file = File(rewards)
    prizes_definition = next(prize_file.read_file(Prizes))

    lottery_data = Lottery(participants=participants, prizes=prizes_definition)
    lottery_data.get_winners_with_prizes()

    results_writer = ResultsWriter(lottery_data)
    results_writer.dump(results)


if __name__ == '__main__':  # pragma: no cover
    main()
