from .media_elements import MediaElement


def alphabetical_sort(media_elements: list[MediaElement]) -> list[MediaElement]:
    return sorted(media_elements, key=lambda media: media.title)


def sort_by_date(media_elements: list[MediaElement]) -> list[MediaElement]:
    return sorted(media_elements, key=lambda media: int(media.year))


def filter_by_movie(media_elements: list[MediaElement]) -> list[MediaElement]:
    return [media for media in media_elements if media.media_type == "movie"]


def filter_by_series(media_elements: list[MediaElement]) -> list[MediaElement]:
    return [media for media in media_elements if media.media_type == "series"]


def filter_by_game(media_elements: list[MediaElement]) -> list[MediaElement]:
    return [media for media in media_elements if media.media_type == "game"]


class Filter:
    ALL_FILTERS = {
        "alphabetical_sort": alphabetical_sort,
        "sort_by_date": sort_by_date,
        "movie": filter_by_movie,
        "series": filter_by_series,
        "game": filter_by_game,
    }

    def __init__(self) -> None:
        self.__filters = {filter_name: False for filter_name in self.ALL_FILTERS}

    @property
    def filters(self) -> dict[str, bool]:
        return self.__filters

    def toggle_filter(self, filter_name: str) -> None:
        self.__filters[filter_name] = not self.__filters[filter_name]

    def apply_filters(self, media_elements: list[MediaElement]) -> list[MediaElement]:
        for filter_name, is_active in self.__filters.items():
            if is_active:
                media_elements = self.ALL_FILTERS[filter_name](media_elements)
        return media_elements
