import pandas
from os import path

LOCAL_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(LOCAL_PATH, "skandinavia.json")


def main() -> None:
    with open(DATA_PATH, encoding="utf-8") as f:
        df = pandas.read_json(f)
        print(df)

    # a : alle land
    land = [land["navn"] for land in df["land"]]
    print(land)

    # b : danske byer
    byer = [land["byer"] for land in df["land"]]
    land_til_byer = {land_navn: land_byer for land_navn, land_byer in zip(land, byer)}
    print(land_til_byer["Danmark"])

    # c : alle landene og byene
    for land_navn, land_byer in land_til_byer.items():
        print(f"{land_navn}: {land_byer}")

    # d : alle byer i danmark som starter på bokstaven A
    print(
        list(filter(lambda by: by and by[0].lower() == "a", land_til_byer["Danmark"]))
    )


if __name__ == "__main__":
    main()
