import matplotlib.pyplot as plt


def main() -> None:
    aktiviteter = ["soving", "transport", "spising", "undervisning", "fritid"]
    tidsbruk = [6, 1, 1, 7, 9]

    plt.pie(tidsbruk, labels=aktiviteter)
    plt.show()


if __name__ == "__main__":
    main()
