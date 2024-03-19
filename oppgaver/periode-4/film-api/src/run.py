from dotenv import load_dotenv
from application import run_app


def main() -> None:
    load_dotenv()
    run_app()


if __name__ == "__main__":
    main()
