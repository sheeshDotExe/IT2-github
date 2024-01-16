import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    utdanningsprogramer = [
        "Bygg- og anleggsteknikk",
        "Elektro og datateknologi",
        "Helse- og oppvekstfag",
        "Naturbruk",
        "Restaurant- og matfag",
        "Teknologi- og industrifag",
        "Håndverk, design og produktutvikling",
        "Frisør, blomster, interiør og eksponeringsdesign",
        "Informasjonsteknologi og medieproduksjon",
        "Salg, service og reiseliv",
    ]

    antallGutter = [3811, 4168, 8661, 2057, 1484, 5501, 313, 901, 1309, 2061]
    antallJenter = [352, 268, 7286, 1028, 709, 851, 243, 826, 200, 895]

    fig, ax = plt.subplots(5, 2)  # Angir dimensjoner for figure-objektet
    ax = ax.flatten()

    for index, (utdanningsprogram, antall_gutter, antall_jenter) in enumerate(
        zip(utdanningsprogramer, antallGutter, antallJenter)
    ):
        ax[index].pie([antall_gutter, antall_jenter], labels=["gutter", "jenter"])
        ax[index].set_title(utdanningsprogram, fontsize=12)

    plt.show()  # Viser diagrammet


if __name__ == "__main__":
    main()
