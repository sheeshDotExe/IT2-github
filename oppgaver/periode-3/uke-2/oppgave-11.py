from os import path
import csv
import matplotlib.pyplot as plt


def main() -> None:
    with open(
        path.join(path.dirname(path.abspath(__file__)), "mediebruk.csv"),
        encoding="utf-8",
    ) as f:
        mediebruk = csv.reader(f, delimiter=";")
        header = next(mediebruk)

        alders_grupper = []
        data = []

        for alders_gruppe, datapunkt in mediebruk:
            alders_grupper.append(alders_gruppe)
            data.append(int(datapunkt))

    plt.barh(alders_grupper, data)
    plt.title(header)
    plt.show()


if __name__ == "__main__":
    main()
