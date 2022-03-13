import click

from awesome_lottery.result_writter import ResultsWriter
from awesome_lottery.file import File
from awesome_lottery.lottery import Lottery, Participant, Prizes


def validate_file(ctx, param, value) -> str:
    if value:
        return value
    raise click.BadParameter('-- File not specified --')


def validate_rewards(ctx, param, value) -> str:
    if value:
        return value

    try:
        return File.get_first_file_in_path('data/lottery_templates')
    except FileNotFoundError:
        raise click.BadParameter("-- File doesn't exist --")


@click.command()
@click.option('--file', help='Provide file path to process',
              type=click.UNPROCESSED, callback=validate_file, prompt=True)
@click.option('--filetype', help='Provide file type csv/json', type=click.Choice(['csv', 'json'], case_sensitive=False))
@click.option('--rewards', help='Provide path for file with rewards',
              type=click.UNPROCESSED, callback=validate_rewards)
@click.option('--results', help='Provide filename to save results')
def main(file, filetype, rewards, results):  # pragma: no cover
    participant_file = File(file)
    rows = participant_file.read_file(Participant, filetype)
    participants = list(rows)

    prize_file = File(rewards)
    prizes_definition = next(prize_file.read_file(Prizes))

    lottery_data = Lottery(participants=participants, prizes=prizes_definition)
    lottery_data.get_winners_with_prizes()

    results_writer = ResultsWriter(lottery_data)
    results_writer.dump(results)


if __name__ == '__main__':  # pragma: no cover
    main()
