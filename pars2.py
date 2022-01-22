import logging
import collections
import requests
import bs4
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('gd')

ParserResult = collections.namedtuple(
    'ParseResult',
    (
        'url',
        'title_name',
        'article_name',
        'city',
        'tag',
    ),
)

HEADERS = (
    'Ссылка',
    'Заголовок',
    'Статья',
    'Город',
    'Тэг',
)


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
            'Accept-Language': 'ru',
        }
        self.result = []

    def load_page(self, page: int = None, ):
        url = 'http://domen'
        res = self.session.get(url=url, verify=False)
        time.sleep(3)
        print('+++')


        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.news_item')
        for block in container:
            self.parse_block(block=block)


    def parse_block(self, block):
        url_block = block.select_one('p.title')
        url_block_all = url_block.select_one('a')
        if not url_block_all:
            logger.error('no url_block')
            return
        url = url_block_all.get('href')
        if not url:
            logger.error('no href')
            return

        title_block = url_block.select_one('a')

        if not title_block:
            logger.error(f'no title_block on {url}')
            return

        # Wrangler /
        title_block = title_block.text
        title_block = title_block.replace('/', '').strip()

        urll = f'http://domen/d{url}'

        if not url:
            logger.error('no href')
            return
        response = self.session.get(urll, verify=False)
        soup1 = bs4.BeautifulSoup(response.text, 'lxml')
        item = soup1.select_one('div.rightcol')

        get_content = item.select('p')


        for itm in get_content:
            itm = itm.text
            itm = itm.replace('/', '').strip()
            print(itm)

        city_name = 'Малая'
        tag_name = 'Власть'

        self.result.append(ParserResult(
            url=urll,
            title_name=title_block,
            article_name=itm,
            city=city_name,
            tag=tag_name
        ))

        logger.debug('%s, %s, %s', f'{url}', title_block, itm)
        logger.debug('=' * 100)

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)


def main():
    p = Client()
    p.run()


if __name__ == '__main__':
    main()
