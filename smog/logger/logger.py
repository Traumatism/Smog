""" Logger module for Smog. """

import time

from rich.console import Console

console = Console()


class Logger:
    """ Logger class for Smog """

    @classmethod
    def __log(cls, message: str, prefix: str) -> None:
        """ Log a message to the console """
        console.print(f"[dim cyan][{time.strftime('%H:%M:%S')}][/dim cyan] [bold white][{prefix}][/bold white] {message}")

    @classmethod
    def info(cls, message: str) -> None:
        """ Log an info message """
        cls.__log(message, "[bold cyan]*[/bold cyan]")

    @classmethod
    def warn(cls, message: str) -> None:
        """ Log a warning message """
        cls.__log(message, "[bold yellow]^[/bold yellow]")

    @classmethod
    def success(cls, message: str) -> None:
        """ Log a success message """
        cls.__log(message, "[bold green]+[/bold green]")
