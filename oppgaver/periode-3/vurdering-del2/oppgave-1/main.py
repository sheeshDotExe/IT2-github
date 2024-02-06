import os, re
import numpy as np
from matplotlib import pyplot as plt

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(LOCAL_PATH, "../datasett")
OUTPUT_PATH = os.path.join(LOCAL_PATH, "../out")

MEDIA_FILE_PATH = os.path.join(DATA_PATH, "Medier.csv")


def unseralize_values(values: list[str]) -> list[int]:
    # converts all values to ints, years and data could be seperated but i cba
    converted_values = []
    for value in values:
        # if the value is . or .. it is a nan-value
        if value in "..":
            converted_values.append(np.nan)
        # if the is not numric, it is a year entry
        elif not value.isnumeric():
            converted_values.append(int(value[-6:-1]))
        # if the value is numeric, it is a data entry
        else:
            converted_values.append(int(value))
    return converted_values


def read_data(file_path: str):
    with open(file_path, encoding="utf-8") as f:
        raw_lines = list(map(lambda line: line.strip("\n"), f.readlines()))

    # the first line is the dataset header
    header = raw_lines.pop(0)

    mapped_data: dict[str, list[int]] = {}
    years = []

    # we iterate each line of csv and extract the value
    for line in raw_lines:
        if not line:
            continue
        field_key, *data = line.split(";")

        # if the field is of type "medietype", then it contains the years
        if field_key.strip('"') == "medietype":
            years = unseralize_values(data)
            continue

        mapped_data[field_key.strip('"')] = unseralize_values(data)

    return header, mapped_data, years


def subtask_a(header: str, years: list[int], dataset: dict) -> None:
    for media_type, minutes_spent in dataset.items():
        plt.plot(years, minutes_spent, label=media_type)

    plt.title(header, wrap=True)
    plt.legend(loc="upper right")
    plt.xlabel("År")
    plt.ylabel("Tid brukt i minutter")
    plt.savefig(os.path.join(OUTPUT_PATH, "task-a.png"))


def subtask_b(header: str, years: list[int], dataset: dict) -> None:
    for key in ("Hjemme-PC", "Bøker", "Internett"):
        plt.plot(years, dataset[key], label=key)

    plt.title("Plot over tid brukt til Hjemme-PC, Bøker and Internett")
    plt.xlabel("År")
    plt.ylabel("Tid brukt i minutter")
    plt.legend(loc="upper right")
    plt.savefig(os.path.join(OUTPUT_PATH, "task-b.png"))


def subtask_c(header: str, years: list[int], dataset: dict) -> None:
    for index, year in enumerate(years):
        filtered_values = list(
            map(lambda item: (item[0], item[1][index]), dataset.items())
        )

        media_type_max, usage_max = max(
            filtered_values,
            key=lambda item: item[1],
        )

        media_type_min, usage_min = min(filtered_values, key=lambda item: item[1])

        print(
            f"Year: {year}. Most used: {media_type_max} ({usage_max} min). Least used: {media_type_min} ({usage_min} min)"
        )


def main() -> None:
    header, dataset, years = read_data(MEDIA_FILE_PATH)
    subtask_a(header=header, years=years, dataset=dataset)
    subtask_b(header=header, years=years, dataset=dataset)
    subtask_c(header=header, years=years, dataset=dataset)


if __name__ == "__main__":
    main()
