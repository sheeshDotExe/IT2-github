import os

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

ABSOLUTE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))


def get_country_stats(df: pd.DataFrame, country_name: str) -> str:
    all_channels_in_country = df[df["Country"] == country_name]

    average_subs = sum(all_channels_in_country["subscribers"]) / (
        len(all_channels_in_country["subscribers"]) * 1e6
    )

    average_views = sum(all_channels_in_country["video views"]) / (
        len(all_channels_in_country["video views"]) * 1e6
    )

    return f"{country_name:<15} | average subs: {average_subs:.2f}M | average views: {average_views:.2f}M"


def subtask_a(sorted_channel_count: pd.DataFrame) -> None:
    plt.bar(sorted_channel_count.index, sorted_channel_count.values)
    plt.title("Countries with the most youtube channels")
    plt.xlabel("Country name")
    plt.ylabel("Number of channels")
    plt.subplots_adjust(top=0.9, bottom=0.25)
    plt.xticks(rotation=50)
    plt.show()


def main() -> None:
    with open(os.path.join(ABSOLUTE_DIR_PATH, "Global Youtube Statistics.csv")) as f:
        df = pd.read_csv(f)

    # some channels don't have a country
    # we can either give them a No Country flag or drop them
    # if we remove the line under then channels without a country will not be included
    df["Country"] = df["Country"].fillna("No country")

    sorted_channel_count = df["Country"].value_counts()[:10]

    print("Top ten countries by number of channels:")
    print(sorted_channel_count)
    subtask_a(sorted_channel_count)

    print("Average channel subscribers and views for the given countries:")
    for country in sorted_channel_count.index:
        print(get_country_stats(df, country))


if __name__ == "__main__":
    main()
