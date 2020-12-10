import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from .item_parser import parse_item


scrapers = {
    'habr': {
        'url': 'https://habr.com/ru/',
        'pagination_css': "a.toggle-menu__item-link_pagination",
        'post_css': "a.post__title_link",

        'post_title': 'span.post__title-text::text',
        'post_likes': 'span.voting-wjt__counter::text',
        'post_bookmarks': 'span.bookmark__counter::text',
        'post_views': 'span.post-stats__views-count::text',
        'post_comments': 'span.post-stats__comments-count::text',
        'post_date': 'span.post__time::text',
        'post_tags': 'a.inline-list__item-link::text',
        'post_text': 'div.post__body_full'
    }
}

def construct_crawler(params):
    url = params.get('url')
    allowed_domains = [re.search(r'https://.*?/', url)[0].split('/')[-2]]
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


a = construct_crawler(scrapers.get('habr'))