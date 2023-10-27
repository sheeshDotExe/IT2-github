from konto import Bankkonto, BSUKonto, Sparekonto


def main() -> None:
    bankkonto = Bankkonto("Viktor", "1920.21.34098", 1500)
    bankkonto.uttak(2000)
    bankkonto.innskudd(500)
    print(bankkonto)


if __name__ == "__main__":
    main()
