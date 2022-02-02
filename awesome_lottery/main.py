import csv
import json
from pathlib import Path
import random
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from operator import attrgetter

import click


@dataclass
class Participant:
    id: int
    first_name: str
    last_name: str
    weight: int

    def reduce_win_change(self):
        self.weight = max(
            self.weight - 1,
            0
        )

    @staticmethod
    def factory(row):
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
    amount: 1


@dataclass_json
@dataclass
class Prizes:
    name: str
    prizes: list[Prize]

    @property
    def total_count(self) -> int:
        return sum(
            map(
                attrgetter('amount'),
                self.prizes
            )
        )

    def __iter__(self):
        for prize in self.prizes:
            for _ in range(prize.amount):
                yield prize

    @staticmethod
    def factory(x):
        prizes = []
        for z in x["prizes"]:
            prizes.append(Prize(**z))
        return Prizes(name=x["name"], prizes=prizes)


@dataclass
class Winner:
    winner: Participant
    prize: Prize

    def __str__(self):
        return f'-> {self.winner.first_name} {self.winner.last_name} won {self.prize.name}'


@dataclass_json
@dataclass
class Lottery:
    participants: list[Participant]
    prizes: Prizes
    winners: list[Winner] = field(default_factory=list)

    def get_winners_with_prizes(self):
        for prize in self.prizes:
            self.winners.append(Winner(self.get_winner(), prize))
        return self.winners

    def get_winner(self):
        list_of_weights = list(map(attrgetter('weight'), self.participants))
        winner = random.choices(self.participants, weights=list_of_weights, k=1)[0]
        winner.reduce_win_change()
        return winner

    def print_winners(self):
        print('Winners of lottery: ')
        for winner in self.winners:
            print(winner)
        print('Congratulations for winners!')


class File:

    file_path: str

    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def load_lottery(file_object):
        x = json.load(file_object)
        yield x

    @property
    def file_extension(self) -> str:
        return Path(self.file_path).suffix[1:]

    def read_file(self, opener, adapter):
        opener = self.OPENERS[opener]
        with open(self.file_path) as data_file:
            for x in opener(data_file):
                yield adapter(x)

    OPENERS = {
        "participant_csv": csv.DictReader,
        "participant_json": json.load,
        "prize_json": load_lottery,
    }

    @staticmethod
    def get_first_file_in_path(path):
        return next(Path(f"{path}/").iterdir())


class ResultsWriter:
    def __init__(self):
        pass
    # create object of that file
    # save lottery results
    # method for displaying


def validate_file(ctx, param, value):
    if value:
        return value
    raise click.BadParameter('-- File not specified --')


def validate_rewards(ctx, param, value):
    if value:
        return value

    try:
        return File.get_first_file_in_path('data/lottery_templates')
    except ValueError:
        raise click.BadParameter("-- File doesn't exist --")


@click.command()
@click.option('--file', help='Provide file path to process',
              type=click.UNPROCESSED, callback=validate_file, prompt=True)
@click.option('--filetype', help='Provide file type csv/json', type=click.Choice(['csv', 'json'], case_sensitive=False))
@click.option('--rewards', help='Provide path for file with rewards',
              type=click.UNPROCESSED, callback=validate_rewards)
@click.option('--results', help='Provide filename to save results')
def lottery(file, filetype, rewards, results):
    participant_file = File(file)
    participant_filetype = filetype or participant_file.file_extension
    rows = participant_file.read_file('participant_' + participant_filetype, Participant.factory)
    participants = list(rows)

    prize_file = File(rewards)
    prizes_definition = next(prize_file.read_file('prize_' + prize_file.file_extension, Prizes.factory))

    #    prizes_definition = next(read_file(rewards, 'prize_json', Prizes.factory))

    lottery_data = Lottery(participants=participants, prizes=prizes_definition)

    lottery_data.get_winners_with_prizes()

    if results is None:  # TODO move this to separate classes
        lottery_data.print_winners()
    # else:
    #     with open(results, 'w') as f:
    #         f.write(Winners.to_json(winners_with_prizes))


if __name__ == '__main__':
    lottery()
