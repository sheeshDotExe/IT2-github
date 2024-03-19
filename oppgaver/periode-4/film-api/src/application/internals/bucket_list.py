import os, json
from .media_elements import MediaElement, MediaElementDetailed

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class BucketList:
    def __init__(self) -> None:
        self.__database = "Uniplemented"
        self.__local_database = os.environ.get("LOCAL-JSON-DATABASE-PATH")
        self.__elements: dict[str, tuple[MediaElement, bool]] = {}

    def add(self, media_element: MediaElement) -> None:
        if media_element.imdb_id not in self.__elements:
            self.__elements[media_element.imdb_id] = (
                media_element.model_dump(by_alias=True),
                False,
            )

    def remove(self, media_element: MediaElement) -> None:
        if media_element.imdb_id in self.__elements:
            del self.__elements[media_element.imdb_id]

    def check(self, media_element: MediaElement) -> None:
        if media_element.imdb_id in self.__elements:
            self.__elements[media_element.imdb_id] = (
                self.__elements[media_element.imdb_id][0],
                True,
            )

    def uncheck(self, media_element: MediaElement) -> None:
        if media_element.imdb_id in self.__elements:
            self.__elements[media_element.imdb_id] = (
                self.__elements[media_element.imdb_id][0],
                False,
            )

    def get(self) -> list[tuple[MediaElement, bool]]:
        return list(
            map(
                lambda element: (MediaElement(**element[0]), element[1]),
                self.__elements.values(),
            )
        )

    def load_from_local(self) -> None:
        assert (
            self.__local_database
        ), "Local database path not set, set in .env as LOCAL-JSON-DATABASE-PATH"
        json_file_path = os.path.join(BASE_PATH, self.__local_database)
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as file:
                self.__elements = json.load(file)

    def save_to_local(self) -> None:
        assert (
            self.__local_database
        ), "Local database path not set, set in .env as LOCAL-JSON-DATABASE-PATH"

        json_file_path = os.path.join(BASE_PATH, self.__local_database)
        with open(json_file_path, "w") as file:
            json.dump(self.__elements, file)
