import csv
import json
from pathlib import Path
import random
from dataclasses import dataclass
from typing import List
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
    prizes: List[Prize]

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


@dataclass_json
@dataclass
class Winners:
    winners: List[Participant]

    def __iter__(self):
        for participant in self.winners:
            for _ in range(participant.amount):
                yield participant

    def __str__(self):  # TODO not sure if this shouldn't be moved to lottery class??
        print('Winners of lottery: ')
        for winner in self.winners:
            print(f'-> {winner.participant.first_name} {winner.participant.last_name} won {winner.prize.name}')
        print('Congratulations for winners!')


@dataclass_json
@dataclass
class Lottery:
    participants: List[Participant]
    prizes: List[Prizes]
    winners: List[Participant]

    def get_winners(self):
        for i in range(self.prizes.total_count):
            winner = self.get_winner()
            self.winners.append(winner)
            winner.reduce_win_change()
        return self.winners

    def get_winners_with_prizes(self):  # TODO verify if this works
        yield zip(self.participants, self.prizes)

    def get_winner(self):
        list_of_weights = list(map(attrgetter('weight'), self.participants))
        return random.choices(self.participants, weights=list_of_weights, k=1)[0]


OPENERS = {
    "csv": csv.DictReader,
    "json": json.load,
}


def read_file(file_path, file_type):
    opener = OPENERS[file_type]
    with open(file_path) as data_file:
        yield from opener(data_file)


def iterate_participants(reader):  # TODO move it somehow to participant class
    for row in reader:
        idk = int(row.get('id'))
        first_name = row.get('first_name')
        last_name = row.get('last_name')
        weight = int(row.get('weight') or 1)
        yield Participant(idk, first_name, last_name, weight)


def get_extension(file):
    return Path(file).suffix[1:]


def get_first_file_in_path(path):
    return next(Path(f"{path}/").iterdir())


def validate_file(ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        return value
    except ValueError:
        raise click.BadParameter('-- File not specified --')


def validate_rewards(ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        return get_first_file_in_path('data/lottery_templates')
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
    filetype = filetype or get_extension(file)
    rows = read_file(file, filetype)
    participants = list(iterate_participants(rows))

    prizes = read_file(rewards, 'json')  # TODO saves results as dict - not sure how to convert this to json
    # rewards = Prizes.from_json(json.dumps(prizes)) TODO not working due to above ^ - worked when prizes were a full json

    # winners = get_winners(participants, rewards)

    # lottery_data = Lottery(participants=participants, prizes=prizes, winners=winners) TODO probably not needed due to all functions are within this class
    # lottery_json = Lottery.to_json(lottery_data)
    # print(lottery_json)
    # winners_with_prizes = get_winners_with_prizes(winners, rewards)

    # if results is None: # TODO move this to separate classes
    #     winners_with_prizes.print_winners()
    # else:
    #     with open(results, 'w') as f:
    #         f.write(Winners.to_json(winners_with_prizes))


if __name__ == '__main__':
    lottery()
