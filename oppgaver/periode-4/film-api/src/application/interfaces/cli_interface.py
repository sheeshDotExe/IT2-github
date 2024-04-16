import cmd, os
from application.internals import App


def validate_input(excpected_type: any):
    def decorator(func):
        def wrapper(self, line):
            try:
                return func(self, excpected_type(line))
            except ValueError:
                print(
                    f"Invalid input, excpected {excpected_type.__name__} got {type(line).__name__}"
                )
                return

        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


class CLI_APP(cmd.Cmd):
    prompt = ">>> "
    intro = "Welcome to the media search app. Type 'help' for a list of commands"

    def __init__(self, app: App):
        super().__init__()
        self.app = app
        self.current_results = {}
        self.filters = app.get_filters()

    def postcmd(self, stop: bool, line: str) -> bool:
        print()
        return stop

    def do_cls(self, line):
        """
        Clear the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")

    @validate_input(str)
    def do_search(self, media_name: str):
        """
        Perform a search for media based on the given name.

        Args:
            media_name (str): The name of the media to search for.
        """
        results = self.app.search_media(media_name)
        self.current_results = {}
        for index, result in enumerate(results):
            self.current_results[index + 1] = result
            print(f"{index + 1}. {result.title} ({result.year})")

    @validate_input(int)
    def do_info(self, id: int):
        """
        Display detailed information about a media item.

        Parameters:
        - id (int): The ID of the media item to display information for.
        """
        media = self.current_results[id]
        detailed = self.app.get_detailed(media)
        image = self.app.get_media_image(media)
        print(
            f"Title: {media.title}\nRating: {detailed.imdb_rating}\nPlot: {detailed.plot}"
        )
        print(image)

    @validate_input(int)
    def do_add(self, id: int):
        """
        Adds a media item to the bucket list, or a filter.

        Parameters:
        - id (int): The ID of the media item to add.
        """

        media = self.current_results[id]
        self.app.add_to_bucket_list(media)
        print(f"{media.title} added to bucket list")

    @validate_input(int)
    def do_toggle(self, id: int):
        """Toggle filter

        Parameters
        ----------
        id : int
            if of filter to toggle
        """
        filter_name = list(self.filters)[id - 1]
        self.app.toggle_filter(filter_name)
        print(
            f"{filter_name} filter toggled to {'on' if self.filters[filter_name] else 'off'}"
        )

    @validate_input(int)
    def do_remove(self, id: int):
        """
        Remove a media item from the bucket list.

        Args:
            id (int): The ID of the media item to remove.
        """
        media = self.current_results[id]
        self.app.remove_from_bucket_list(media)
        print(f"{media.title} removed from bucket list")

    @validate_input(int)
    def do_check(self, id: int):
        """
        Mark a media as watched in the bucket list.

        Args:
            id (int): The ID of the media item to check.
        """
        media = self.current_results[id]
        self.app.check_element_from_bucket_list(media)
        print(f"{media.title} marked as watched")

    @validate_input(int)
    def do_uncheck(self, id: int):
        """
        Mark a media as unwatched in the bucket list.

        Args:
            id (int): The ID of the media item to uncheck.
        """
        media = self.current_results[id]
        self.app.uncheck_element_from_bucket_list(media)
        print(f"{media.title} marked as unwatched")

    def do_list(self, line):
        """
        Display the list of media items in the bucket.
        """
        self.current_results = {}
        for index, (media, watch_status) in enumerate(self.app.get_bucket_list()):
            self.current_results[index + 1] = media
            print(
                f"{index + 1}. {media.title} ({media.year}) {'(watched)' if watch_status else '(not watched)'}"
            )

    def do_save(self, line):
        """
        Save the bucket list to a local file.
        """
        self.app.save_bucket_list()
        print("Bucket list saved")

    def do_filter(self, line):
        """
        Show all available filters and their status.
        """
        for index, (filter_name, is_active) in enumerate(self.filters.items()):
            print(f"({index+1}) {filter_name}: {'on' if is_active else 'off'}")

    @classmethod
    def run(cls, app: App):
        CLI_APP(app=app).cmdloop()
