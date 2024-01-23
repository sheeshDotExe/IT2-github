import matplotlib.pyplot as plt
from os import path

RELATIVE_PATH = path.dirname(path.abspath(__file__))


def plot_data_bar(x, y) -> None:
    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.xlabel("Høyde (moh)")
    plt.ylabel("Antall fritidsboliger")
    plt.subplots_adjust(left=0.15, top=0.9, bottom=0.25)
    plt.xticks(rotation=40)
    plt.title("Høyde i moh for fritidsboliger i 2019")
    plt.show()


def main() -> None:
    with open(
        path.join(RELATIVE_PATH, "fritidsboliger_moh_2019.csv"), encoding="utf-8"
    ) as f:
        dataset = list(map(lambda row: row.split(";"), f.read().split("\n")))

    # the data is written horisontaly so we transpose it
    meter_over_havet = []
    antall_boliger = []
    for label, data in zip(*dataset):
        meter_over_havet.append(label)
        antall_boliger.append(int(data))

    meter_over_havet_grense = None
    for index, label in enumerate(meter_over_havet):
        if "1000" in label:
            meter_over_havet_grense = index
            break
    else:
        raise ValueError("No 1000m found in labels ;(")

    plot_data_bar(meter_over_havet, antall_boliger)

    # vi samler alle boliger over 1000moh
    meter_over_havet = meter_over_havet[0:meter_over_havet_grense] + ["over 1000m"]
    antall_boliger = antall_boliger[0:meter_over_havet_grense] + [
        sum(antall_boliger[meter_over_havet_grense:])
    ]

    plot_data_bar(meter_over_havet, antall_boliger)


if __name__ == "__main__":
    main()
