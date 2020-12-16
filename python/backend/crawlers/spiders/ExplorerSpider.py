from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from loguru import logger


class FollowAllSpider(CrawlSpider):
    name = 'explorer'
    rules = [Rule(LinkExtractor(), callback='parse_item', follow=True)]

    def parse_item(self, response):
        logger.debug(response)