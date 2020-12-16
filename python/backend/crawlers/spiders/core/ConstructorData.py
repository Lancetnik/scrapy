from copy import deepcopy
from pathlib import Path
import json


class Scrapers:
    with open(Path(__file__).parent.joinpath('rules.json')) as j:
        rules = json.load(j)

    @classmethod
    def get(self, name):
        return deepcopy(self.rules.get(name))
