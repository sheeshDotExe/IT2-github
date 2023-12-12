import numpy as np
import matplotlib.pyplot as plt
from os import path

dx = 1e-4

BASE_PATH = path.dirname(path.abspath(__file__))


def function(x: float) -> float:
    return x**3


def derivative(f: callable) -> callable:
    return lambda x: (f(x + dx) - f(x - dx)) / (2 * dx)


def main() -> None:
    x = np.linspace(-2, 2, 1000)

    f1, f2, f3 = function, derivative(function), derivative(derivative(function))
    y1, y2, y3 = (f1(x), f2(x), f3(x))
    labels = ("$f(x) = x^3$", "$f'(x) =3x^2$", "$f''(x) = 6x$")

    # same plot
    for y, label in zip((y1, y2, y3), labels):
        plt.plot(x, y, label=label)
    plt.title("Grafen til f(x), f'(x) og f''(x)")
    plt.legend()

    plt.savefig(path.join(BASE_PATH, "i-samme-plot.png"))
    plt.show()

    # i tre seperate subplots

    colors = ["b", "r", "g"]

    fig, ax = plt.subplots(3, 1)
    fig.tight_layout(h_pad=2)

    for index, (y, label, color) in enumerate(zip((y1, y2, y3), labels, colors)):
        ax[index].set_title(label)
        ax[index].plot(x, y, color, label=label)
        ax[index].legend()

    fig.suptitle("Grafen til f(x), f'(x) og f''(x)")
    plt.subplots_adjust(top=0.85)
    plt.savefig(path.join(BASE_PATH, "i-subplots-plot.png"))
    plt.show()


if __name__ == "__main__":
    main()
