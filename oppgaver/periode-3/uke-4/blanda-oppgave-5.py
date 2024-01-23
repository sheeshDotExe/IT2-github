import pandas
from os import path

LOCAL_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(LOCAL_PATH, "todos.json")


def main() -> None:
    # a : vi leser filen
    with open(DATA_PATH, encoding="utf-8") as f:
        df = pandas.read_json(f)

    # b : vi skriver ut oppgavene
    print(df[["title", "userId", "completed"]])

    # c : vi skriver ut oppgavene som er completed og ikke
    completed = df["completed"] == True
    print(df[completed])

    not_completed = df["completed"] == False
    print(df[not_completed])

    # d : vi finner ut hvem som har løst flest oppgaver
    completed_tasks_count = df[completed]["userId"].value_counts()

    best_user = completed_tasks_count.idxmax()
    print(f"user {best_user} completed {completed_tasks_count[best_user]} tasks")

    # e : vi finner ut hvem som har løst færrest oppgaver
    worst_user = completed_tasks_count.idxmin()
    print(f"user {worst_user} completed {completed_tasks_count[worst_user]} tasks")


if __name__ == "__main__":
    main()
