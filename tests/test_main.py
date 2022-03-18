import copy
import io
import pathlib

import pytest

from awesome_lottery import __version__
from awesome_lottery import main
from awesome_lottery.file import File
from awesome_lottery.lottery import Participant

from awesome_lottery.result_writter import ResultsWriter


def test_version():
    assert __version__ == '0.1.0'


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
