from implementasjon import Idrettsklubb, Gutt, Jente, Stafettkonkurranse
from tester import kjør_tester


def main() -> None:
    idrettsklubb = Idrettsklubb()

    for _ in range(4):
        idrettsklubb.leg_til_medlem(Gutt())

    for _ in range(4):
        idrettsklubb.leg_til_medlem(Jente())

    spesiell_gutt, spesiell_jente = Gutt(hastighet=10), Jente(hastighet=10)
    idrettsklubb.leg_til_medlem(spesiell_gutt)
    idrettsklubb.leg_til_medlem(spesiell_jente)

    stafett_lag = idrettsklubb.trekk_lag(lag_størrelse=4, antall_lag=2)
    stafett = Stafettkonkurranse(antall_lag=2, lengde=100, lag=stafett_lag)

    kjør_tester(lag=stafett_lag, stafett_konkurranse=stafett)
    stafett.kjør_stafett()


if __name__ == "__main__":
    main()
