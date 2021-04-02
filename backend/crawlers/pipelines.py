import copy
from datetime import datetime, timedelta

from bs4 import BeautifulSoup as BS

from scrapy.exceptions import DropItem
from django.core.files.base import ContentFile, File

from loguru import logger

from django.conf import settings
from posts.models import PostModel

from .spiders.core.services import extract_domain, to_datetime
from posts.annotation import get_popular_words


class PreprocessPipeline():
    def __init__(self):
        self.urls = set()

    def open_spider(self, spider): pass

    def close_spider(self, spider): pass

    @logger.catch
    def process_item(self, item, spider):
        if item['link'] in self.urls:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.urls.add(item['link'])

        if item.get('views'):
            views = item.get('views').lstrip('UserPageVisits:')
            item['views'] = int(float(views.replace('k', '').replace(',', '.')) * 1000) if 'k' in views else int(views)
        
        if item.get('likes'):
            likes = item.get('likes').lstrip('+').strip()
            likes = likes.replace('–', '-')
            item['likes'] = int(likes)
        
        if item.get('unlikes'):
            unlikes = item.get('unlikes').lstrip('-').strip()
            item['likes'] -= int(unlikes)
        
        for i in BS(item['text']).find_all('img'):
            if i.get('src'):
                if not i['src'].startswith('http'):
                    address = spider.url.split('/')
                    address = address[0] + '//' + address[2]
                    item['text'] = item['text'].replace(i['src'], address + i['src'])
        
        text = BS(item.get('text'), features="lxml").text
        words = list(set(get_popular_words(text)))
        if item.get('tags'):
            words += list(set(i.strip().lower() for i in item.get('tags')))
        item['tags'] = words

        if item.get('posted'):
            try:
                item['posted'] = datetime.strptime(item.get('posted'), "%Y-%m-%dT%H:%M:%S%z")
            except Exception:
                posted = item.get('posted').replace('Создано: ', '')
                posted = posted.replace('Обновлено: ', '')
                if 'вчера' in posted.lower():
                    posted = posted.replace('вчера в ', '').split(':')
                    now = datetime.now()
                    yesterday = now - timedelta(days=1)
                    item['posted'] = now.replace(day=yesterday.day, hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)

                elif 'сегодня' in posted.lower():
                    posted = posted.replace('сегодня в ', '').split(':')
                    now = datetime.now()
                    item['posted'] = now.replace(hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)

                else:
                    item['posted'] = to_datetime(posted)
        
        return item


class PostgresPipeline():
    def open_spider(self, spider):
        logger.success(f'Run spider: {spider.name.upper()}')

    def close_spider(self, spider):
        logger.success(f'{spider.name.upper()} finished!')
        logger.success(f'Scraped: {len(self.urls)} items.')
    
    def process_item(self, item, spider):
        source = extract_domain(item['link'])
        h = PostModel.objects.get_or_create(
            link=item['link'], title=item['title'],
            posted=item['posted'], text=item['text'],
            source=source
        )
        model, isCreated = copy.deepcopy(h[0]), h[1]
        if isCreated:
            model.tags = item.get('tags')
            logger.info(f'Created - {model}')
        else:
            if len(model.datetime) >= settings.PARSER_COUNTER:
                return item
            logger.info(f'Updated - {model}')
        model.likes.append(item.get('likes'))
        model.bookmarks.append(item.get('bookmarks'))
        model.views.append(item.get('views'))
        model.datetime.append(item.get('datetime'))
        model.comments.append(item.get('comments'))
        model.save()
        return item