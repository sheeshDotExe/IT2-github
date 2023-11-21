from typing import Optional, Literal
import random
import numpy as np

Kjønn = Literal["gutt", "jente", "udefinert"]


class Person:
    """Standardklasse for person"""

    def __init__(self, hastighet: float) -> None:
        self.kjønn: Kjønn = "udefinert"
        self.hastighet = hastighet


class Jente(Person):
    __STØRSTE_FART = 100 / 11.5
    __MINSTE_FART = 100 / 13.5

    def __init__(self, hastighet: Optional[float] = None) -> None:
        if not hastighet:
            # gir personen en tilfelldig hastighet fra intervallet
            hastighet = random.uniform(self.__MINSTE_FART, self.__STØRSTE_FART)
        super().__init__(hastighet)
        self.kjønn = "jente"


class Gutt(Person):
    __STØRSTE_FART = 100 / 11
    __MINSTE_FART = 100 / 13

    def __init__(self, hastighet: Optional[float] = None) -> None:
        if not hastighet:
            # gir personen en tilfelldig hastighet fra intervallet
            hastighet = random.uniform(self.__MINSTE_FART, self.__STØRSTE_FART)
        super().__init__(hastighet)
        self.kjønn = "gutt"


class Lag:
    def __init__(self, gutter: list[Gutt], jenter: list[Jente]) -> None:
        self.antall_medlemmer = len(gutter) + len(jenter)
        self._gutter, self._jenter = gutter, jenter

        # definerer rekkefølgen laget skal løpe i
        self.rekkefølge = self._gutter + self._jenter
        random.shuffle(self.rekkefølge)


class Stafettkonkurranse:
    def __init__(self, antall_lag: int, lengde: float, lag: list[Lag]) -> None:
        # setter opp alt som trengs for løpet og sjekker om lagene er rettferdige

        self.antall_lag, self.løp_lengde, self._lag = antall_lag, lengde, lag

        assert lag, "Kan ikke starte ha en stafett uten lag"

        for enkelt_lag in lag:
            assert (
                enkelt_lag.antall_medlemmer == lag[0].antall_medlemmer
            ), "Kan ikke ha flere medlemmer i et lag"

        self.antall_løp = lag[0].antall_medlemmer

    def kjør_stafett(self) -> None:
        total_lengde = self.antall_løp * self.løp_lengde

        print(
            f"""Starter {total_lengde}m løp !!!\n\
            """
        )

        totale_tider = np.zeros((self.antall_lag))

        for etappe in range(self.antall_løp):
            print(f"Etappe {etappe+1}:")
            totale_tider += self._kjør_etappe(etappe=etappe)
            print()

        for x, tid in enumerate(totale_tider):
            print(f"Lag {x+1} brukte {tid:.2f} sekunder totalt!")

        print(f"\nLag {np.argmin(totale_tider)+1} vant!")

    def _kjør_etappe(self, etappe: int) -> list[float]:
        """Kjører en etappe (1 løper fra hvert lag) og samler tidene

        Returns
        -------
        list[float]
           Tidene til hver av løperne
        """
        tider = np.zeros((self.antall_lag), dtype=float)

        for x, lag in enumerate(self._lag):
            løper = lag.rekkefølge[etappe]

            tid = self.løp_lengde / løper.hastighet
            tider[x] = tid

            print(f"Lag {x+1} brukte {tid:.2f} sekunder og personen var {løper.kjønn}.")

        return tider


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
