from implementasjon import Idrettsklubb, Gutt, Jente, Stafettkonkurranse
from tester import kjør_tester


def main() -> None:
    idrettsklubb = Idrettsklubb()

    # legger til 4 vanlige gutter
    for _ in range(4):
        idrettsklubb.legg_til_medlem(Gutt())

    # legger til 4 vanlige jenter
    for _ in range(4):
        idrettsklubb.legg_til_medlem(Jente())

    # legger til én spesiell gutt og jente
    spesiell_gutt, spesiell_jente = Gutt(hastighet=10), Jente(hastighet=10)
    idrettsklubb.legg_til_medlem(spesiell_gutt)
    idrettsklubb.legg_til_medlem(spesiell_jente)

    # trekker ut lag og lager en stafettkonkurranse
    stafett_lag = idrettsklubb.trekk_lag(lag_størrelse=4, antall_lag=2)
    stafett = Stafettkonkurranse(antall_lag=2, lengde=100, lag=stafett_lag)

    # kjører tester på stafettkonkurransen og starter stafetten
    kjør_tester(lag=stafett_lag, stafettkonkurranse=stafett)
    stafett.kjør_stafett()


if __name__ == "__main__":
    main()
