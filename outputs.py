import datetime as dt
import logging

from constants import BASE_DIR, DATETIME_FORMAT


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        for key in results.keys():
            f.write("%s, %s\n" % (key, results[key]))
    logging.info(f'Файл с результатами был сохранён: {file_path}')
