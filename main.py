import logging
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import EXPECTED_STATUS, PEP_URL
from outputs import file_output
from utils import find_tag, get_response


result_of_status = {}


def pep(session):
    pep_url = PEP_URL
    response = get_response(session, pep_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    result = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tag_abbr = result.find_all('abbr')
    for tag in tqdm(tag_abbr):
        status = tag.text[1:]
        sibling = tag.parent.find_next_sibling()
        tag_a = find_tag(sibling, 'a')
        link = tag_a['href']
        one_page(session, status, link)
    result_of_status['total'] = sum(result_of_status.values())
    return result_of_status


def one_page(session, status, link):
    logging.info('Парс одной страницы.')
    url_link = urljoin(PEP_URL, link)
    response = get_response(session, url_link)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    result = soup.find(string='Status')
    status_sibling = result.parent.next_sibling.next_sibling.text
    if status_sibling not in result_of_status:
        result_of_status[status_sibling] = 0
    result_of_status[status_sibling] += 1
    if status_sibling not in EXPECTED_STATUS.get(status):
        logging.warn(
            f'Несовпадающие статусы: {url_link}'
            f'Статус в карточке: {status_sibling}'
            f'Ожидаемые статусы: {EXPECTED_STATUS[status]}'
        )
    return


MODE_TO_FUNCTION = {
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Старт парсера.')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        file_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
