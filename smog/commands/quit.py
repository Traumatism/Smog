import sys

from rich.prompt import Prompt

from smog.abstract.command import Command


class Quit(Command):

    command = "quit"
    description = "Exit Smog"
    aliases = ["leave", "exit", "q"]

    def execute(self):
        response = Prompt.ask("Are you sure you want to exit? ", default="n", choices=["y", "n"])

        if response == "y":
            sys.exit(1)
