from awesome_lottery.lottery import Prize, Winner, Lottery


def test_prizes_total_count(prizes):
    assert prizes.total_count == 3


def test_prizes_iter(prizes):
    prizes_list = list(prizes)
    assert prizes_list == [
        Prize(id=1, name='WE'),
        Prize(id=1, name='WE2', amount=2),
        Prize(id=1, name='WE2', amount=2)
    ]


def test_participant_win_chance_reduction(participants):
    for participant in participants:
        base_weight = participant.weight
        participant.reduce_win_chance()
        new_weight = participant.weight
        assert new_weight == base_weight - 1


def test_winner_to_str(participants, prizes):
    participant = participants.pop()
    prize = prizes.prizes.pop()
    winner = Winner(winner=participant, prize=prize)
    assert str(winner) == '-> Seba Prze won WE2'


def test_getting_winners_with_prizes(participants, prizes):
    lottery_data = Lottery(participants=participants, prizes=prizes)
    winners_with_prizes = lottery_data.get_winners_with_prizes()
    assert lottery_data.winners == winners_with_prizes



