# runs the chosen interface
from .internals import App
from .interfaces import CLI_APP


def run_cli() -> None:
    app = App()
    CLI_APP.run(app)


def run_app() -> None:
    run_cli()
