""" Argumeents utils for Smog """

from argparse import ArgumentParser, Namespace

from smog.logger import console
from rich.panel import Panel


class ArgumentParser(ArgumentParser):
    """ Custom argument parser """

    class ParserError(Exception):
        """ Exception parser """

    def print_help(self):
        """ Display the help """
        return console.print(Panel(self.format_help(), width=80, highlight=True))

    def error(self, message):
        """ Raise error message """
        raise self.ParserError(message)
