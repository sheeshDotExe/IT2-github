import cmd
from application.internals import App


class CLI_APP(cmd.Cmd):
    prompt = ">>> "
    intro = "Welcome to the media search app. Type 'help' for a list of commands"

    def __init__(self, app: App):
        super().__init__()
        self.app = app
        self.current_results = {}

    def do_search(self, media_name: str):
        """
        Perform a search for media based on the given name.

        Args:
            media_name (str): The name of the media to search for.

        Returns:
            None
        """
        results = self.app.search_media(media_name)
        self.current_results = {}
        for index, result in enumerate(results):
            self.current_results[index + 1] = result
            print(f"{index + 1}. {result.title} ({result.year})")

    def do_info(self, id: str):
        """
        Display detailed information about a media item.

        Parameters:
        - id (str): The ID of the media item to display information for.

        Returns:
        None
        """
        media = self.current_results[int(id)]
        detailed = self.app.get_detailed(media)
        print(
            f"Title: {media.title} Rating: {detailed.imdb_rating} Plot: {detailed.plot}"
        )

    def do_add(self, id: str):
        """
        Adds a media item to the bucket list.

        Parameters:
        - id (str): The ID of the media item to add.

        Returns:
        None
        """
        media = self.current_results[int(id)]
        self.app.add_to_bucket_list(media)
        print(f"{media.title} added to bucket list")

    def do_list(self, line):
        """
        Display the list of media items in the bucket.

        Args:
            line (str): The command line input.

        Returns:
            None
        """
        self.current_results = {}
        for index, media in enumerate(self.app.get_bucket_list()):
            self.current_results[index + 1] = media
            print(f"{index + 1}. {media.title} ({media.year})")

    def do_save(self, line):
        """
        Save the bucket list to a local file.

        Args:
            line (str): The command line input.

        Returns:
            None
        """
        self.app.save_bucket_list()
        print("Bucket list saved")

    @classmethod
    def run(cls, app: App):
        CLI_APP(app=app).cmdloop()
