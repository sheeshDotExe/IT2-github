import matplotlib.pyplot as plt
from os import path

RELATIVE_PATH = path.dirname(path.abspath(__file__))


def main() -> None:
    with open(
        path.join(RELATIVE_PATH, "fritidsboliger_moh_2019.csv"), encoding="utf-8"
    ) as f:
        dataset = list(map(lambda row: row.split(";"), f.read().split("\n")))

    # the data is written horisontaly so we transpose it
    meter_over_havet = []
    antall_boliger = []
    for label, data in zip(*dataset):
        meter_over_havet.append(f"{label.split('-')[0]}m")
        antall_boliger.append(int(data))

    # b
    plt.barh(meter_over_havet, antall_boliger)
    plt.show()

    # c
    meter_over_havet = meter_over_havet[0:13] + ["over 1000m"]
    antall_boliger = antall_boliger[0:13] + [sum(antall_boliger[13:])]

    plt.barh(meter_over_havet, antall_boliger)
    plt.show()


if __name__ == "__main__":
    main()
