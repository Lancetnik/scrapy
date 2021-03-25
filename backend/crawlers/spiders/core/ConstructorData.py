from abc import ABC
from copy import deepcopy
from pathlib import Path
import json


RULES_PATH = Path(__file__).parent.joinpath('rules.json')
REQUIRED_FIELDS = {'name', 'url', 'post_css'}


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

    required_fields = REQUIRED_FIELDS
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