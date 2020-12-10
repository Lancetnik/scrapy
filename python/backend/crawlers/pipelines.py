import copy

from loguru import logger

from .models import HabrModel


class PostgresPipeline():
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass
    
    @logger.catch
    def process_item(self, item, spider):
        h = HabrModel.objects.get_or_create(link=item['link'], title=item['title'], posted=item['posted'])
        model = copy.deepcopy(h[0])
        if h[1]: 
            model.tags=item['tags']
            logger.info(f'Created - {model}')
        else:
            logger.info(f'Updated - {model}')
        model.likes.append(item['likes'])
        model.bookmarks.append(item['bookmarks'])
        model.views.append(item['views'])
        model.datetime.append(item['datetime'])
        model.comments.append(item['comments'])
        model.save()
        return item