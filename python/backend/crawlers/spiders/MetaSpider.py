import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .core.item_parser import parse_item
from .core.ConstructorData import Scrapers
from .core.services import extract_domain


def construct_crawler(params):
    url = params.get('url')
    allowed_domains = [extract_domain(url)] # list with 1 element. Important
    name = allowed_domains[0].split('.')[0]

    rules = (
        Rule(LinkExtractor(restrict_css = params.get('pagination_css')), follow=True),
        Rule(LinkExtractor(restrict_css = params.get('post_css')), follow=True, callback='parse_item')
    )

    params['rules'] = rules
    params['allowed_domains'] = allowed_domains
    params['name'] = name
    params['parse_item'] = parse_item

    def start_requests(self):
        yield scrapy.Request(url=self.url)
    params['start_requests'] = start_requests

    return type(name, (CrawlSpider, ), params)


for i in Scrapers.rules.keys():
    exec(f'{i} = construct_crawler(Scrapers.get("{i}"))')