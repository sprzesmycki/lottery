import csv
import json


def read_file(file_path, file_type):
    print(f'File path -> {file_path}'). # try use logging module to not put it into stdout (or redirect ro stderr in print)
    print(f'File type -> {file_type}')
    rows = []  # nit: consider very big file with bilions of participants (for later)

    with open(file_path) as data_file:
        if file_type == "csv":  # everything what you have in `if` (as well as `else`) block should be a separate function
            reader = csv.reader(data_file)
            next(reader)
            for row in reader:
                rows.append(row)  # how do we know it is the same order as in JSON?
        elif file_type == "json":
            reader = json.load(data_file)
            for row in reader:
                rows.append([row.get('id'), row.get('first_name'), row.get('last_name')])
    data_file.close()  # when you use `with open` close() is not needed, with automatically closes the data_file
    print(rows)  # this print should be one level higher (function already returns it
    return rows


if __name__ == '__main__':
    read_file('data/participants1.csv', 'csv')  # use argparse or optparse modules to parametrize input
    read_file('data/participants1.json', 'json')
