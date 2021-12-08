""" Argumeents utils for Smog """

from argparse import ArgumentParser, Namespace

from rich.console import Console
from rich.theme import Theme
from rich.highlighter import RegexHighlighter


class Highlighter(RegexHighlighter):
    """ Highlighter for arguments help """
    
    base_style = "arguments."

    highlights = [
        r"(?P<metavar>[<\[]\w+[\]>])",
        r"(?P<argument>[\-]+[a-z]+)",
    ]


theme = Theme(
    {"arguments.metavar": "bold magenta", "arguments.argument": "bold green"}
)

console = Console(highlighter=Highlighter(), theme=theme)


class ParserError(Exception):
    """ Exception parser """


class ArgumentParser(ArgumentParser):
    """ Custom argument parser """

    def format_help(self):
        """ Format the help """
        formatter = self._get_formatter()

        formatter.add_usage(self.usage, self._actions,self._mutually_exclusive_groups)

        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        formatter.add_text(self.epilog)

        return formatter.format_help()

    def print_help(self):
        """ Display the help """
        return console.print(self.format_help(), highlight=True)

    def error(self, message):
        """ Raise error message """
        raise ParserError(message)
