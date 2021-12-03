""" Smog abstract classes. """

from abc import ABC, abstractmethod

from rich.console import Console

from smog.database.database import Database
from smog.shell.arguments import ArgumentParser, argparse

from prompt_toolkit.completion import Completer, Completion

from typing import List


class Command(ABC):
    """ Abstract class for commands. """

    command: str = ""
    description: str = ""
    aliases: List[str] = []

    _arguments = {}

    def __init__(
        self,
        raw_arguments: List[str], 
        shell: ..., 
        console: Console, 
        database: Database
    ):
        self.shell = shell
        self.console = console
        self.database = database
        self.raw_arguments = raw_arguments

        self.parser = ArgumentParser(description=self.description, usage=self.command + " <options>")  
        self.arguments = argparse.Namespace()

    def init_arguments(self):
        """ Initialize command arguments """

    @abstractmethod
    def execute(self):
        """ Execute the command. """
