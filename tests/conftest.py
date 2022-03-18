import copy

import pytest

from awesome_lottery.lottery import Winner, Participant, Prize, Prizes


@pytest.fixture
def winners(participants, prizes):
    participants = participants.copy()
    prizes = copy.deepcopy(prizes)
    winners = [
        Winner(participants.pop(), prizes.prizes.pop()),
        Winner(participants.pop(), prizes.prizes.pop()),
    ]
    return winners


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
