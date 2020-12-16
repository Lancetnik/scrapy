import copy

from loguru import logger

from django.conf import settings
from .models import HabrModel


class PostgresPipeline():
    def open_spider(self, spider):
        logger.debug(f'Run spider: {spider}')

    def close_spider(self, spider):
        logger.debug(f'{spider} finished')
    
    def process_item(self, item, spider):
        h = HabrModel.objects.get_or_create(link=item['link'], title=item['title'], posted=item['posted'])
        model, isCreated = copy.deepcopy(h[0]), h[1]
        if isCreated: 
            model.tags=item['tags']
            logger.info(f'Created - {model}')
        else:
            if len(model.datetime) >= settings.PARSER_COUNTER:
                return item
            logger.info(f'Updated - {model}')
        model.likes.append(item['likes'])
        model.bookmarks.append(item['bookmarks'])
        model.views.append(item['views'])
        model.datetime.append(item['datetime'])
        model.comments.append(item['comments'])
        model.save()
        return item