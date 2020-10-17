from datetime import datetime, timedelta

from loguru import logger
import scrapy

from crawlers.items import HabrPostItem


class HabrSpider(scrapy.Spider):
    name = 'habr'

    start_urls = ['https://habr.com/ru/']

    def parse(self, response):
        for post in response.css('li.content-list__item_post'):
            post_title = post.css('a.post__title_link')
            if post_title:
                Item = HabrPostItem()
                Item['title'] = post_title.css('::text').get()
                Item['link'] = post_title.css('::attr(href)').get()

                Item['likes'] = int(post.css('span.post-stats__result-counter::text').get().lstrip('+'))
                Item['bookmarks'] = int(post.css('span.bookmark__counter::text').get())

                views = post.css('span.post-stats__views-count::text').get()
                Item['views'] = int(float(views.replace('k', '').replace(',', '.')) * 1000) if 'k' in views else int(views)

                Item['comments'] = int(post.css('span.post-stats__comments-count::text').get() or 0)

                Item['datetime'] = datetime.now().replace(second=0, microsecond=0)

                posted = post.css('span.post__time::text').get()
                if 'вчера' in posted:
                    posted = posted.replace('вчера в ', '').split(':')
                    now = datetime.now()
                    yesterday = now - timedelta(days=1)
                    Item['posted'] = now.replace(day=yesterday.day, hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)
                if 'сегодня' in posted:
                    posted = posted.replace('сегодня в ', '').split(':')
                    now = datetime.now()
                    Item['posted'] = now.replace(hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)

                yield scrapy.Request(url=Item['link'], callback=self.parse)
                Item['text'] = ''.join(response.css('div.post__text-html::text').getall())

                yield Item

        for next_page in response.css('a.toggle-menu__item-link_pagination'):
            yield response.follow(next_page, self.parse)