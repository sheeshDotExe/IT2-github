# runs the chosen interface
from .internals import App
from .interfaces import CLI_APP


def testing() -> None:
    print("Testing the app")

    app = App()
    # results = app.search_media("Naruto")

    # for result in results:
    #     detailed = app.get_detailed(result)
    #     # print(detailed
    #     app.add_to_bucket_list(result)

    # app.save_bucket_list()

    for media in app.get_bucket_list():
        print(media)


def run_cli() -> None:
    app = App()
    CLI_APP.run(app)


def run_app() -> None:
    # testing()
    run_cli()
