""" Argumeents utils for Smog """

from argparse import ArgumentParser, HelpFormatter, Namespace
from typing import Dict, List

from rich.console import Console
from rich.theme import Theme
from rich.highlighter import RegexHighlighter


class Highlighter(RegexHighlighter):
    """ Highlighter for arguments help """

    base_style = "arguments."

    highlights = [
        r"(?P<metavar>[<\[]\w+[\]>])",
        r"(?P<argument>[\-]+[a-z]+)",
        r"(?P<opt>(options|positional arguments):)"
    ]


theme = Theme({
    "arguments.metavar": "bold magenta",
    "arguments.argument": "bold yellow",
    "arguments.usage": "cyan",
    "arguments.opt": "bold green"
})

console = Console(highlighter=Highlighter(), theme=theme)


class ParserError(Exception):
    """ Exception parser """


class HelpFormatter(HelpFormatter):
    """ Custom help formatter """

    def _metavar_formatter(self, action, default_metavar):
        result = action.metavar or ('/'.join(str(choice) for choice in action.choices) if action.choices else default_metavar)

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result, ) * tuple_size

        return format


class ArgumentParser(ArgumentParser):
    """ Custom argument parser """

    @property
    def completions(self) -> List[str]:
        c = []
        for action_x in self._action_groups:
            for action_y in action_x._group_actions:
                if action_y.choices is not None:
                    for k in action_y.choices:
                        c.append(k)
                for action_z in action_y.option_strings:
                    if action_z.startswith("-") is False: # positional arguments
                        continue
                    c.append(action_z)
        return c

    def _get_formatter(self):
        """ Return formatter """
        return HelpFormatter(prog="", indent_increment=4, width=console.width, max_help_position=console.width)

    def format_help(self):
        formatter = self._get_formatter()

        formatter.add_text(f"[cyan]{self.description}[/cyan]")

        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        return formatter.format_help()

    def print_help(self):
        """ Display the help """
        return console.print(self.format_help(), highlight=True)

    def error(self, message):
        """ Raise error message """
        raise ParserError(message)
