from application.internals import App

app = App()


def test_get_by_name() -> None:
    naruto_results = app.search_media("Naruto")
    assert naruto_results


def test_get_info() -> None:
    naruto_results = app.search_media("Naruto")
    assert naruto_results

    naruto_info = app.get_detailed(naruto_results[0])
    assert naruto_info
