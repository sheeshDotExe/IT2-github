import pandas
from os import path
from matplotlib import pyplot as plt

LOCAL_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(LOCAL_PATH, "todos_oppgave1.json")


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
    plt.savefig(path.join(LOCAL_PATH, "Task6.png"))


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
    plt.savefig(path.join(LOCAL_PATH, "Task7.png"))


def main() -> None:
    # a : vi leser filen
    with open(DATA_PATH, encoding="utf-8") as f:
        df = pandas.read_json(f)

    subtask_7(df)


if __name__ == "__main__":
    main()
