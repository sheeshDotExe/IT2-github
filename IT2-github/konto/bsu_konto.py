from .bankkonto import Bankkonto

MAKS_INNSKUDD = 5000 * 100


class BSUKonto(Bankkonto):
    def __init__(self, navn: str, nummer: str, saldo: float) -> None:
        super().__init__(navn, nummer, saldo)
        self.innskudd_i_år = 0

    def innskudd(self, beløp: float) -> float | None:
        if self.innskudd_i_år + Bankkonto.kroner_til_øre(beløp) > MAKS_INNSKUDD:
            print("Du kan ikke sette inn mer penger på denne kontoen")
            return
        self.innskudd_i_år += Bankkonto.kroner_til_øre(beløp)
        return super().innskudd(beløp)
