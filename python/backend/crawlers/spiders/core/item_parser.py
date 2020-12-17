from datetime import datetime, timedelta

from bs4 import BeautifulSoup as BS

from crawlers.items import PostItem
from .services import to_datetime


def parse_item(self, response):
    Item = PostItem()

    Item['title'] = response.css(self.post_title).get()
    Item['link'] = response.url
    Item['id'] = response.url.split('/')[-2]

    like = response.css(self.post_likes).get().replace('–', '-')
    Item['likes'] = int(like)

    Item['bookmarks'] = int(response.css(self.post_bookmarks).get())

    views = response.css(self.post_views).get()
    Item['views'] = int(float(views.replace('k', '').replace(',', '.')) * 1000) if 'k' in views else int(views)

    Item['comments'] = int(response.css(self.post_comments).get() or 0)

    Item['datetime'] = datetime.now().replace(second=0, microsecond=0)

    posted = response.css(self.post_date).get()
    if 'вчера' in posted:
        posted = posted.replace('вчера в ', '').split(':')
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        Item['posted'] = now.replace(day=yesterday.day, hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)
    elif 'сегодня' in posted:
        posted = posted.replace('сегодня в ', '').split(':')
        now = datetime.now()
        Item['posted'] = now.replace(hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)
    else:
        Item['posted'] = to_datetime(posted)
    
    Item['text'] = BS(response.css(self.post_text).get(), features="lxml").text
    Item['tags'] = list(set(i.strip() for i in response.css(self.post_tags).getall()))
    
    yield Item