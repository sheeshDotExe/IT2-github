import pandas
import numpy as np
from os import path
from matplotlib import pyplot as plt

LOCAL_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(LOCAL_PATH, "feilaktige_tasks.json")


def subtask_3(df: pandas.DataFrame):
    users = df["userId"].unique()
    print(f"Antall arbeidere: {len(users)}")
    print(f"Antall oppgaver: {len(df)}")
    print(f"Antall fullførte oppgaver: {len(df[df['completed']==True])}")


def subtask_4(df: pandas.DataFrame):
    print("Fullførte oppgaver:")
    completed = df["completed"] == True
    print(df[completed])

    print("Ikke fullførte oppgaver:")
    not_completed = df["completed"] == False
    print(df[not_completed])


def subtask_5(df: pandas.DataFrame):
    completed = df["completed"] == True
    # d : vi finner ut hvem som har løst flest oppgaver
    completed_tasks_count = df[completed]["userId"].value_counts()

    # multiple people may have completed similar tasks, we check them all
    last_score = 0
    while True:
        best_user = completed_tasks_count.idxmax()
        if completed_tasks_count[best_user] < last_score:
            break
        print(
            f"User {best_user} completed the most tasks, they completed: {completed_tasks_count[best_user]} tasks"
        )
        last_score = completed_tasks_count[best_user]
        completed_tasks_count[best_user] = 0


def subtask_6(df: pandas.DataFrame):
    completed = df["completed"] == True
    not_completed = df["completed"] == False

    completed_tasks = df[completed]
    not_completed_tasks = df[not_completed]

    plt.bar(
        ["Completed tasks", "Not completed tasks"],
        [len(completed_tasks), len(not_completed_tasks)],
    )
    plt.ylabel("Number of tasks completed")
    plt.title("Overview over all tasks")
    plt.show()


def subtask_7(df: pandas.DataFrame):
    completed = df["completed"] == True
    completed_tasks = df[completed]

    completed_tasks_count = completed_tasks["userId"].value_counts()

    total_tasks_completed = len(completed_tasks)
    labels = [
        f"User: {userID} ( {(tasks_completed*100)/total_tasks_completed:.2f}% )"
        for tasks_completed, userID in zip(
            completed_tasks_count.values, completed_tasks_count.index
        )
    ]

    plt.pie(completed_tasks_count.values, labels=labels)
    plt.title("User percent overview of tasks completed")
    plt.show()


def clean_dataset(df: pandas.DataFrame):
    # first we find duplicates
    cleaned_dataset = df.drop_duplicates(subset="id")
    print(f"Found {len(df)-len(cleaned_dataset)} duplicates found, removing them.")

    # we change user ids to ints
    cleaned_dataset["userId"] = cleaned_dataset["userId"].astype(int)

    # we fix estimates
    cleaned_dataset = cleaned_dataset.fillna("1d")

    # we fix titles
    fixed_titles = [" ".join(title.split()) for title in cleaned_dataset["title"]]
    cleaned_dataset["title"] = fixed_titles

    # we convert estimates to int
    converted_estimates = [
        int(estimate.strip("d")) if estimate else 0
        for estimate in cleaned_dataset["estimat"]
    ]
    cleaned_dataset["estimat"] = np.array(converted_estimates, dtype=int)

    return cleaned_dataset


def get_dataset(file_name: str) -> pandas.DataFrame:
    with open(path.join(LOCAL_PATH, file_name), encoding="utf-8") as f:
        df = pandas.read_json(f)

    return df


def test_dataset() -> None:
    dataset_with_errors = get_dataset("feilaktige_tasks.json")
    dataset_without_errors = get_dataset("todos_oppgave1.json")

    assert len(dataset_with_errors) == 3
    assert len(dataset_without_errors) == 139
    assert type(dataset_with_errors["estimat"][0]) == str
    assert type(dataset_without_errors["estimat"][0]) == str

    # we clean the dataset
    cleaned_dataset_with_errors = clean_dataset(dataset_with_errors)
    cleaned_dataset_without_erros = clean_dataset(dataset_without_errors)

    # we remove 1 duplicate
    assert len(cleaned_dataset_with_errors) == 2
    assert len(cleaned_dataset_without_erros) == 139
    assert type(cleaned_dataset_with_errors["estimat"][0]) == np.int32
    assert type(cleaned_dataset_without_erros["estimat"][0]) == np.int32


def main() -> None:
    test_dataset()


if __name__ == "__main__":
    main()
