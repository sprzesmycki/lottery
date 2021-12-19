import csv
import json
from pathlib import Path
import random
from dataclasses import dataclass

from dataclasses_json import dataclass_json

import click


@dataclass
class Participant:
    id: int
    first_name: str
    last_name: str
    weight: int


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
    total_count: int = 0

    def get_prizes_count(self):
        for i in self.prizes:
            self.total_count += i.amount
        return self.total_count

    def get_next_prize(self):
        for i in self.prizes:
            if i.amount > 0:
                i.amount -= 1
                return i


@dataclass_json
@dataclass
class Winner:
    first_name: str
    last_name: str
    prize: str


@dataclass_json
@dataclass
class Winners:
    winners: list[Winner]

    def print_winners(self):
        print('Winners of lottery: ')
        for winner in self.winners:
            print(f'-> {winner.first_name} {winner.last_name} won {winner.prize}')
        print('Congratulations for winners!')


@dataclass_json
@dataclass
class Lottery:
    participants: list[Participant]
    prizes: list[Prizes]
    winners: list[Winner]


def read_file(file_path, file_type):
    with open(file_path) as data_file:
        if file_type == "csv":
            return csv.DictReader(data_file)
        elif file_type == "json":
            return json.load(data_file)


def read_participants_file(file_path, file_type):
    with open(file_path) as data_file:
        if file_type == "csv":
            yield from read_participants_csv_file(data_file)
        elif file_type == "json":
            yield from read_participants_json_file(data_file)


def read_participants_json_file(data_file):
    reader = json.load(data_file)
    yield from iterate_participants(reader)


def read_participants_csv_file(data_file):
    reader = csv.DictReader(data_file)
    yield from iterate_participants(reader)


def iterate_participants(reader):
    for row in reader:
        weight = row.get('weight')
        if weight is None:
            weight = 1
        else:
            weight = int(weight)
        yield Participant(int(row.get('id')),
                          row.get('first_name'),
                          row.get('last_name'),
                          weight)


def get_winner(list_of_users):
    list_of_weights = list(map(lambda user: user.weight, list_of_users))
    return random.choices(list_of_users, weights=list_of_weights, k=1)[0]


def reduce_winner_chances(winner):
    winner.weight -= 1


def get_extension(file):
    return Path(file).suffix[1:]


def get_list_of_participants(participants):
    list_of_participants = []
    it = iter(participants)
    while True:
        try:
            list_of_participants.append(next(it))
        except StopIteration:
            break
    return list_of_participants


def get_winners_with_prizes(winners, prizes: Prizes):
    list_of_winners_with_prizes = []
    for winner in winners:
        list_of_winners_with_prizes.append(
            Winner(first_name=winner.first_name, last_name=winner.last_name, prize=prizes.get_next_prize().name))
    return Winners(winners=list_of_winners_with_prizes)


def get_first_file_in_path(path):
    return next(Path(f"{path}/").iterdir())


@click.command()
@click.option('--file', help='Provide file path to process')
@click.option('--filetype', help='Provide file type csv/json')
@click.option('--rewards', help='Provide path for file with rewards')
@click.option('--results', help='Provide filename to save results')
def lottery(file, filetype, rewards, results):
    participants = []
    if file is not None:
        filetype = filetype or get_extension(file)
        participants = read_participants_file(file, filetype)
    else:
        print('-- File not specified --')
        exit()
    participants = get_list_of_participants(participants)

    if rewards is None:
        rewards = get_first_file_in_path('data/lottery_templates')
    prizes = read_file(rewards, 'json')
    rewards = Prizes.from_json(json.dumps(prizes))

    winners = []
    for i in range(rewards.get_prizes_count()):
        winner = get_winner(participants)
        winners.append(winner)
        reduce_winner_chances(winner)

    lottery_data = Lottery(participants=participants, prizes=prizes, winners=winners)
    lottery_json = Lottery.to_json(lottery_data)
    print(lottery_json)
    winners_with_prizes = get_winners_with_prizes(winners, rewards)

    if results is None:
        winners_with_prizes.print_winners()
    else:
        with open(results, 'w') as f:
            f.write(Winners.to_json(winners_with_prizes))


if __name__ == '__main__':
    lottery()
