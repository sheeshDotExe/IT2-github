import numpy as np
import matplotlib.pyplot as plt
import random
from os import path

DICE_EYES = 6
BASE_PATH = path.dirname(path.abspath(__file__))


def random_throws(number_of_throws: int) -> np.ndarray:
    throws = np.zeros((DICE_EYES), dtype=int)
    for _ in range(number_of_throws):
        throws[random.randint(0, DICE_EYES - 1)] += 1

    return throws


def main() -> None:
    x = range(1, DICE_EYES + 1)

    # task 1. 100 throws
    throws = random_throws(100)
    plt.scatter(x, throws)
    plt.savefig(path.join(BASE_PATH, "dice-throws-100.png"))
    plt.show()

    # task 2. Variable amount of throws
    number_of_throws = int(input("How many throws? "))
    throws = random_throws(number_of_throws=number_of_throws)
    plt.scatter(x, throws)
    plt.savefig(path.join(BASE_PATH, f"dice-throws-{number_of_throws}.png"))
    plt.show()


if __name__ == "__main__":
    main()
