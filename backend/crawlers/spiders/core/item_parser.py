from datetime import datetime

from crawlers.items import PostItem


def parse_item(self, response):
    Item = PostItem()
    dictionary = self.crawler.spidercls.__dict__

    Item['link'] = response.url
    Item['id'] = response.url.split('/')[-2]
    Item['datetime'] = datetime.now().replace(second=0, microsecond=0)

    Item['title'] = _get_token(response, dictionary, 'post_title')
    Item['bookmarks'] = int(_get_token(response, dictionary, 'post_bookmarks') or 0)
    Item['comments'] = int(_get_token(response, dictionary, 'post_comments') or 0)

    Item['views']  = _get_token(response, dictionary, 'post_views')
    Item['likes'] = _get_token(response, dictionary, 'post_likes')
    Item['unlikes'] = _get_token(response, dictionary, 'post_unlikes')
    Item['text']  = _get_token(response, dictionary, 'post_text')
    Item['tags'] = _get_all_tokens(response, dictionary, 'post_tags')
    Item['posted'] = _get_token(response, dictionary, 'post_date_modified') or _get_token(response, dictionary, 'post_date')

    yield Item
    

def _check_parsing_type(response, dictionary, item):
    a = dictionary.get(item)
    if a is None: return None
    if a['type'] == 'css':
        return response.css(a['path'])
    elif a['type'] == 'xpath': 
        return response.xpath(a['path'])

def _get_token(response, dictionary, item):
    a = _check_parsing_type(response, dictionary, item)
    if a:
        return a.get()

def _get_all_tokens(response, dictionary, item):
    a = _check_parsing_type(response, dictionary, item)
    if a:
        return a.getall()