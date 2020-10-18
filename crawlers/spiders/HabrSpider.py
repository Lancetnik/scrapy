from datetime import datetime, timedelta

from bs4 import BeautifulSoup as BS
from loguru import logger
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawlers.items import HabrPostItem


class HabrSpider(CrawlSpider):
    name = 'habr'
    allowed_domains = ['habr.com']


    def start_requests(self):
        yield scrapy.Request(url='https://habr.com/ru/')

    rules = (
        Rule(LinkExtractor(restrict_css ='a.toggle-menu__item-link_pagination'), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//h2[@class='post__title']/a"), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        Item = HabrPostItem()

        Item['title'] = response.css('span.post__title-text::text').get()
        Item['link'] = response.url
        Item['id'] = response.url.split('/')[-2]

        Item['likes'] = int(response.css('span.voting-wjt__counter::text').get().lstrip('+'))
        Item['bookmarks'] = int(response.css('span.bookmark__counter::text').get())

        views = response.css('span.post-stats__views-count::text').get()
        Item['views'] = int(float(views.replace('k', '').replace(',', '.')) * 1000) if 'k' in views else int(views)

        Item['comments'] = int(response.css('span.post-stats__comments-count::text').get() or 0)

        Item['datetime'] = datetime.now().replace(second=0, microsecond=0)

        posted = response.css('span.post__time::text').get()
        if 'вчера' in posted:
            posted = posted.replace('вчера в ', '').split(':')
            now = datetime.now()
            yesterday = now - timedelta(days=1)
            Item['posted'] = now.replace(day=yesterday.day, hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)
        if 'сегодня' in posted:
            posted = posted.replace('сегодня в ', '').split(':')
            now = datetime.now()
            Item['posted'] = now.replace(hour=int(posted[0]), minute=int(posted[1]), second=0, microsecond=0)
        
        Item['text'] = BS(response.xpath('//*[@id="post-content-body"]').get(), features="lxml").text
        Item['tags'] = list(set(i.strip() for i in response.css('a.inline-list__item-link::text').getall()))

        yield Item

