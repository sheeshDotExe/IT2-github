import os
import requests
from requests.models import PreparedRequest
from .media_elements import MediaElement, MediaElementDetailed
from .media_elements import MovieElement, SeriesElement

MEDIA_TYPE_TO_ELEMENT = {
    "movie": MovieElement,
    "series": SeriesElement,
}


class API:
    def __init__(self) -> None:
        self.__api_key = os.environ.get("OMDB-API-KEY")
        assert self.__api_key, "OMDB API key not set, set in .env as OMDB-API-KEY"

        self.base_query_url = os.environ.get("OMDB-API-URL")
        assert self.base_query_url, "OMDB API URL not set, set in .env as OMDB-API-URL"

        self._cached_searches: dict[str, list[MediaElement]] = {}
        self._cached_elements: dict[str, MediaElementDetailed] = {}

        self.__request_session = requests.Session()

    def create_search_query(self, query_parameters: dict) -> PreparedRequest:
        query_parameters["apikey"] = self.__api_key
        request = requests.Request("GET", self.base_query_url, params=query_parameters)
        return request.prepare()

    def search(self, media_name: str, page: int = 1) -> list[MediaElement]:
        query = self.create_search_query({"s": media_name})

        if query.url in self._cached_searches:
            return self._cached_searches[query.url]

        result = self.__request_session.send(query, timeout=5)
        result.raise_for_status()

        assert result.status_code == 200, "API request failed"

        data = list(
            map(lambda element: MediaElement(**element), result.json()["Search"])
        )
        self._cached_searches[query.url] = data
        return data

    def get_detailed(self, media_element: MediaElement) -> MediaElementDetailed:
        if media_element.imdb_id in self._cached_elements:
            return self._cached_elements[media_element.imdb_id]

        query = self.create_search_query({"i": media_element.imdb_id, "plot": "short"})
        result = self.__request_session.send(query, timeout=5)
        result.raise_for_status()

        assert result.status_code == 200, "API request failed"

        data = MEDIA_TYPE_TO_ELEMENT[media_element.media_type](**result.json())
        self._cached_elements[media_element.imdb_id] = data
        return data
