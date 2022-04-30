import argparse

from typing import Iterator, Tuple

from rich.highlighter import RegexHighlighter
from rich.console import Console
from rich.markup import render
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text


class Highlighter(RegexHighlighter):
    """Highlighter for arguments help"""

    base_style = "arguments."

    highlights = [
        r"(?P<metavar>[<\[]\w+[\]>])",
        r"(?P<argument>[\-]+[a-z]+)",
        r"(?P<opt>(options|positional arguments):)",
    ]


theme = Theme(
    {
        "arguments.metavar": "bold magenta",
        "arguments.argument": "bold yellow",
        "arguments.usage": "cyan",
        "arguments.opt": "bold green",
    }
)

console = Console(highlighter=Highlighter(), theme=theme)


class ParserError(Exception):
    """Exception parser"""


class HelpFormatter(argparse.HelpFormatter):
    """Custom help formatter"""

    def _metavar_formatter(self, action, default_metavar):
        result = action.metavar or (
            "/".join(str(choice) for choice in action.choices)
            if action.choices
            else default_metavar
        )

        def format(tuple_size):
            return (
                result if isinstance(result, tuple) else (result,) * tuple_size
            )

        return format


class ArgumentParser(argparse.ArgumentParser):
    """Custom argument parser"""

    @property
    def completions(self) -> Iterator[str]:
        for action_x in self._action_groups:
            for action_y in action_x._group_actions:
                if action_y.choices is not None:
                    yield from action_y.choices

                for action_z in action_y.option_strings:
                    if action_z.startswith("-") is True:
                        yield action_z

    def _get_formatter(self):
        """Return formatter"""
        return HelpFormatter(
            prog="",
            indent_increment=4,
            width=console.width,
            max_help_position=console.width,
        )

    def format_help(self):
        formatter = self._get_formatter()

        for action_group in self._action_groups:
            if len(action_group._group_actions) == 1 and isinstance(
                action_group._group_actions[0], argparse._HelpAction
            ):
                continue

            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        return formatter.format_help()

    def get_help(self) -> Tuple[Panel, Text]:
        """Display the help"""

        return (
            Panel.fit(f"[bold magenta]{self.description}[/bold magenta]"),
            render(self.format_help()),
        )

    def print_help(self):
        """Display the help"""
        console.print(
            Panel.fit(f"[bold magenta]{self.description}[/bold magenta]")
        )

        console.print(self.format_help(), highlight=True)

    def error(self, message):
        """Raise error message"""
        raise ParserError(message)
