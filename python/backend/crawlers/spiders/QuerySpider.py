import re

from scrapy import spiders

from .core import item_parser
from .core.ConstructorData import Scrapers


def construct_crawler(params):
    url = params.get('url')
    allowed_domains = [re.search(r'https://.*?/', url)[0].split('/')[-2]]
    name = "query_" + allowed_domains[0].split('.')[0]

    params['parse'] = item_parser.parse_item
    params['name'] = name
    params.pop('url')

    return type(name, (spiders.Spider, ), params)


for i in Scrapers.rules.keys():
    exec(f'str_{i} = construct_crawler(Scrapers.get("{i}"))')