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
    reader = csv.DictReader(data_file)
    for row in reader:
        rows.append([row.get('id'),
                     row.get('first_name'),
                     row.get('last_name'),
                     row.get('weight') or "1"])
    return rows


def get_winner_and_reduce_his_chances(list_of_users):
    winner = random.choices(list_of_users, weights=user_weights, k=1)
    reduce_winner_chances(winner)
    return winner


def reduce_winner_chances(winner):
    winner_id = int(winner[0][0])
    user_weights[winner_id-1] -= 1


def show_winners(list_of_participants):
    for i, user in enumerate(list_of_participants):
        user_weights.append(int(user[3]))
    winners = []
    for i in range(int(winners_count)):
        winners.append(get_winner_and_reduce_his_chances(list_of_participants))
    print("--- winners ---")
    for winner in winners:
        print(winner)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="Provide csv file path to process")
    parser.add_argument("--json", help="Provide json file path to process")
    args = parser.parse_args()

    user_weights = []
    winners_count = input("How many winners?")

    if args.csv is not None:
        list_of_users_from_csv = read_file(args.csv, 'csv')
        show_winners(list_of_users_from_csv)
    if args.json is not None:
        list_of_users_from_json = read_file(args.json, 'json')
        show_winners(list_of_users_from_json)
