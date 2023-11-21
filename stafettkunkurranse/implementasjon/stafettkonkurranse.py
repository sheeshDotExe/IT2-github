import numpy as np
from .lag import Lag


class Stafettkonkurranse:
    def __init__(self, antall_lag: int, lengde: float, lag: list[Lag]) -> None:
        # setter opp alt som trengs for løpet og sjekker om lagene er rettferdige

        self.antall_lag, self.løp_lengde, self._lag = antall_lag, lengde, lag

        assert lag, "Kan ikke starte ha en stafett uten lag"

        for enkelt_lag in lag:
            assert (
                enkelt_lag.antall_medlemmer == lag[0].antall_medlemmer
            ), "Kan ikke ha flere medlemmer i et lag"

        self.antall_løp = lag[0].antall_medlemmer

    def kjør_stafett(self) -> None:
        total_lengde = self.antall_løp * self.løp_lengde

        print(
            f"""Starter {total_lengde}m løp !!!\n\
            """
        )

        totale_tider = np.zeros((self.antall_lag))

        for etappe in range(self.antall_løp):
            print(f"Etappe {etappe+1}:")
            totale_tider += self._kjør_etappe(etappe=etappe)
            print()

        for x, tid in enumerate(totale_tider):
            print(f"Lag {x+1} brukte {tid:.2f} sekunder totalt!")

        print(f"\nLag {np.argmin(totale_tider)+1} vant!")

    def _kjør_etappe(self, etappe: int) -> list[float]:
        """Kjører en etappe (1 løper fra hvert lag) og samler tidene

        Returns
        -------
        list[float]
           Tidene til hver av løperne
        """
        tider = np.zeros((self.antall_lag), dtype=float)

        for x, lag in enumerate(self._lag):
            løper = lag.rekkefølge[etappe]

            tid = self.løp_lengde / løper.hastighet
            tider[x] = tid

            print(f"Lag {x+1} brukte {tid:.2f} sekunder og personen var {løper.kjønn}.")

        return tider
