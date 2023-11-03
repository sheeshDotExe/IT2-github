from kontoeier import Person


class Bankkonto:
    def kroner_til_øre(kroner: float) -> int:
        return int(kroner * 100)

    def øre_til_kroner(øre: int) -> int:
        return øre / 100

    def __init__(self, person: Person, nummer: str, saldo: float) -> None:
        self.person, self.nummer, self._saldo = (
            person,
            nummer,
            Bankkonto.kroner_til_øre(saldo),
        )
        self.person.bankkontoer.append(self)
        print("Opprettet konto:")
        print(self)

    @property
    def saldo(self) -> float:
        return Bankkonto.øre_til_kroner(self._saldo)

    def uttak(self, beløp: float) -> float | None:
        beløp_øre = Bankkonto.kroner_til_øre(beløp)
        print(f"Prøver å ta ut {beløp}kr.")
        if self._saldo < beløp_øre:
            print("Ikke nok penger på konto")
            print(f"Saldoen er {Bankkonto.øre_til_kroner(self._saldo)}kr\n")
            return None
        self._saldo -= beløp_øre
        print(f"Ny saldo er {Bankkonto.øre_til_kroner(self._saldo)}kr\n")
        return Bankkonto.øre_til_kroner(self._saldo)

    def innskudd(self, beløp: float) -> float:
        beløp_øre = Bankkonto.kroner_til_øre(beløp)
        print(f"Setter inn {beløp}kr.")
        self._saldo += beløp_øre
        print(f"Ny saldo er {Bankkonto.øre_til_kroner(self._saldo)}kr\n")
        return Bankkonto.øre_til_kroner(self._saldo)

    def __str__(self) -> str:
        return f"{'Eier':<15}: {self.person.navn}\n{'Kontonummer':<15}: {self.nummer}\n{'Saldo':<15}: {Bankkonto.øre_til_kroner(self._saldo)}kr\n"
