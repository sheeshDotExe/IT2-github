from kontoeier import Person


class Bankkonto:
    def kroner_til_øre(kroner: float) -> int:
        return int(kroner * 100)

    def øre_til_kroner(øre: int) -> int:
        return øre / 100

    def __init__(self, person: Person, nummer: str, saldo: float) -> None:
        self.__person, self.__nummer, self.__saldo = (
            person,
            nummer,
            Bankkonto.kroner_til_øre(saldo),
        )
        self.__person.bankkontoer.append(self)
        print("Opprettet konto:")
        print(self)

    @property
    def saldo(self) -> float:
        return Bankkonto.øre_til_kroner(self.__saldo)

    def uttak(self, beløp: float) -> float | None:
        beløp_øre = Bankkonto.kroner_til_øre(beløp)
        print(f"Prøver å ta ut {beløp}kr.")

        if self.__saldo < beløp_øre:
            print("Ikke nok penger på konto")
            print(f"Saldoen er {Bankkonto.øre_til_kroner(self.__saldo)}kr\n")
            return None

        self.__saldo -= beløp_øre
        print(f"Ny saldo er {Bankkonto.øre_til_kroner(self.__saldo)}kr\n")

        return Bankkonto.øre_til_kroner(self.__saldo)

    def innskudd(self, beløp: float) -> float:
        beløp_øre = Bankkonto.kroner_til_øre(beløp)
        print(f"Setter inn {beløp}kr.")

        self.__saldo += beløp_øre
        print(f"Ny saldo er {Bankkonto.øre_til_kroner(self.__saldo)}kr\n")

        return Bankkonto.øre_til_kroner(self.__saldo)

    def __str__(self) -> str:
        return f"{'Eier':<15}: {self.__person.navn}\n{'Kontonummer':<15}: {self.__nummer}\n{'Saldo':<15}: {Bankkonto.øre_til_kroner(self.__saldo)}kr\n"
