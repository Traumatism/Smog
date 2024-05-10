from rich.console import Console
from typing import Literal

from smog import VARIABLES

console = Console()


class Logger:
    """Logger class for Smog"""

    SUCCESS = "+"
    ERROR = "-"
    WARNING = "!"
    INFO = "*"

    @classmethod
    def __log(cls, message: str, prefix: str):
        """Log a message to the console"""
        console.print(f"[{prefix}] {message}")

    @classmethod
    def info(cls, message: str) -> Literal[True]:
        """Log an info message"""
        cls.__log(message, f"[bold cyan]{cls.INFO}[/bold cyan]")
        return True

    @classmethod
    def warn(cls, message: str) -> Literal[False]:
        """Log a warning message"""
        cls.__log(message, f"[bold yellow]{cls.WARNING}[/bold yellow]")
        return False

    @classmethod
    def error(cls, message: str) -> Literal[False]:
        """Log an error message"""
        cls.__log(message, f"[bold red]{cls.ERROR}[/bold red]")
        return False

    @classmethod
    def success(cls, message: str) -> Literal[True]:
        """Log a success message"""
        cls.__log(message, f"[bold green]{cls.SUCCESS}[/bold green]")
        return True
