from .person import Person, Gutt, Jente
from .lag import Lag

import random


class Idrettsklubb:
    def __init__(self) -> None:
        self.medlemmer: list[Person] = []
        self._jenter: list[Jente] = []
        self._gutter: list[Gutt] = []

    def legg_til_medlem(self, person: Person) -> None:
        self.medlemmer.append(person)
        if person.kjønn == "jente":
            self._jenter.append(person)
        elif person.kjønn == "gutt":
            self._gutter.append(person)

    def trekk_lag(self, lag_størrelse: int, antall_lag: int) -> list[Lag]:
        """Trekker ut tilfeldige lag

        Parameters
        ----------
        lag_st : _type_
            Størrelsen av hvert lag (må være partall slik at lagene blir rettferdige)
        antall_lag : int
            Hvor mange lag som skal trekkes

        Returns
        -------
        list[Lag]
        """
        assert (
            lag_størrelse % 2 == 0
        ), "Lag størrelse må være partall for rettferdige lag"

        assert lag_størrelse * antall_lag <= len(
            self.medlemmer
        ), "Har ikke nok spillere til å lage lagene"

        random.shuffle(self._jenter)
        random.shuffle(self._gutter)

        lag = []

        # trekker tilfeldige lag hvor 50% er gutter og 50% er jenter
        for x in range(0, (lag_størrelse // 2) * antall_lag, lag_størrelse // 2):
            lag.append(
                Lag(
                    self._gutter[x : x + lag_størrelse // 2],
                    self._jenter[x : x + lag_størrelse // 2],
                )
            )
        return lag
