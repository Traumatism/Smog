from smog.abstract.command import Command
from smog.logger import console
from smog.banner import Banner


class Clear(Command):

    command = "clear"
    description = "Clear the screen"
    aliases = ["cls"]

    def execute(self):
        console.clear()
        Banner.print()
