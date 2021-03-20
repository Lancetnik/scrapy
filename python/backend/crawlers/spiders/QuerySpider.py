from scrapy import spiders

from .core import item_parser
from .core.services import extract_domain
from .core.ConstructorData import Scrapers


def construct_crawler(params):
    url = params.get('url')
    allowed_domains = [extract_domain(url)] # list with 1 element. Important
    name = "query_" + allowed_domains[0].split('.')[0]

    params['parse'] = item_parser.parse_item
    params['name'] = name
    params.pop('url')

    return type(name, (spiders.Spider, ), params)


for i in Scrapers.rules.keys():
    exec(f'query_{i} = construct_crawler(Scrapers.get("{i}"))')