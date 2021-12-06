import csv
import json


def read_file(file_path, file_type):
    print(f'File path -> {file_path}')
    print(f'File type -> {file_type}')
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
                rows.append([row.get('id'), row.get('first_name'), row.get('last_name')])
    data_file.close()
    print(rows)
    return rows


if __name__ == '__main__':
    read_file('data/participants1.csv', 'csv')
    read_file('data/participants1.json', 'json')
