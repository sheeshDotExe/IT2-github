from typing import Optional, Literal
import random

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
