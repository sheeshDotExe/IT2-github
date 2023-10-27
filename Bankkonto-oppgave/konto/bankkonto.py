class Bankkonto:
    def kroner_til_øre(kroner: float) -> int:
        return int(kroner * 100)

    def øre_til_kroner(øre: int) -> int:
        return øre / 100

    def __init__(self, navn: str, nummer: str, saldo: float) -> None:
        self.navn, self.nummer, self.saldo = (
            navn,
            nummer,
            Bankkonto.kroner_til_øre(saldo),
        )
        print("Opprettet konto:")
        print(self)

    def uttak(self, beløp: float) -> float | None:
        beløp_øre = Bankkonto.kroner_til_øre(beløp)
        print(f"Prøver å ta ut {beløp}kr.")
        if self.saldo < beløp_øre:
            print("Ikke nok penger på konto")
            print(f"Saldoen er {Bankkonto.øre_til_kroner(self.saldo)}kr\n")
            return None
        self.saldo -= beløp_øre
        print(f"Ny saldo er {Bankkonto.øre_til_kroner(self.saldo)}kr\n")
        return Bankkonto.øre_til_kroner(self.saldo)

    def innskudd(self, beløp: float) -> float:
        beløp_øre = Bankkonto.kroner_til_øre(beløp)
        print(f"Setter inn {beløp}kr.")
        self.saldo += beløp_øre
        print(f"Ny saldo er {Bankkonto.øre_til_kroner(self.saldo)}kr\n")
        return Bankkonto.øre_til_kroner(self.saldo)

    def __str__(self) -> str:
        return f"{'Eier':<15}: {self.navn}\n{'Kontonummer':<15}: {self.nummer}\n{'Saldo':<15}: {Bankkonto.øre_til_kroner(self.saldo)}kr\n"
