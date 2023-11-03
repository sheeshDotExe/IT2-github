from konto import Bankkonto, BSUKonto, Sparekonto
from kontoeier import Person


def test_bankkonto() -> None:
    kontoeier = Person(
        navn="Viktor", etternavn="Vikingstad", telefonnummer="123", alder=99
    )

    assert kontoeier.navn == "Viktor"

    bankkonto = Bankkonto(kontoeier, "1920.21.34098", 0)
    assert bankkonto.saldo == 0

    bankkonto.innskudd(1000)
    assert bankkonto.saldo == 1000

    bankkonto.innskudd(2000)
    assert bankkonto.saldo == 3000

    bankkonto.uttak(1500)
    assert bankkonto.saldo == 1500

    bankkonto.uttak(2500)
    assert bankkonto.saldo == 1500


def test_bsukonto() -> None:
    kontoeier = Person(
        navn="Viktor", etternavn="Vikingstad", telefonnummer="123", alder=99
    )

    assert kontoeier.navn == "Viktor"

    bankkonto = BSUKonto(kontoeier, "1920.21.34098", 0)
    assert bankkonto.saldo == 0
    assert bankkonto.innskudd_i_år == 0

    bankkonto.innskudd(3000)
    assert bankkonto.saldo == 3000

    bankkonto.innskudd(3000)
    assert bankkonto.saldo == 3000

    bankkonto.innskudd(2000)
    assert bankkonto.saldo == 5000


def test_sparekonto() -> None:
    kontoeier = Person(
        navn="Viktor", etternavn="Vikingstad", telefonnummer="123", alder=99
    )

    assert kontoeier.navn == "Viktor"

    bankkonto = Sparekonto(kontoeier, "1920.21.34098", 0)
    assert bankkonto.saldo == 0
    assert bankkonto.antall_uttak == 5

    bankkonto.innskudd(1000)
    assert bankkonto.saldo == 1000

    for _ in range(5):
        bankkonto.uttak(100)
    assert bankkonto.saldo == 500
