import io

from awesome_lottery.lottery import Lottery
from awesome_lottery.result_writter import ResultsWriter


def test_result_writer_to_file(participants, prizes, winners):
    lottery_data = Lottery(participants=participants, prizes=prizes, winners=winners)
    ResultsWriter(lottery=lottery_data).dump('results.json')


def test_result_writer_to_console(participants, prizes, winners):
    temp_out = io.StringIO()
    lottery_data = Lottery(participants=participants, prizes=prizes, winners=winners)
    ResultsWriter(lottery=lottery_data, output=temp_out).dump(None)
    console_output = temp_out.getvalue()
    assert console_output == '''Winners of lottery:\n-> Seba Prze won WE2\n-> Seb Prz won WE\nCongratulations for winners!\n'''
