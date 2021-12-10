from rich.console import Console

console = Console()


class Logger:
    """ Logger class for Smog """

    @classmethod
    def __log(cls, message: str, prefix: str):
        """ Log a message to the console """
        console.print(f"[bold bright_black][{prefix}][/bold bright_black] {message}")

    @classmethod
    def info(cls, message: str):
        """ Log an info message """
        cls.__log(message, "[bold cyan]info[/bold cyan]")

    @classmethod
    def warn(cls, message: str):
        """ Log a warning message """
        cls.__log(message, "[bold yellow]warn[/bold yellow]")

    @classmethod
    def error(cls, message: str):
        """ Log an error message """
        cls.__log(message, "[bold red]fail[/bold red]")

    @classmethod
    def success(cls, message: str):
        """ Log a success message """
        cls.__log(message, "[bold green]okay[/bold green]")
