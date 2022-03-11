import copy
import io
import pathlib

import pytest

from awesome_lottery import __version__
from awesome_lottery import main


def test_version():
    assert __version__ == '0.1.0'


@pytest.fixture
def prizes():
    prizes = main.Prizes(
        name='Hey',
        prizes=[
            main.Prize(id=1, name='WE'),
            main.Prize(id=1, name='WE2', amount=2)
        ]
    )
    return prizes


def test_prizes_total_count(prizes):
    assert prizes.total_count == 3


def test_prizes_iter(prizes):
    prizes_list = list(prizes)
    assert prizes_list == [
        main.Prize(id=1, name='WE'),
        main.Prize(id=1, name='WE2', amount=2),
        main.Prize(id=1, name='WE2', amount=2)
    ]


@pytest.fixture
def participants():
    participants = [
        main.Participant(id=1, first_name='Seb', last_name='Prz', weight=1),
        main.Participant(id=2, first_name='Seba', last_name='Prze', weight=2)]
    return participants


def test_participant_win_chance_reduction(participants):
    for participant in participants:
        base_weight = participant.weight
        participant.reduce_win_chance()
        new_weight = participant.weight
        assert new_weight == base_weight - 1


def test_winner_to_str(participants, prizes):
    participant = participants.pop()
    prize = prizes.prizes.pop()
    winner = main.Winner(winner=participant, prize=prize)
    assert str(winner) == '-> Seba Prze won WE2'


def test_getting_winners_with_prizes(participants, prizes):
    lottery_data = main.Lottery(participants=participants, prizes=prizes)
    winners_with_prizes = lottery_data.get_winners_with_prizes()
    assert lottery_data.winners == winners_with_prizes


@pytest.fixture
def winners(participants, prizes):
    participants = participants.copy()
    prizes = copy.deepcopy(prizes)
    winners = [
        main.Winner(participants.pop(), prizes.prizes.pop()),
        main.Winner(participants.pop(), prizes.prizes.pop()),
    ]
    return winners


def test_reading_file_extension():
    file = main.File('what_a_path.json')
    assert file.file_extension == 'json'
    file = main.File('isThisAgoodPath/what_a_path.csv')
    assert file.file_extension == 'csv'
    file = main.File('what_a_path.exe')
    assert file.file_extension == 'exe'


def test_file():
    mockInput = io.StringIO('{"name": "test"}')

    lottery = main.File.load_lottery(mockInput)
    assert next(lottery) == {"name": "test"}
    with pytest.raises(StopIteration):
        next(lottery)


def test_read_json_participant_file():
    path = get_test_file_path('participant.json')
    file = main.File(path)
    rows = file.read_file(main.Participant)
    assert next(rows) == main.Participant(id=1, first_name='Tanny', last_name='Bransgrove', weight=1)
    with pytest.raises(StopIteration):
        next(rows)


def test_read_csv_participant_file():
    path = get_test_file_path('participant.csv')
    file = main.File(path)
    rows = file.read_file(main.Participant)
    assert next(rows) == main.Participant(id=1, first_name='Tanny', last_name='Bransgrove', weight=1)
    with pytest.raises(StopIteration):
        next(rows)


def test_read_json_rewards_file():
    path = get_test_file_path('rewards.json')
    file = main.File(path)
    rows = file.read_file(main.Prizes)
    assert next(rows) == main.Prizes(name='Item giveaway: 5 identical prizes',
                                     prizes=[main.Prize(id=1, name='Annual Vim subscription', amount=5)],
                                     OPENER_PREFIX='prize_')
    with pytest.raises(StopIteration):
        next(rows)


def test_validate_file():
    value = 'participant.csv'
    assert main.validate_file('', '', value) == value


def test_validate_file_exception():
    with pytest.raises(Exception):
        main.validate_file('', '', '')


def test_validate_rewards():
    value = 'participant.csv'
    assert main.validate_rewards('', '', value) == value


def test_validate_rewards_exception():
    with pytest.raises(main.click.BadParameter):
        main.validate_rewards('', '', '')


def get_test_file_path(file_name: str) -> str:
    return str(pathlib.Path(__file__).parent / 'test_resources' / file_name)


def test_result_writer_to_file(participants, prizes, winners):  # todo fails
    lottery_data = main.Lottery(participants=participants, prizes=prizes, winners=winners)
    main.ResultsWriter(lottery=lottery_data).dump('results.json')


def test_result_writer_to_console(participants, prizes, winners):
    temp_out = io.StringIO()
    lottery_data = main.Lottery(participants=participants, prizes=prizes, winners=winners)
    main.ResultsWriter(lottery=lottery_data, output=temp_out).dump(None)
    console_output = temp_out.getvalue()
    assert console_output == '''Winners of lottery:\n-> Seba Prze won WE2\n-> Seb Prz won WE\nCongratulations for winners!\n'''
