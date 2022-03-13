import sys
from io import StringIO
from typing import TextIO, Optional

from awesome_lottery.lottery import Lottery, Winner


class ResultsWriter:
    lottery: Lottery
    output: TextIO

    def __init__(self, lottery: Lottery, output: Optional[StringIO] = None):
        self.lottery = lottery
        if output:
            self.output = output
        else:
            self.output = sys.stdout

    def display_results_in_console(self):
        results = 'Winners of lottery:\n'
        for winner in self.lottery.winners:
            results += str(winner) + '\n'
        results += 'Congratulations for winners!'
        print(results, file=self.output)

    def save_output_to_file(self, output: str):
        with open(output, 'w') as f:
            f.write(Winner.schema().dumps(self.lottery.winners, many=True))

    def dump(self, output: str):
        if output:
            self.save_output_to_file(output)
        else:
            self.display_results_in_console()
