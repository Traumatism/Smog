from os import system

from smog.abstract.command import CommandBase
from smog.logger import Logger

class Python(CommandBase):

    command = "python"
    aliases = ["py"]
    description = "Pop a Python REPL"

    def execute(self):
        Logger.info("Executing 'python3' command...")
        system("python3")
        Logger.success("Done!")
