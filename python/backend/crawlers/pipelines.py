import copy

from loguru import logger

from django.conf import settings
from posts.models import PostModel

from .spiders.core.services import extract_domain


class PostgresPipeline():
    def open_spider(self, spider):
        logger.success(f'Run spider: {spider}')

    def close_spider(self, spider):
        logger.success(f'{spider} finished')
    
    def process_item(self, item, spider):
        source = extract_domain(item['link'])
        h = PostModel.objects.get_or_create(
            link=item['link'], title=item['title'],
            posted=item['posted'], source=source
        )
        model, isCreated = copy.deepcopy(h[0]), h[1]
        if isCreated: 
            model.tags=item.get('tags')
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