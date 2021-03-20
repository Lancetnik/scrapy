from datetime import datetime, timedelta

from bs4 import BeautifulSoup as BS

from crawlers.items import PostItem
from .services import to_datetime

from loguru import logger
def parse_item(self, response):
    Item = PostItem()
    dictionary = self.crawler.spidercls.__dict__

    Item['link'] = response.url
    Item['id'] = response.url.split('/')[-2]
    Item['datetime'] = datetime.now().replace(second=0, microsecond=0)

    Item['title'] = _get_token(response, dictionary, 'post_title')
    Item['bookmarks'] = int(_get_token(response, dictionary, 'post_bookmarks') or 0)
    Item['comments'] = int(_get_token(response, dictionary, 'post_comments') or 0)

    tags = _get_all_tokens(response, dictionary, 'post_tags')
    if tags: Item['tags'] = list(set(i.strip() for i in tags))

    views = _get_token(response, dictionary, 'post_views')
    if views:
        views = views.lstrip('UserPageVisits:')
        Item['views'] = int(float(views.replace('k', '').replace(',', '.')) * 1000) if 'k' in views else int(views)

    likes = _get_token(response, dictionary, 'post_likes')
    if likes:
        likes = likes.lstrip('+').strip()
        likes = likes.replace('–', '-')
        Item['likes'] = int(likes)

    unlikes = _get_token(response, dictionary, 'post_unlikes')
    if unlikes:
        unlikes = unlikes.lstrip('-').strip()
        Item['likes'] -= int(unlikes)

    text = _get_token(response, dictionary, 'post_text')
    if text: Item['text'] = BS(text, features="lxml").text

    posted = _get_token(response, dictionary, 'post_date_modified') or _get_token(response, dictionary, 'post_date')
    if posted:
        try:
            Item['posted'] = datetime.strptime(posted, "%Y-%m-%dT%H:%M:%S%z")
        except Exception:
            posted = posted.replace('Создано: ', '')
            posted = posted.replace('Обновлено: ', '')
            if 'вчера' in posted.lower():
                posted = posted.replace('вчера в ', '').split(':')
                now = datetime.now()
                yesterday = now - timedelta(days=1)
                Item['posted'] = now.replace(day=yesterday.day, hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)
            elif 'сегодня' in posted.lower():
                posted = posted.replace('сегодня в ', '').split(':')
                now = datetime.now()
                Item['posted'] = now.replace(hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)
            else:
                Item['posted'] = to_datetime(posted)

    yield Item
    

def _check_parsing_type(response, dictionary, item):
    a = dictionary.get(item)
    if a is None: return None
    if a['type'] == 'css':
        return response.css(a['path'])
    elif a['type'] == 'xpath': 
        return response.xpath(a['path'])

def _get_token(response, dictionary, item):
    a = _check_parsing_type(response, dictionary, item)
    if a:
        return a.get()

def _get_all_tokens(response, dictionary, item):
    a = _check_parsing_type(response, dictionary, item)
    if a:
        return a.getall()