import copy
import io

import pytest

from awesome_lottery.lottery import Lottery, Prizes, Participant, Prize, Winner
from awesome_lottery.result_writter import ResultsWriter


@pytest.fixture
def participants():
    participants = [
        Participant(id=1, first_name='Seb', last_name='Prz', weight=1),
        Participant(id=2, first_name='Seba', last_name='Prze', weight=2)]
    return participants


@pytest.fixture
def prizes():
    prizes = Prizes(
        name='Hey',
        prizes=[
            Prize(id=1, name='WE'),
            Prize(id=1, name='WE2', amount=2)
        ]
    )
    return prizes


@pytest.fixture
def winners(participants, prizes):
    participants = participants.copy()
    prizes = copy.deepcopy(prizes)
    winners = [
        Winner(participants.pop(), prizes.prizes.pop()),
        Winner(participants.pop(), prizes.prizes.pop()),
    ]
    return winners


def test_result_writer_to_file(participants, prizes, winners):
    lottery_data = Lottery(participants=participants, prizes=prizes, winners=winners)
    ResultsWriter(lottery=lottery_data).dump('results.json')


def test_result_writer_to_console(participants, prizes, winners):
    temp_out = io.StringIO()
    lottery_data = Lottery(participants=participants, prizes=prizes, winners=winners)
    ResultsWriter(lottery=lottery_data, output=temp_out).dump(None)
    console_output = temp_out.getvalue()
    assert console_output == '''Winners of lottery:\n-> Seba Prze won WE2\n-> Seb Prz won WE\nCongratulations for winners!\n'''
