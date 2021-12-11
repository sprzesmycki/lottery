import csv
import json
import pathlib
import random
from dataclasses import dataclass

import click


@dataclass
class Participant:
    id: int
    first_name: str
    last_name: str
    weight: int


def read_file(file_path, file_type):
    with open(file_path) as data_file:
        if file_type == "csv":
            yield from read_csv_file(data_file)
        elif file_type == "json":
            yield from read_json_file(data_file)


def read_json_file(data_file):
    reader = json.load(data_file)
    yield from iterate_participants(reader)


def read_csv_file(data_file):
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
    print(list_of_weights)
    return random.choices(list_of_users, weights=list_of_weights, k=1)[0]


def reduce_winner_chances(winner):
    winner.weight -= 1


def show_winners(list_of_winners):
    print("--- winners ---")
    for winner in list_of_winners:
        print(winner)


def get_extension(file):
    return pathlib.Path(file).suffix[1:]


def get_list_of_participants(participants):
    list_of_participants = []
    it = iter(participants)
    while True:
        try:
            list_of_participants.append(next(it))
        except StopIteration:
            break
    return list_of_participants


@click.command()
@click.option('--file', help='Provide file path to process')
@click.option('--filetype', help='Provide file type csv/json')
@click.option('--count', prompt='Winners count:', default=1, help='Provide winners count')
def lottery(file, filetype, count):
    participants = []
    if file is not None:
        filetype = filetype or get_extension(file)
        participants = read_file(file, filetype)
    else:
        print('Please specify the file')
    participants = get_list_of_participants(participants)

    winners = []
    for i in range(count):
        winner = get_winner(participants)
        winners.append(winner)
        reduce_winner_chances(winner)

    show_winners(winners)


if __name__ == '__main__':
    lottery()
