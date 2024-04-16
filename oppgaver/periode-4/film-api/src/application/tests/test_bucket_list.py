from application.internals import App

app = App()

BUCKET_LIST_INITIAL_SIZE = len(app.get_bucket_list())


def test_add_to_bucket_list() -> None:
    naruto_results = app.search_media("Naruto")
    assert naruto_results

    for result in naruto_results:
        app.add_to_bucket_list(result)
        assert result in [media_element for media_element, _ in app.get_bucket_list()]

    assert len(app.get_bucket_list()) == len(naruto_results) + BUCKET_LIST_INITIAL_SIZE


def test_remove_from_bucket_list() -> None:
    naruto_results = app.search_media("Naruto")
    assert naruto_results

    for result in naruto_results:
        app.remove_from_bucket_list(result)
        assert result not in [
            media_element for media_element, _ in app.get_bucket_list()
        ]

    assert len(app.get_bucket_list()) == BUCKET_LIST_INITIAL_SIZE


def test_check_element_from_bucket_list() -> None:
    naruto_results = app.search_media("Naruto")
    assert naruto_results

    for result in naruto_results:
        app.add_to_bucket_list(result)
        app.check_element_from_bucket_list(result)
        assert result in [
            media_element for media_element, checked in app.get_bucket_list() if checked
        ]

    for result in naruto_results:
        app.uncheck_element_from_bucket_list(result)
        assert result not in [
            media_element for media_element, checked in app.get_bucket_list() if checked
        ]
