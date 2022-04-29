from smog.logger import console

from rich.text import Text
from typing import List, Tuple
from prompt_toolkit import ANSI


def parse_user_input(user_input: str) -> Tuple[str, List[str]]:
    """Parse user input to command name and arguments"""
    command, *args = user_input.split()
    return command.lower(), args


def rich_to_ansi(rich_text: str) -> ANSI:
    """Convert rich text to ANSI"""
    text = Text.from_markup(rich_text)
    rendered = ""

    for segment in text.render(console):
        if segment.style is None:
            continue

        style = segment.style.copy()

        style._color = segment.style.bgcolor
        style._bgcolor = style.color

        rendered += style.render(segment.text)

    return ANSI(rendered)
