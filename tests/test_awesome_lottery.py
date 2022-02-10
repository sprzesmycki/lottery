import copy

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


def test_printing_winners(participants, prizes, winners):
    lottery_data = main.Lottery(participants=participants, prizes=prizes, winners=winners)
    assert lottery_data.get_lottery_results() == 'Winners of lottery:' \
                                                 '\n-> Seba Prze won WE2' \
                                                 '\n-> Seb Prz won WE' \
                                                 '\nCongratulations for winners!'


def test_reading_file_extension():
    file = main.File('what_a_path.json')
    assert file.file_extension == 'json'
    file = main.File('isThisAgoodPath/what_a_path.csv')
    assert file.file_extension == 'csv'
    file = main.File('what_a_path.exe')
    assert file.file_extension == 'exe'

