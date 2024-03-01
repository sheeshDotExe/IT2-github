import os
import pandas as pd
import matplotlib.pyplot as plt

MAPPE_STI = os.path.dirname(os.path.abspath(__file__))


def konverter_installasjoner(installasjoner: str) -> int:
    """
    Konverterer installasjoner fra streng til heltall.

    Args:
        installasjoner (str): Strengen som skal konverteres.

    Returns:
        int: Konverterte installasjoner som heltall.
    """
    return int(installasjoner.replace(",", "").replace("+", ""))


def skriv_kategori_statistikk(kategori_df: pd.DataFrame) -> None:
    """
    Skriver ut statistikk for en gitt kategori DataFrame.

    Parameters:
    kategori_df (pandas.DataFrame): DataFrame som inneholder app-data for en spesifikk kategori.

    Returns:
    None
    """
    antall_apper = len(kategori_df)  # Hent antall apper i kategori DataFrame
    gjennomsnittlig_vurdering = kategori_df[
        "Rating"
    ].mean()  # Beregn gjennomsnittlig vurdering for appene i kategorien
    gjennomsnittlig_installasjoner = (
        kategori_df["Installs"].apply(konverter_installasjoner).mean()
    )  # Beregn gjennomsnittlig antall installasjoner for appene i kategorien

    print(f"Antall Apper: {antall_apper}")  # Skriv ut antall apper i kategorien
    print(
        f"Gjennomsnittlig Vurdering: {gjennomsnittlig_vurdering:.2f}"
    )  # Skriv ut gjennomsnittlig vurdering for appene i kategorien
    print(
        f"Gjennomsnittlig Installasjoner: {gjennomsnittlig_installasjoner:.2f}"
    )  # Skriv ut gjennomsnittlig antall installasjoner for appene i kategorien
    print()

    modifisert_kategori_df = (
        kategori_df.copy()
    )  # Opprett en kopi av kategorien DataFrame
    modifisert_kategori_df["Installs"] = modifisert_kategori_df["Installs"].apply(
        konverter_installasjoner
    )  # Konverter "Installs"-kolonnen fra streng til heltall i den kopierte DataFrameen
    topp_apper = modifisert_kategori_df.nlargest(
        3, "Installs"
    )  # Hent de 3 appene med flest installasjoner i kategorien

    print("Topp 3 Apper:\n")
    for _, rad in topp_apper.iterrows():  # Gå gjennom radene i topp apper fra DataFrameen
        app_navn = rad["App"]  # Hent app-navnet
        antall_installasjoner = rad["Installs"]  # Hent antall installasjoner for appen
        print(f"App: {app_navn}")  # Skriv ut app-navnet
        print(
            f"Antall Installasjoner: {antall_installasjoner}"
        )  # Skriv ut antall installasjoner for appen
        print()

    print("-------------------------------------------------")


def hoved() -> None:
    """
    Hovedfunksjon som leser en CSV-fil som inneholder Google Play Store-data,
    utfører dataanalyse og skriver ut statistikk for de 3 kategoriene med flest apper.
    """
    # Sett stien til CSV-filen
    csv_sti = os.path.join(MAPPE_STI, "googleplaystore.csv")

    # Les CSV-filen inn i en pandas DataFrame
    df = pd.read_csv(csv_sti)

    # Fjern duplikate rader basert på "App"-kolonnen
    df.drop_duplicates(subset="App", inplace=True)

    # Tell antall apper i hver kategori
    kategori_tellinger = df["Category"].value_counts()

    # Hent de 3 kategoriene med flest apper
    topp_kategorier = kategori_tellinger.nlargest(3).index.tolist()
    print("Topp 3 Kategorier:", topp_kategorier)
    print()

    # Gå gjennom de øverste kategoriene og skriv ut statistikk for hver kategori
    for kategori in topp_kategorier:
        kategori_df = df[df["Category"] == kategori]
        print(f"Kategori: {kategori}")
        skriv_kategori_statistikk(kategori_df)


if __name__ == "__main__":
    hoved()
