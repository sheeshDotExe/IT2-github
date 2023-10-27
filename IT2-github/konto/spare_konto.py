from .bankkonto import Bankkonto

ÅRLIGE_UTTAK = 5


class Sparekonto(Bankkonto):
    def __init__(self, navn: str, nummer: str, saldo: float) -> None:
        super().__init__(navn, nummer, saldo)
        self.antall_uttak = ÅRLIGE_UTTAK

    def uttak(self, beløp: float) -> float | None:
        if self.antall_uttak - 1 < 0:
            print("Du kan ikke ta ut mer penger fra denne kontoen i år")
            return
        self.antall_uttak -= 1
        return super().uttak(beløp=beløp)
