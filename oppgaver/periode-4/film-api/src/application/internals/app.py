import os
from .api import API
from .bucket_list import BucketList
from .media_elements import MediaElement, MediaElementDetailed
from .filter import Filter


class App:
    def __init__(self) -> None:
        self.__api = API()
        self.__bucket_list = BucketList()
        self.__filter = Filter()

        if os.environ.get("LOAD-BUCKET-LIST-ON-STARTUP"):
            self.__bucket_list.load_from_local()

    def search_media(self, media_name: str, page: int = 1) -> list[MediaElement]:
        return self.__filter.apply_filters(self.__api.search(media_name, page))

    def get_detailed(self, media_element: MediaElement) -> MediaElementDetailed:
        return self.__api.get_detailed(media_element)

    def get_media_image(self, media_element: MediaElement) -> str:
        return self.__api.get_media_image(media_element)

    def add_to_bucket_list(self, media_element: MediaElement) -> None:
        self.__bucket_list.add(media_element)

    def remove_from_bucket_list(self, media_element: MediaElement) -> None:
        self.__bucket_list.remove(media_element)

    def check_element_from_bucket_list(self, media_element: MediaElement) -> None:
        self.__bucket_list.check(media_element)

    def uncheck_element_from_bucket_list(self, media_element: MediaElement) -> None:
        self.__bucket_list.uncheck(media_element)

    def save_bucket_list(self) -> None:
        self.__bucket_list.save_to_local()

    def get_bucket_list(self) -> list[tuple[MediaElement, bool]]:
        return self.__filter.apply_filters(self.__bucket_list.get(), key=0)

    def get_filters(self) -> list[str]:
        return self.__filter.filters

    def toggle_filter(self, filter_name: str) -> None:
        self.__filter.toggle_filter(filter_name)
