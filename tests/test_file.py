import io
import pathlib

import pytest

from awesome_lottery.file import File
from awesome_lottery.lottery import Lottery, Participant, Prizes, Prize


def test_reading_file_extension():
    file = File('what_a_path.json')
    assert file.file_extension == 'json'
    file = File('isThisAgoodPath/what_a_path.csv')
    assert file.file_extension == 'csv'
    file = File('what_a_path.exe')
    assert file.file_extension == 'exe'


def test_file():
    mock_input = io.StringIO('{"name": "test"}')

    lottery = File.load_lottery(mock_input)
    assert next(lottery) == {"name": "test"}
    with pytest.raises(StopIteration):
        next(lottery)


def test_read_json_participant_file():
    path = get_test_file_path('participant.json')
    file = File(path)
    rows = file.read_file(Participant)
    assert next(rows) == Participant(id=1, first_name='Tanny', last_name='Bransgrove', weight=1)
    with pytest.raises(StopIteration):
        next(rows)


def test_read_csv_participant_file():
    path = get_test_file_path('participant.csv')
    file = File(path)
    rows = file.read_file(Participant)
    assert next(rows) == Participant(id=1, first_name='Tanny', last_name='Bransgrove', weight=1)
    with pytest.raises(StopIteration):
        next(rows)


def test_read_json_rewards_file():
    path = get_test_file_path('rewards.json')
    file = File(path)
    rows = file.read_file(Prizes)
    assert next(rows) == Prizes(name='Item giveaway: 5 identical prizes',
                                prizes=[Prize(id=1, name='Annual Vim subscription', amount=5)],
                                OPENER_PREFIX='prize_')
    with pytest.raises(StopIteration):
        next(rows)


def get_test_file_path(file_name: str) -> str:
    return str(pathlib.Path(__file__).parent / 'test_resources' / file_name)

