import sys

from rich.prompt import Prompt

from smog.abstract.command import CommandBase


class Quit(CommandBase):

    command = "quit"
    description = "Exit Smog"
    aliases = ("leave", "exit", "q")

    def execute(self):
        response = Prompt.ask("Are you sure you want to exit? ", choices=["y", "n"])

        if response == "y":
            sys.exit(0)
