import csv
import json
from collections.abc import Generator
from pathlib import Path


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