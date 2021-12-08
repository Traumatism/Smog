""" Module containing abstract commad class """
from typing import List
from rich.console import Console
from abc import ABC, abstractmethod

from smog.database.database import Database
from smog.utils.arguments import ArgumentParser, Namespace


class CommandBase(ABC):
    """ Abstract class for commands """

    command = ""
    description = ""
    aliases = []
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
        self.arguments = Namespace()

    def init_arguments(self):
        """ Initialize command arguments """

    @abstractmethod
    def execute(self):
        """ Execute the command """
