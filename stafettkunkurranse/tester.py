from implementasjon import Lag, Stafettkonkurranse


def kjør_tester(lag: list[Lag], stafettkonkurranse: Stafettkonkurranse) -> None:
    test_lag(lag=lag)
    print("Fullførte alle tester")


def test_lag(lag: list[Lag]) -> None:
    for lag_ in lag:
        assert lag_.antall_medlemmer == 4, "Laget må ha 4 medlemmer"
        assert len(lag_._gutter) == 2, "Laget må ha to gutter"
        assert len(lag_._jenter) == 2, "Laget må ha to jenter"
