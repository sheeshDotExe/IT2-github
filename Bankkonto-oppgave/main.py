from konto import Bankkonto, BSUKonto, Sparekonto


def main() -> None:
    bankkonto = Bankkonto("Viktor", "1920.21.34098", 0)
    bankkonto.innskudd(1000)
    bankkonto.innskudd(2000)
    bankkonto.uttak(1500)
    bankkonto.uttak(2500)
    print(bankkonto)


if __name__ == "__main__":
    main()
