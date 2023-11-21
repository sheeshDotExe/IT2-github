import random

from .person import Gutt, Jente


class Lag:
    def __init__(self, gutter: list[Gutt], jenter: list[Jente]) -> None:
        self.antall_medlemmer = len(gutter) + len(jenter)
        self._gutter, self._jenter = gutter, jenter

        # definerer rekkefølgen laget skal løpe i
        self.rekkefølge = self._gutter + self._jenter
        random.shuffle(self.rekkefølge)
