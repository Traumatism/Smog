from rich.console import Console

from typing import Literal

console = Console()


class Logger:
    """ Logger class for Smog """

    @classmethod
    def __log(cls, message: str, prefix: str):
        """ Log a message to the console """
        console.print(f"[bold bright_black][{prefix}][/bold bright_black] {message}")

    @classmethod
    def info(cls, message: str) -> Literal[True]:
        """ Log an info message """
        cls.__log(message, "[bold cyan]info[/bold cyan]")
        return True

    @classmethod
    def warn(cls, message: str) -> Literal[False]:
        """ Log a warning message """
        cls.__log(message, "[bold yellow]warn[/bold yellow]")
        return False

    @classmethod
    def error(cls, message: str) -> Literal[False]:
        """ Log an error message """
        cls.__log(message, "[bold red]fail[/bold red]")
        return False

    @classmethod
    def success(cls, message: str) -> Literal[True]:
        """ Log a success message """
        cls.__log(message, "[bold green]okay[/bold green]")
        return True