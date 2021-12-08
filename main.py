import csv
import json
import random
import argparse


def read_file(file_path, file_type):
    rows = []
    with open(file_path) as data_file:
        if file_type == "csv":
            reader = csv.reader(data_file)
            next(reader)
            for row in reader:
                rows.append(row)
        elif file_type == "json":
            reader = json.load(data_file)
            for row in reader:
                rows.append([row.get('id'),
                             row.get('first_name'),
                             row.get('last_name'),
                             row.get('weight') or "1"])
    return rows


def get_winners_with_weight(list_of_users, count):
    user_weights = []
    for i, user in enumerate(list_of_users):
        user_weights.append(int(user[3]))
    return random.choices(list_of_users, weights=user_weights, k=int(count))


def get_winners(list_of_users, count):
    return random.choices(list_of_users, k=int(count))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="Provide csv file path to process")
    parser.add_argument("--json", help="Provide json file path to process")
    args = parser.parse_args()

    list_of_users_from_csv = read_file('data/participants2.csv',
                                       'csv')  # use argparse or optparse modules to parametrize input
    list_of_users_from_json = read_file('data/participants2.json', 'json')

    winners_count = input("How many winners?")
    winners = get_winners_with_weight(list_of_users_from_csv, winners_count)
    print("--- csv winners with weights ---")
    for winner in winners:
        print(winner)

    winners = get_winners(list_of_users_from_json, winners_count)
    print("--- json winners without weights ---")
    for winner in winners:
        print(winner)
