import csv
import json
import random
import argparse


def read_file(file_path, file_type):
    with open(file_path) as data_file:
        if file_type == "csv":
            rows = read_csv_file(data_file)
        elif file_type == "json":
            rows = read_json_file(data_file)
    return rows


def read_json_file(data_file):
    rows = []  # nit: consider very big file with bilions of participants (for later)
    reader = json.load(data_file)
    for row in reader:
        rows.append([row.get('id'),
                     row.get('first_name'),
                     row.get('last_name'),
                     row.get('weight') or "1"])
    return rows


def read_csv_file(data_file):
    rows = []  # nit: consider very big file with bilions of participants (for later)
    reader = csv.reader(data_file)
    next(reader)
    for row in reader:
        rows.append(row)  # how do we know it is the same order as in JSON?
    return rows


def get_winners_with_weight(list_of_users, count):
    user_weights = []
    for i, user in enumerate(list_of_users):
        user_weights.append(int(user[3]))
    return random.choices(list_of_users, weights=user_weights, k=int(count))


def get_winners(list_of_users, count):
    return random.choices(list_of_users, k=int(count))


def show_winners(list_of_participants):
    winners = get_winners_with_weight(list_of_participants, winners_count)
    print("--- winners ---")
    for winner in winners:
        print(winner)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="Provide csv file path to process")
    parser.add_argument("--json", help="Provide json file path to process")
    args = parser.parse_args()

    winners_count = input("How many winners?")

    if args.csv is not None:
        list_of_users_from_csv = read_file(args.csv, 'csv')
        show_winners(list_of_users_from_csv)
    if args.json is not None:
        list_of_users_from_json = read_file(args.json, 'json')
        show_winners(list_of_users_from_json)
