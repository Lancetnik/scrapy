from abc import ABC
from copy import deepcopy
from pathlib import Path
import json


RULES_PATH = Path(__file__).parent.joinpath('rules.json')


def add_required_arguments(func):
    def decor(self, name, **kwargs):
        kwargs['name'] = name
        difference = Scrapers.required_fields - set(kwargs.keys())
        if difference:
            raise TypeError(f'{func} missing {len(difference)} required positional argument(s): {difference}')
        return func(self, **kwargs)
    return decor


class Scrapers(ABC):
    with open(RULES_PATH) as j:
        rules = json.load(j)

    required_fields = {'name', 'url', 'post_css'}
    fields = set.union(*[set(j.keys()) for j in rules.values()]) - required_fields

    @classmethod
    def get(self, name):
        return deepcopy(self.rules.get(name))
   
    @classmethod
    @add_required_arguments
    def construct(self, name, **kwargs):
        self.rules[name] = {}
        for i, j in kwargs.items():
            self.rules[name][i] = j

    @classmethod
    def save(self):
        with open(RULES_PATH, 'w') as j:
            json.dump(self.rules, j, indent=4)



# smth = {
#         "url": "https://habr.com/ru/",
#         "pagination_css": "a.toggle-menu__item-link_pagination",
#         "post_css": "a.post__title_link",
#         "post_title": "span.post__title-text::text",
#         "post_likes": "span.voting-wjt__counter::text",
#         "post_bookmarks": "span.bookmark__counter::text",
#         "post_views": "span.post-stats__views-count::text",
#         "post_comments": "span.post-stats__comments-count::text",
#         "post_date": "span.post__time::text",
#         "post_tags": "a.inline-list__item-link::text",
#         "post_text": "div.post__body_full"
#     }
# Scrapers.construct('smth', **smth)
# Scrapers.save()