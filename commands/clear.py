from smog.abstract.command import CommandBase
from smog.logger import console
from smog.banner import Banner


class Clear(CommandBase):

    command = "clear"
    description = "Clear the screen"
    aliases = ["cls"]

    def execute(self):
        console.clear()
        Banner.print()
