import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .core.item_parser import parse_item
from .core.ConstructorData import Scrapers
from .core.services import extract_domain


def construct_crawler(params):
    url = params.get('url')
    allowed_domains = [extract_domain(url)] # list with 1 element. Important
    name = allowed_domains[0].lstrip('www.').split('.')[0]

    if params.get('post_css').get('type') == 'xpath':
        post_rule = LinkExtractor(restrict_xpaths = params.get('post_css').get('path'))
    elif params.get('post_css').get('type') == 'css':
        post_rule = LinkExtractor(restrict_css = params.get('post_css').get('path'))

    rules = [
        Rule(post_rule, follow=True, callback='parse_item')
    ]

    if params.get('pagination_css'):
        if params.get('pagination_css').get('type') == 'xpath':
            pagination_rule = LinkExtractor(restrict_xpaths = params.get('pagination_css').get('path'))
        elif params.get('pagination_css').get('type') == 'css':
            pagination_rule = LinkExtractor(restrict_css = params.get('pagination_css').get('path'))
        rules.append(Rule(pagination_rule, follow=True),)

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