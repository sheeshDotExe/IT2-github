from application.internals import App


def main() -> None:
    print("Testing the app api")

    app = App()
    naruto_results = app.search_media("Naruto")
    assert len(naruto_results) == app.search_media("Naruto")

    for result in naruto_results:
        detailed = app.get_detailed(result)


if __name__ == "__main__":
    main()
